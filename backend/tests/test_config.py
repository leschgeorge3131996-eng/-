from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

from backend.app.core import config as config_module


def make_workspace() -> Path:
    root = Path.cwd() / ".test_tmp" / uuid4().hex
    root.mkdir(parents=True, exist_ok=True)
    return root


def cleanup_workspace(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


def test_get_settings_respects_data_dir_env(monkeypatch) -> None:
    config_module.get_settings.cache_clear()
    workspace = make_workspace()
    monkeypatch.setattr(config_module, "_load_env_file", lambda _: None)
    monkeypatch.setenv("DATA_DIR", str(workspace / "persistent-data"))

    try:
        settings = config_module.get_settings()

        assert settings.data_dir == workspace / "persistent-data"
        assert settings.uploads_dir == settings.data_dir / "uploads"
        assert settings.parsed_dir == settings.data_dir / "parsed"
        assert settings.logs_dir == settings.data_dir / "logs"
        assert settings.cache_dir == settings.data_dir / "cache"
        assert settings.data_dir.exists()
    finally:
        config_module.get_settings.cache_clear()
        cleanup_workspace(workspace)
