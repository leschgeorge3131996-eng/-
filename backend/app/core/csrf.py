from __future__ import annotations

from collections.abc import Iterable
from urllib.parse import urlsplit

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.types import ASGIApp

from ..schemas.common import error_response

SAFE_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "TRACE"})


def _origin_from_url(value: str | None) -> str | None:
    if not value:
        return None
    candidate = value.strip()
    if not candidate:
        return None
    try:
        parsed = urlsplit(candidate)
    except ValueError:
        return None
    if not parsed.scheme or not parsed.hostname:
        return None
    netloc = parsed.hostname.lower()
    port = parsed.port
    default_ports = {"http": 80, "https": 443, "ws": 80, "wss": 443}
    if port and port != default_ports.get(parsed.scheme):
        netloc = f"{netloc}:{port}"
    return f"{parsed.scheme.lower()}://{netloc}"


def _normalize_pattern(raw: str) -> str | None:
    """Normalize either a plain origin or a wildcard pattern.

    Wildcard pattern format: ``scheme://*.domain.tld`` — matches any subdomain
    of ``domain.tld`` on the same scheme. Only a leading ``*.`` label is
    supported; this is the common form (e.g. ``https://*.trycloudflare.com``)
    and avoids the surprises of arbitrary-position glob matching.
    """
    if raw is None:
        return None
    candidate = raw.strip().rstrip("/")
    if not candidate:
        return None
    if "://*." in candidate:
        scheme, _, rest = candidate.partition("://")
        scheme = scheme.strip().lower()
        rest = rest.strip().lower()
        if not scheme or not rest.startswith("*."):
            return None
        suffix = rest[2:]
        if not suffix or "*" in suffix:
            return None
        return f"{scheme}://*.{suffix}"
    return _origin_from_url(candidate)


def normalize_allowed_origins(origins: Iterable[str]) -> frozenset[str]:
    normalized: set[str] = set()
    for origin in origins:
        normalized_value = _normalize_pattern(origin)
        if normalized_value:
            normalized.add(normalized_value)
    return frozenset(normalized)


def _origin_matches_allowlist(candidate: str, allowed: frozenset[str]) -> bool:
    if not candidate:
        return False
    if candidate in allowed:
        return True
    for entry in allowed:
        if "://*." not in entry:
            continue
        scheme, _, rest = entry.partition("://")
        if not rest.startswith("*."):
            continue
        suffix = rest[2:]
        prefix = f"{scheme}://"
        if not candidate.startswith(prefix):
            continue
        host_and_port = candidate[len(prefix) :]
        # Strip any port so the suffix match only compares hostnames. This
        # means a wildcard entry matches any port on the subdomain, which is
        # fine for demo tunnels and matches the intuition that the host is the
        # trust anchor, not the port.
        host_only = host_and_port.split(":", 1)[0]
        if host_only.endswith("." + suffix) and host_only != suffix:
            return True
    return False


class OriginValidationMiddleware(BaseHTTPMiddleware):
    """Reject state-changing requests whose Origin/Referer is not in the allowlist.

    Why this exists: cookie-backed sessions are vulnerable to CSRF when any origin
    can trigger a browser POST/DELETE that rides the session cookie. SameSite=Lax
    blocks most of this, but not all (top-level GET-to-POST redirects, some embeds).
    Validating Origin/Referer on state-changing methods is the OWASP-recommended
    defence and is sufficient when combined with SameSite=Lax.

    Requests without Origin AND without Referer are allowed through: CSRF requires
    a browser to attach the victim's cookie, and every modern browser sends at
    least one of those headers on state-changing requests. Server-to-server tooling
    (tests, curl without -e) legitimately omits both.
    """

    def __init__(
        self,
        app: ASGIApp,
        *,
        allowed_origins: Iterable[str],
        api_prefix: str = "/api",
    ) -> None:
        super().__init__(app)
        self._allowed = normalize_allowed_origins(allowed_origins)
        self._api_prefix = api_prefix.rstrip("/") or "/api"

    async def dispatch(self, request: Request, call_next):
        if request.method.upper() in SAFE_METHODS:
            return await call_next(request)

        if not request.url.path.startswith(self._api_prefix):
            return await call_next(request)

        origin_header = request.headers.get("origin")
        referer_header = request.headers.get("referer")

        # Some browsers/proxies may set Origin to the literal string "null" for
        # sandboxed iframes or file:// contexts; treat that as absent so we fall
        # through to the Referer check rather than silently blessing it.
        if origin_header and origin_header.strip().lower() == "null":
            origin_header = None

        claimed = _origin_from_url(origin_header) or _origin_from_url(referer_header)

        if claimed is None:
            return await call_next(request)

        if _origin_matches_allowlist(claimed, self._allowed):
            return await call_next(request)

        payload = error_response(
            "FORBIDDEN_ORIGIN",
            "请求来源不在允许列表，已被跨站伪造防护拒绝。",
            details={"origin": claimed},
        )
        return JSONResponse(status_code=403, content=payload.model_dump())
