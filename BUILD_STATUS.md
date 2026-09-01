# Build status

Verified locally in the build window:
- independent Git history created after 2026-09-01T00:00:00Z;
- fail-closed authority evaluator unit tests;
- Sibyl adapter contract tests with exact 0.8.0 API surface;
- deletion acceptance test;
- CI definition pins sibyl-memory-client==0.8.0.

Open gates:
- PyPI install is blocked in this runtime by DNS/network isolation;
- real SDK roundtrip and fresh-process judge acceptance are therefore skipped locally;
- dedicated public GitHub repository cannot be created by the connected GitHub action surface;
- GitHub Actions has not executed.

No PASS claim is permitted until those open gates execute successfully.
