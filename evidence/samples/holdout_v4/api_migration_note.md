# Atlas API Migration Note

## Scope

Atlas API v2 will replace the legacy v1 document ingestion endpoint.
The migration affects upload, parse-status polling, and page-render requests.
It does not affect billing exports or user invitation codes.

## Timeline

Sandbox access starts on 2026-09-02.
Partner integration testing runs from 2026-09-09 to 2026-09-23.
Production cutover is scheduled for 2026-10-06 at 01:00 UTC.
The v1 endpoint will remain read-only for 30 days after cutover.

## Compatibility

The maximum upload size increases from 20 MB to 50 MB.
The page-render API keeps the same default DPI value of 144.
Client SDK versions earlier than 1.8.0 are not supported.
Webhook signatures change from SHA-1 to SHA-256.

## Owners

The migration owner is Priya Nair.
SDK updates are owned by Marco Lee.
Partner communication is owned by Elena Rossi.

## Exclusions

This note does not define pricing for API overage.
This note does not provide a rollback date.
