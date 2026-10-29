# demo-repo 🎯

A demo target repository designed for **Green-Gate** to demonstrate the **red-then-green** verification moment.

## Vulnerability & Breaking Change Pattern

1. **Vulnerable Dependency**:
   - `requirements.txt` pins `Werkzeug==2.2.2`.
   - `pip-audit -r requirements.txt` flags multiple security advisories (e.g. `CVE-2024-34069`, `CVE-2024-49766`, `CVE-2024-49767`, `CVE-2025-66221`, `CVE-2026-21860`, `CVE-2026-27199`) with fix versions starting at `3.0.3` / `3.0.6` / `3.1.4+`.

2. **The Breaking Change**:
   - In Werkzeug 3.0, `werkzeug.urls.url_quote` was deprecated and completely removed.
   - `utils.py` uses:
     ```python
     from werkzeug.urls import url_quote
     ```
   - When a dependency-upgrade agent naively bumps `Werkzeug==2.2.2` to `>=3.0.3`, tests immediately fail with:
     ```
     ImportError: cannot import name 'url_quote' from 'werkzeug.urls'
     ```
     This produces the **RED** test failure in Green-Gate's isolated sandbox.

3. **The Agent's Fix**:
   - Rather than rolling back or hallucinating, the agent inspects the code and performs a minimal drop-in fix using the Python standard library:
     ```python
     from urllib.parse import quote as url_quote
     ```
   - Running tests again produces the **GREEN** verification moment: 5 passed tests!

## Running Manually

```bash
# 1. Pinned baseline (PASSES)
pip install -r requirements.txt pytest
pytest

# 2. Check vulnerability with pip-audit
pip-audit -r requirements.txt --format json

# 3. Upgrade to fixed version (FAILS with ImportError)
pip install "Werkzeug>=3.0.3"
pytest  # <-- RED (ImportError: cannot import name 'url_quote' from 'werkzeug.urls')

# 4. Apply fix in utils.py (PASSES)
# Replace `from werkzeug.urls import url_quote`
# with `from urllib.parse import quote as url_quote`
pytest  # <-- GREEN
```
