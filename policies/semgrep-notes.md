# Semgrep Notes
- CI uses `p/ci` ruleset (basic security + secrets checks).
- Add project-specific rules in `.semgrep.yml` at repo root if needed.
- Prefer scanning changed paths for large repos to keep runs fast.
