# ASD STIG + NIST SP 800-53 Rev. 5 review of Flight Review untrusted-input boundaries

This document records a source-code review of Flight Review's untrusted-input
and data boundaries against the DISA Application Security and Development
(ASD) STIG and NIST SP 800-53 Rev. 5, and the remediations applied in the
same change set. It is a developer-produced findings record. It does not
certify or attest compliance of any deployment; deployment-level facts that
cannot be established from source are listed under "needs-input".

## References

Rule identifiers were checked against the STIG text at review time.

- DISA Application Security and Development STIG, Version 6 Release 4
  (V6R4, benchmark date 2025-09-09), rule identifiers `V-2224xx`..`V-2226xx`.
  Rule text and severities consulted at
  https://www.stigviewer.com/stigs/application_security_and_development
  (version history: https://www.stigviewer.com/stigs/application_security_and_development/versions).
- NIST SP 800-53 Rev. 5 (incl. update 1),
  https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- CWE, https://cwe.mitre.org (e.g. https://cwe.mitre.org/data/definitions/22.html)

Note on rule IDs: the task brief suggested several IDs by topic. The V6R4
titles differ for some of them, so the table below uses the rule whose text
matches the finding:

| Topic | Rule used here (V6R4 title) |
|---|---|
| Input validation | V-222606 "must validate all input"; V-222609 "must not be subject to input handling vulnerabilities"; V-222605 "canonical representation vulnerabilities" |
| XSS | V-222602 "must protect from Cross-Site Scripting (XSS) vulnerabilities" |
| SQL injection | V-222607 "must not be vulnerable to SQL Injection" |
| Error handling | V-222610 "error messages ... without revealing information that could be exploited"; V-222611 "reveal error messages only to the ISSO, ISSM, or SA"; V-222656 "must not be subject to error handling vulnerabilities" |
| Audit records | V-222471/V-222472 "log user actions involving access to / changes to data"; V-222473 (when), V-222474 (which component), V-222476 (outcome), V-222477 (identity), V-222446 (time stamp) |
| Access control / authorization | V-222425 "enforce approved authorizations for logical access" |
| Session / authenticator exposure | V-222577 "must not expose session IDs"; V-222581 "must not use URL embedded session IDs"; V-222583 "unique session identifier using an approved RNG" |
| Transport | V-222596 "protect the confidentiality and integrity of transmitted information"; V-222597 "cryptographic mechanisms ... during transmission" |
| Secrets / keys | V-222642 "must not contain embedded authentication data"; V-222662 "Default passwords must be changed"; V-222588/V-222589 (cryptography at rest) |
| Dependencies | V-222614 "Security-relevant software updates and patches must be kept up to date"; V-222658 "products must be supported by the vendor or the development team" |
| Information disclosure | V-222600 "must not disclose unnecessary information to users" |
| Denial of service | V-222594 / V-222667 "protections against DoS attacks" |

Severity uses STIG categories: CAT I (high), CAT II (medium), CAT III (low).
Outcome is one of `satisfied`, `not-satisfied`, `needs-input`,
`not-applicable`. Findings marked "Remediated" were `not-satisfied` before
this change set and are `satisfied` after it, as verified by the unit tests
listed in the remediation section.

## Scope

Reviewed sources (`app/` unless noted): `tornado_handlers/upload.py`,
`tornado_handlers/multipart_streamer.py`, `tornado_handlers/download.py`,
`tornado_handlers/edit_entry.py`, `tornado_handlers/browse.py`,
`tornado_handlers/db_info_json.py`, `tornado_handlers/error_labels.py`,
`tornado_handlers/three_d.py`, `tornado_handlers/radio_controller.py`,
`tornado_handlers/common.py`, `tornado_handlers/send_email.py`,
`plot_app/helper.py`, `plot_app/config.py`, `plot_app/db_entry.py`,
`plot_app/main.py`, `plot_app/overview_generator.py`,
`plot_app/templates/*.html`, `serve.py`, `setup_db.py`, `prune_old_logs.py`,
`download_logs.py`, `config_default.ini`, `requirements.txt`, `Dockerfile`,
repository-root `docker-compose*.yml`, `nginx/default.conf`,
`nginx/default_ssl.conf`. The `plot_app/libevents` submodule was treated as a
dependency and not reviewed line by line.

## Trust boundaries

| # | Boundary | Entry points |
|---|---|---|
| B1 | Multipart ULog upload and temporary-file handling | `POST /upload` (`upload.py`, `multipart_streamer.py`) |
| B2 | Encrypted `.ulge` upload and private-key handling | `upload.py`, `helper.decrypt_ulge_payload`, `config_default.ini` `ulge_private_key`, `app/private_key/` |
| B3 | Log storage and download path construction | `download.py`, `helper.get_log_filename`, `overview_generator.py`, `prune_old_logs.py`, `edit_entry.py` |
| B4 | SQL statements | `db_entry.py`, `browse.py`, `db_info_json.py`, `edit_entry.py`, `upload.py`, `error_labels.py`, `main.py`, `common.py`, `serve.py`, `setup_db.py` |
| B5 | Edit/delete authorization via per-log token | `edit_entry.py`, token creation in `upload.py` |
| B6 | Browse/search parameters and reflection | `GET /browse`, `GET /browse_data_retrieval` (`browse.py`) |
| B7 | Jinja2/Bokeh template rendering, `safe` and manual escaping | `plot_app/templates/*.html`, `common.py` Jinja environment, `main.py` |
| B8 | Email sending | `send_email.py` |
| B9 | Outbound HTTP and client-exposed API tokens | `helper.download_file_maybe`, `download_logs.py`, `index.html` / `3d.html` map tokens |
| B10 | Error handling and exception detail in responses | `common.CustomHTTPError`, `common.write_error`, `print(...)` on error paths |
| B11 | Security-relevant logging / audit | (none before this change set) `plot_app/audit.py` |
| B12 | Cookies, sessions, transport, Nginx, Docker Compose, Dockerfile | `serve.py`, `nginx/*.conf`, `docker-compose*.yml`, `app/Dockerfile` |
| B13 | Dependency pinning | `app/requirements.txt` |

## Findings

`file:line` references are to the tree after this change set. Rows marked
"Remediated" describe the pre-change condition in the description and the
post-change implementation in the evidence column.

| ID | Boundary | file:line | Description | CWE | ASD STIG (V6R4) | NIST 800-53 r5 | Sev | Outcome | Evidence / notes |
|---|---|---|---|---|---|---|---|---|---|
| F-01 | B3 | `app/plot_app/helper.py:66`, `:73`, `:83`; `app/plot_app/security.py` (`is_valid_log_id`, `resolve_under`) | `validate_log_id` accepted any `[0-9a-zA-Z_-]+` and `get_log_filename` joined it under the storage directory; KML/preview/overview/prune paths were assembled independently from `log_id`. Remediated: UUID allow-list at the handler boundary, `realpath` containment check (`resolve_under`), single helper `get_log_derived_filename` used for `.ulg`, `.kml`, `.png`. Invalid IDs -> generic 400/404. | CWE-22, CWE-20 | V-222609, V-222605, V-222606 | SI-10 | CAT I | satisfied (remediated) | `tests/test_security.py` (`test_valid_log_ids`, `test_invalid_log_ids`, `resolve_under` symlink/escape tests), `tests/test_helper_paths.py` |
| F-02 | B1 | `app/tornado_handlers/upload.py:89-103` (`prepare`) ; `app/plot_app/config.py:44,180`; `app/config_default.ini:37` | Request body limit was raised to the client-supplied `expected_size` (up to 300 MB in `serve.py`); no configured server-side maximum. Remediated: `max_upload_size_mb` (default 100) enforced from `Content-Length` and `set_max_body_size`; oversize -> 413; missing/malformed `Content-Length` -> 411 and empty body -> 400 (`security.parse_content_length`); client value no longer consulted; `serve.py` sizes the HTTP server `max_buffer_size` to at least the configured limit. | CWE-400, CWE-770 | V-222594, V-222667, V-222606 | SI-10, SC-5 | CAT II | satisfied (remediated) | Config default matches nginx `client_max_body_size 100M`; audit event `upload/failure reason=request body exceeds max_upload_size` |
| F-03 | B1 | `app/tornado_handlers/upload.py:229-235` | ULog magic check existed for plain uploads but was inline and parsing errors bubbled to the user. Remediated: `security.is_ulog_header` on the first 16 bytes for plain and decrypted content; non-ULog -> generic "Invalid File" 400 with server-side detail; missing file part rejected. | CWE-434, CWE-20 | V-222606, V-222609 | SI-10 | CAT II | satisfied (remediated) | `tests/test_security.py::test_is_ulog_header*` |
| F-04 | B1 | `app/tornado_handlers/multipart_streamer.py:149`, `upload.py:375-376` | Streamed parts are written to `NamedTemporaryFile(delete=False)` in the storage dir; accepted file is moved to `<uuid>.ulg`. Remediated: parts are released from `post()`, `on_finish` and `on_connection_close` (idempotent `release()`), so aborted or over-limit streams do not leave temporary files behind; a stored `.ulg` whose parse or DB step fails is removed again (`_discard_stored_file`). Temp files are not world-readable beyond process umask; no user-controlled filename is used for the destination. | CWE-377, CWE-459 | V-222609 | SI-10, SC-28 | CAT III | satisfied (remediated) | `tests/test_multipart_cleanup.py`, `tests/test_upload_cleanup.py`. Original filename only used for the `.ulge` suffix decision (F-05) |
| F-05 | B2 | `app/tornado_handlers/upload.py:203-227`; `app/plot_app/helper.py:600-640` | Decryption exceptions (incorrect key, corrupt file, key path) were reflected in the HTTP error. Remediated: failures logged server-side with a correlation id, user sees generic "Invalid File"; decrypted bytes must pass the ULog magic check before being written. `decrypt_ulge_payload` uses RSA-OAEP(SHA-256) + ChaCha20 via PyCryptodome. | CWE-209, CWE-20 | V-222610, V-222606 | SI-11, SI-10, SC-13 | CAT II | satisfied (remediated) | Decryption itself unchanged |
| F-06 | B2 | `app/config_default.ini:41`; `app/plot_app/config.py:62,193`; `app/private_key/`; `.gitignore:25` | Private key location is a config path; `private_key.pem` is git-ignored and only a `dummy_key.pem` placeholder is tracked. Whether the operational key is protected at rest (permissions, HSM/KMS, rotation) cannot be determined from source. | CWE-522 | V-222642, V-222588 | SC-12, SC-13, SC-28 | CAT II | needs-input | See "needs-input" section, item 5 |
| F-07 | B3 | `app/tornado_handlers/download.py` (`DownloadHandler.get`, `is_public_log`) | Download of `.ulg`/`.kml`/derived files used `log_id` to build paths; original filename from the DB was placed in `Content-Disposition` unsanitized. Remediated: paths via `get_log_derived_filename`; `sanitize_header_value` on the attachment filename; quoted KML filename; `is_public_log` parameterized; private-log downloads audited. | CWE-22, CWE-113 | V-222609, V-222606 | SI-10, AU-2 | CAT II | satisfied (remediated) | Audit event `log_download` with `public=False` |
| F-08 | B4 | `app/tornado_handlers/browse.py:346-362`; `db_info_json.py:34-38`; `edit_entry.py:89-112`; `error_labels.py:44`; `upload.py:262`; `plot_app/main.py:134,152`; `common.py:93,128`; `setup_db.py` | All statements that carry request data use `?` placeholders. `browse.py` builds `ORDER BY` from an index into a fixed column list and `LIKE` patterns via `_escape_like`; page size is capped (`_MAX_PAGE_SIZE`). `setup_db.py` executes static DDL only. `serve.py` has no SQL. | CWE-89 | V-222607 | SI-10 | CAT I | satisfied | No string-formatted SQL with untrusted input found |
| F-09 | B5 | `app/tornado_handlers/upload.py:248`; `app/plot_app/security.py` (`generate_token`, `tokens_match`, `is_valid_token_format`) | Token was `binascii.hexlify(os.urandom(16))` and compared with `!=`. Remediated: `secrets.token_hex(16)`; allow-list format check before DB lookup; `hmac.compare_digest`; token never written to audit or error output. | CWE-208, CWE-330 | V-222583, V-222425 | IA-5, AC-3, SC-13 | CAT II | satisfied (remediated) | `tests/test_security.py::test_generate_token*`, `test_tokens_match*`, `test_is_valid_token_format*` |
| F-10 | B5 | `app/tornado_handlers/edit_entry.py:30-60`; `upload.py` (delete link in the upload confirmation / email) | The edit/delete capability token is transported as a URL query parameter (`/edit_entry?action=delete&log=...&token=...`). This is inherent to the emailed-link design; it means the token appears in browser history, referrer headers and proxy access logs (nginx `access_log` is enabled). | CWE-598 | V-222581, V-222577 | IA-5, AC-3, SC-8 | CAT II | not-satisfied | Documented, not remediated: changing the transport requires a UX/design decision (e.g. POST form or one-time link). Audit records now cover malformed/mismatched token attempts (`log_edit/failure`). |
| F-11 | B5 | `app/tornado_handlers/edit_entry.py:36-40` | No rate limiting or lockout on token guesses. Token entropy is 128 bits so online guessing is impractical; malformed attempts are audited. | CWE-307 | V-222425 | AC-7 | CAT III | satisfied | Compensated by 128-bit token + audit record |
| F-12 | B6 | `app/tornado_handlers/browse.py:321-360` | `search[value]`, `order[0][column]`, `order[0][dir]`, `start`, `length` are validated (int parsing, index bounds, capped length) and only used through parameters or fixed column names. Malformed ints raise `ValueError` -> handled by `write_error` as 500 (generic). | CWE-20 | V-222606 | SI-10 | CAT III | satisfied | Consider 400 instead of 500 for malformed ints (non-security) |
| F-13 | B6/B7 | `app/tornado_handlers/browse.py` (`BrowseHandler.get`), `app/plot_app/templates/browse.html` (`"search": {{ initial_search }}`) | The `search` query parameter was rendered inside a `<script>` block; Jinja2 autoescape is not enabled in `common.py`'s `Environment`, so `</script>` breakout was possible. Remediated: `security.json_for_script` (JSON + `\u003c`/`\u003e`/`\u0026`/U+2028/2029 escaping). | CWE-79 | V-222602 | SI-10 | CAT I | satisfied (remediated) | `tests/test_security.py::test_json_for_script*` |
| F-14 | B7 | `app/tornado_handlers/common.py` (`get_jinja_env`), `app/plot_app/templates/*.html` | Jinja2 `Environment` is created without `autoescape`. Templates that render request-derived values (`browse.html` search, `3d.html`/`index.html` config tokens, upload confirmation) rely on the handler escaping values by hand (`html.escape` in `upload.py:139-185`). No Jinja `safe` filters were found; Bokeh `plot_app/main.py` builds `Div` HTML from static strings and DB fields that were escaped at upload time. | CWE-79, CWE-116 | V-222602 | SI-10 | CAT II | not-satisfied | Documented, not remediated: enabling autoescape would double-escape existing DB content that was stored HTML-escaped; needs a data migration decision. Manual escaping is currently applied consistently at ingest. |
| F-15 | B8 | `app/tornado_handlers/send_email.py` (`_send_email`); `app/plot_app/security.py` (`sanitize_header_value`); `helper.is_valid_email:412` | User-influenced description was truncated into the mail `Subject`; destinations were passed through unchecked. Remediated: CR/LF and control characters stripped and length-limited on `Subject`; every destination must pass `is_valid_email`; body stays `MIMEText` plain text. | CWE-93 | V-222606 | SI-10 | CAT II | satisfied (remediated) | `tests/test_security.py::test_sanitize_header_value*` |
| F-16 | B8 | `app/config_default.ini:47-59` (`[email]` `user_name`/`password`, `smtpserver`) | SMTP credentials are read from the ini file mounted read-only into the container. Whether the operational file has restricted permissions / uses a secret store cannot be determined from source. Defaults are empty (no embedded credentials). | CWE-522 | V-222642, V-222662 | IA-5, SC-28 | CAT II | needs-input | See "needs-input" section, item 6 |
| F-17 | B9 | `app/plot_app/helper.py:116` (`urlretrieve` of airframe/releases metadata from fixed URLs); `app/download_logs.py:119,178` | Outbound URLs are constants in config/code, not request-controlled; `requests.get` calls set timeouts. `download_logs.py` is an operator CLI, not a web entry point. | CWE-918 | V-222609 | SI-10, SC-7 | CAT III | satisfied | `validate_url` (`helper.py:282`) additionally restricts the uploader `videoUrl` field to http(s)/ftp URLs |
| F-18 | B9 | `app/plot_app/templates/index.html:33`, `3d.html:149-150`; `app/plot_app/config.py:39-40` | Mapbox / Cesium Ion tokens are emitted into client-side JavaScript. These are public-by-design browser tokens; exposure is expected. Whether the configured tokens are URL-restricted at the provider is an operational fact. | CWE-200 | V-222600 | CM-6, SC-8 | CAT III | needs-input | Operator must confirm provider-side restrictions (domain allow-list) on the tokens |
| F-19 | B10 | `app/tornado_handlers/common.py:44-72` (`write_error`); `audit.py` (`new_correlation_id`, `log_server_error`) | `write_error` rendered `CustomHTTPError.error_message` unescaped and no server-side detail was logged; several handlers did not inherit the common base. Remediated: single `write_error` path, generic text plus a 12-hex correlation id, exception detail (with traceback for 5xx) logged server-side; `BrowseHandler`, `BrowseDataRetrievalHandler`, `DBInfoHandler`, `RadioControllerHandler`, `UpdateErrorLabelHandler`, `EditEntryHandler` now derive from `TornadoRequestHandlerBase`. Explicit `CustomHTTPError` messages are static strings and are HTML-escaped. | CWE-209, CWE-79 | V-222610, V-222611, V-222656 | SI-11 | CAT II | satisfied (remediated) | `tests/test_audit.py::test_new_correlation_id*`, `test_log_server_error_includes_correlation_id_and_traceback` |
| F-20 | B10 | `app/tornado_handlers/upload.py:62,65,235,283`; `edit_entry.py:108`; `common.py:136`; `plot_app/main.py:168` | Remaining `print(...)` calls on non-error paths log operational info (file moves, vehicle names from DB, plot URL). Exception text on the `.ulge` path and upload failure path no longer goes to the client. `main.py` shows a static "Internal Server Error" page for unhandled plot exceptions. | CWE-532 | V-222444 | AU-3, SI-11 | CAT III | satisfied | Vehicle name is user-supplied but is escaped at ingest and only written to stdout |
| F-21 | B11 | `app/plot_app/audit.py`; call sites in `upload.py:107,238`, `edit_entry.py:37,44,53`, `download.py` | No structured audit record existed for upload / delete / edit-token failure / private download. Remediated: `audit_log(event, outcome, **fields)` emits one JSON line (`timestamp` UTC ISO-8601 ms, `event`, `outcome`, `log_id`, `client_ip`, `reason`, ...) via `logging` logger `flight_review.audit`; no external sink. | CWE-778 | V-222471, V-222472, V-222473, V-222474, V-222476, V-222477, V-222446 | AU-2, AU-3, AU-12 | CAT II | satisfied (remediated) | `tests/test_audit.py`. Identity field is `client_ip` (no user accounts exist; see F-23). Retention/off-loading (V-222481/V-222482) is deployment-side: needs-input item 7 |
| F-22 | B12 | `serve.py:118-130`; `app/tornado_handlers/*.py` | The application sets no cookies and has no login or server-side session; Bokeh session ids are per-document websocket tokens generated by Bokeh. HTTPOnly/Secure cookie flags and session timeout rules have no application-side object to apply to. | - | V-222575, V-222576, V-222388-V-222391 | AC-12, SC-23 | - | not-applicable | Basic-auth (`auth_basic` in `nginx/default_ssl.conf:41-42`) is the only authentication and is outside the application |
| F-23 | B12 | `nginx/default_ssl.conf:41-42`, `docker-compose.prod.yml` (`.htpasswd` mount) | Administrative functions (delete via token, DB access, prune scripts) have no application-level IdP/MFA; the production compose file gates the whole site with nginx basic auth from a mounted `.htpasswd`. Existence, strength, and MFA status of that mechanism cannot be determined from source. | CWE-306 | V-222522, V-222526, V-222425 | IA-2, IA-5, AC-3 | CAT II | needs-input | See "needs-input" item 4 |
| F-24 | B12 | `nginx/default_ssl.conf:6-32`; `nginx/default.conf` | `default_ssl.conf` redirects 80->443, serves TLS with Let's Encrypt certificates and includes `options-ssl-nginx.conf` (protocol/cipher policy comes from that generated file, not from this repo). No HSTS header and no `X-Content-Type-Options`/`X-Frame-Options`/CSP headers are configured. `default.conf` (plain HTTP) is a valid `NGINX_CONF` choice. Which profile is deployed and the resulting TLS policy cannot be determined from source. | CWE-319, CWE-693 | V-222596, V-222597 | SC-8, SC-8(1), SC-13, CM-6 | CAT I | needs-input | See "needs-input" items 1-2. The application itself listens on plain HTTP 5006 and relies on the proxy. |
| F-25 | B12 | `app/Dockerfile:1-18`; `docker-compose*.yml` | Image is `ubuntu:noble` (floating tag), runs as root (no `USER`), copies the full `app/` tree including `private_key/dummy_key.pem`; `docker-compose.yml`/`.dev.yml` publish 5006 directly and bind-mount `./app` read-write. `env_file: .env` is not tracked. | CWE-250, CWE-1104 | V-222614, V-222626 | CM-6, CM-7, SC-28 | CAT II | not-satisfied | Documented, not remediated (deployment hardening decision: non-root user, pinned base digest, exclude dev compose from production) |
| F-26 | B13 | `app/requirements.txt:1-11` | Only `bokeh==3.8.2` is exact-pinned; `jinja2`, `jupyter`, `pyfftw`, `pylint`, `requests`, `simplekml`, `smopy` are unbounded, `pyulog`, `scipy`, `pycryptodome` are lower-bounded. No lock file / hash pinning; no SCA/vulnerability scan in CI. `jupyter` and `pylint` are build/dev tools installed into the runtime image (CM-7). | CWE-1104, CWE-1395 | V-222614, V-222658 | RA-5, SI-2, CM-7, SA-11 | CAT II | not-satisfied | Documented, not remediated: pinning requires a compatibility test across the CI Python matrix (3.10-3.13) and is out of scope for this change set |
| F-27 | B6/B7 | `app/tornado_handlers/browse.py` (`BrowseDataRetrievalHandler.get` JSON output) | Server-side DataTables JSON embeds DB fields (description, feedback, vehicle name, rating) that were HTML-escaped at upload (`upload.py:139-185`) and are re-escaped in the JS renderer. `Content-Type: application/json` is set. | CWE-79 | V-222602 | SI-10 | CAT III | satisfied | No change |
| F-28 | B1 | `app/tornado_handlers/upload.py:139-185` | Form fields (`description`, `feedback`, `windSpeed`, `rating`, `videoUrl`, `vehicleName`, `email`, `allowForAnalysis`) are HTML-escaped; `windSpeed` parsed as int; `videoUrl` passed through `validate_url`; `email` through `is_valid_email`; `rating`/`type` compared against fixed value sets. No length limits beyond the upload body cap. | CWE-20 | V-222606 | SI-10 | CAT III | satisfied | Length limits on free-text fields are a possible hardening (not a finding under the reviewed rules) |
| F-29 | B3/B5 | `app/tornado_handlers/download.py` (`DownloadHandler.get`, `is_public_log`); `app/plot_app/main.py` (`/plot_app?log=`); `upload.py` (`public` form field) | Logs uploaded with `public=false` are unlisted (excluded from browse/`dbinfo` by `Logs.Public = 1`) but are served by the plot page and every download type to any client that knows the `log_id`. Access control is knowledge of the 122-bit random UUID (capability URL); no authentication or per-log authorization is applied, and the same URL is what the uploader is given to share. Remediated only as a compensating measure: `log_download` audit records with `public=False`, strict UUID allow-list (no enumeration via path tricks). | CWE-284, CWE-639 | V-222577, V-222589 | AC-3, IA-2 | CAT II | not-satisfied | Documented, not remediated: whether unlisted-by-UUID is an acceptable access model, or whether private logs need an authenticated owner/reader concept, is a system-owner decision (see needs-input item 4). |

### Outcome totals

| Outcome | Count | Findings |
|---|---|---|
| satisfied | 18 | F-01, F-02, F-03, F-04, F-05, F-07, F-08, F-09, F-11, F-12, F-13, F-15, F-17, F-19, F-20, F-21, F-27, F-28 (11 of these were remediated in this change set: F-01, F-02, F-03, F-04, F-05, F-07, F-09, F-13, F-15, F-19, F-21) |
| not-satisfied | 5 | F-10, F-14, F-25, F-26, F-29 |
| needs-input | 5 | F-06, F-16, F-18, F-23, F-24 |
| not-applicable | 1 | F-22 |

29 findings in total. F-21 is counted as satisfied for the application-side
control and additionally raises a needs-input item (7) for deployment-side
audit retention. Every boundary B1-B13 has at least one row with an outcome.
`app/tests/test_review_doc.py` checks that these totals match the findings
table.

## Remediated in this change set

| Finding | Change | Tests |
|---|---|---|
| F-01, F-07 | `plot_app/security.py`: `LOG_ID_RE` (UUID), `is_valid_log_id`, `resolve_under` (realpath containment). `plot_app/helper.py`: `validate_log_id`, `get_log_filename`, new `get_log_derived_filename`. Call sites: `download.py`, `edit_entry.py`, `overview_generator.py`, `prune_old_logs.py`. | `tests/test_security.py`, `tests/test_helper_paths.py` |
| F-02, F-03, F-05 | `upload.py` `prepare()` enforces `config.get_max_upload_size()` (`max_upload_size_mb`, default 100); `is_ulog_header` on plain and decrypted content; generic "Invalid File"/"File too large" to client, detail server-side. | `tests/test_security.py` (`is_ulog_header`, `is_ulge_header`) |
| F-04 | `multipart_streamer.py` `TemporaryFileStreamedPart.release()` is idempotent; `upload.py` releases parts from `post()`, `on_finish` and `on_connection_close` so aborted/over-limit streams leave no temporary files; `_discard_stored_file` removes a stored log whose parse/DB step failed. | `tests/test_multipart_cleanup.py`, `tests/test_upload_cleanup.py` |
| F-09 | `generate_token` (`secrets.token_hex`), `is_valid_token_format`, `tokens_match` (`hmac.compare_digest`); `edit_entry.py` validates format before lookup and never echoes the token. | `tests/test_security.py` |
| F-13 | `json_for_script` used for `initial_search` in `browse.py`/`browse.html`. | `tests/test_security.py` |
| F-15 | `sanitize_header_value` applied to mail `Subject`; recipients filtered through `is_valid_email`. | `tests/test_security.py` |
| F-19 | `common.write_error`: generic body + correlation id, `audit.log_server_error` server-side with traceback on 5xx; five handlers moved onto `TornadoRequestHandlerBase`. | `tests/test_audit.py` |
| F-21 | `plot_app/audit.py` `audit_log(event, outcome, **fields)` -> JSON line via `logging`; events: `upload` (success after the DB row is committed; failure with reason, including post-storage failures), `log_delete` (success/failure), `log_edit` (failure: malformed/mismatched token), `log_download` (private log; outcome recorded from `on_finish`/`on_connection_close` once the response completes). | `tests/test_audit.py` |

Run the tests with:

```bash
pip install pytest
pytest app/tests
```

## Documented, not remediated (not-satisfied)

- **F-10** token in URL query string: design change (POST/one-time link) needed; audit coverage added as a compensating measure.
- **F-14** Jinja2 autoescape disabled: enabling it requires deciding how to handle already HTML-escaped DB content.
- **F-25** container runs as root on a floating base tag; dev compose publishes the app port directly.
- **F-26** unpinned dependencies and no SCA in CI.
- **F-29** private (unlisted) logs are readable by anyone holding the UUID URL: an authenticated owner/reader model would be a design change to upload, plot, download and the shared links; audit coverage of private downloads added as a compensating measure.

## needs-input (evidence an ISSM/assessor must supply)

The following cannot be determined from the repository and are recorded as
`needs-input`; nothing below is assumed to be present or absent.

1. **TLS termination and policy at the reverse proxy (F-24, SC-8/SC-13, V-222596/V-222597).** Which `NGINX_CONF` profile is deployed; the content of `/etc/letsencrypt/options-ssl-nginx.conf` on the host (TLS versions, cipher suites); whether HTTP/80 is only used for ACME + redirect.
2. **HTTP security headers (F-24, CM-6).** Whether `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`/`frame-ancestors` and a CSP are added at the proxy or by another layer; none are set in this repository.
3. **Host and container hardening (F-25, CM-6/CM-7).** Host OS STIG posture, Docker daemon configuration, whether the container runs as a non-root user in production, file permissions on `data/` (SQLite DB, ULog files), and the network exposure of port 5006.
4. **Identity provider / administrative authentication (F-23, IA-2/IA-5/AC-3).** Whether nginx basic auth is in use, how `.htpasswd` credentials are managed, whether MFA is enforced in front of the application, and who may run `prune_old_logs.py` / `delete_db_entry.py`.
5. **Storage of the `.ulge` private key (F-06, SC-12/SC-13/SC-28).** Where `ulge_private_key` points in production, file ownership/permissions, whether the key is held in a secret store/HSM, and the rotation procedure.
6. **SMTP credentials (F-16, IA-5/SC-28).** Where `config_user.ini` `[email]` `user_name`/`password` are stored, permissions, whether SMTP uses STARTTLS/TLS to the configured server (the code uses `SMTP` + `starttls()`), and credential rotation.
7. **Audit record handling (F-21 deployment side, AU-4/AU-9/AU-11, V-222481/V-222482).** Where container stdout (the audit JSON lines) is collected, retention period, integrity protection and off-loading to a central log system.
8. **Backup and contingency planning (CP-9/CP-10, V-222636/V-222638).** Backup interval and restore testing for `data/` (SQLite DB and ULog storage), and the contingency plan for the service.
9. **Vulnerability management (F-26, RA-5/SI-2).** Whether dependency scanning (SCA) and image scanning run outside this repository's CI, and the patch cadence for the `ubuntu:noble` base image and Python packages.
10. **Provider-side token restrictions (F-18).** Whether the Mapbox / Cesium Ion tokens configured in production are URL/domain-restricted.

## Method

Manual source review of every handler and helper listed in Scope, repository-
wide search for path construction from `log_id`, SQL execution sites,
`escape(...)`/`safe` usage, `print(...)` on error paths, and outbound HTTP
calls; verification by `./run_pylint.sh` (10.00/10 before and after) and the
new `app/tests` suite. Dynamic testing (DAST) was not performed and is not
claimed.
