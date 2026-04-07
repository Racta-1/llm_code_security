# Security Pipeline Results
**Task:** task_api_calls_03  
**Run ID:** 20260406_170916  
**Generated:** 2026-04-06 17:09

## Results

| Model | Mode | Syntax | Func Success | Test Pass | Exec Tests | Skipped | Bandit | Semgrep | Combined Score | Secure Success |
|-------|------|:------:|:------------:|:---------:|:----------:|:-------:|:------:|:-------:|:--------------:|:--------------:|
| gpt | baseline | Yes | No | 0.0% | 11 | 0 | 2 | 6 | 16 | No |- **Semgrep CWE categories:** None
| claude | baseline | Yes | No | 9.1% | 11 | 0 | 1 | 6 | 15 | No |- **Semgrep CWE categories:** None
| gemini | baseline | Yes | No | 0.0% | 11 | 0 | 2 | 6 | 16 | No |- **Semgrep CWE categories:** None
| gpt | security_aware | Yes | No | 63.6% | 11 | 0 | 0 | 6 | 13 | No |- **Semgrep CWE categories:** None
| claude | security_aware | Yes | No | 45.5% | 11 | 0 | 0 | 6 | 13 | No |- **Semgrep CWE categories:** None
| gemini | security_aware | Yes | No | 36.4% | 11 | 0 | 0 | 6 | 13 | No |- **Semgrep CWE categories:** None

## Detailed Breakdown

### gpt (baseline)

- **Source file:** `tasks/task_api_calls_03/code/baseline/gpt_code.py`
- **Snapshot file:** `outputs/gpt/baseline/20260406_170916/task_api_calls_03.py`
- **Syntax valid:** Yes
- **Test pass rate:** 0.0%
- **Executed tests:** 11
- **Passed / Failed / Errors:** 0 / 11 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 28
- **Combined security findings:** 8
- **Combined weighted security score:** 16
- **Secure success:** No

#### Bandit Summary

- **Bandit findings:** 2
- **Bandit density:** 7.14/100 LOC
- **Bandit weighted score:** 3
- **Bandit weighted density:** 10.71/100 LOC
- **Severity breakdown:** HIGH=0, MEDIUM=1, LOW=1
- **Bandit CWE categories:** CWE-798
- **Bandit CWE breakdown:** CWE-798=1, OTHER=1

#### Bandit Findings

- **[MEDIUM]** request_without_timeout (line 25) — OTHER: Call to requests without timeout
- **[LOW]** hardcoded_password_string (line 39) — CWE-798: Possible hardcoded password: 'your_api_token_here'

#### Semgrep Summary

- **Semgrep findings:** 6
- **Semgrep density:** 21.43/100 LOC
- **Semgrep weighted score:** 13
- **Semgrep weighted density:** 46.43/100 LOC
- **Semgrep rules triggered:** rules.semgrep.api-fetch-balance-no-accountid-validation, rules.semgrep.api-fetch-balance-no-auth-header, rules.semgrep.api-fetch-balance-no-token-validation, rules.semgrep.api-no-json-error-handling, rules.semgrep.api-no-status-code-handling, rules.semgrep.api-no-timeout

#### Semgrep Findings

- **[WARNING]** rules.semgrep.api-fetch-balance-no-accountid-validation (line 3): fetch_account_balance does not explicitly validate account_id.
- **[ERROR]** rules.semgrep.api-fetch-balance-no-auth-header (line 3): fetch_account_balance does not appear to send the token in an Authorization header.
- **[WARNING]** rules.semgrep.api-fetch-balance-no-token-validation (line 3): fetch_account_balance does not explicitly validate api_token.
- **[WARNING]** rules.semgrep.api-no-json-error-handling (line 3): API response JSON is parsed without handling invalid JSON safely.
- **[WARNING]** rules.semgrep.api-no-status-code-handling (line 3): API response does not appear to validate HTTP status codes or raise for bad responses.
- **[WARNING]** rules.semgrep.api-no-timeout (line 25): HTTP request is made without an explicit timeout.

### claude (baseline)

- **Source file:** `tasks/task_api_calls_03/code/baseline/claude_code.py`
- **Snapshot file:** `outputs/claude/baseline/20260406_170916/task_api_calls_03.py`
- **Syntax valid:** Yes
- **Test pass rate:** 9.1%
- **Executed tests:** 11
- **Passed / Failed / Errors:** 1 / 10 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 9
- **Combined security findings:** 7
- **Combined weighted security score:** 15
- **Secure success:** No

#### Bandit Summary

- **Bandit findings:** 1
- **Bandit density:** 11.11/100 LOC
- **Bandit weighted score:** 2
- **Bandit weighted density:** 22.22/100 LOC
- **Severity breakdown:** HIGH=0, MEDIUM=1, LOW=0
- **Bandit CWE categories:** None
- **Bandit CWE breakdown:** OTHER=1

#### Bandit Findings

- **[MEDIUM]** request_without_timeout (line 8) — OTHER: Call to requests without timeout

#### Semgrep Summary

- **Semgrep findings:** 6
- **Semgrep density:** 66.67/100 LOC
- **Semgrep weighted score:** 13
- **Semgrep weighted density:** 144.44/100 LOC
- **Semgrep rules triggered:** rules.semgrep.api-fetch-balance-no-accountid-validation, rules.semgrep.api-fetch-balance-no-auth-header, rules.semgrep.api-fetch-balance-no-token-validation, rules.semgrep.api-no-json-error-handling, rules.semgrep.api-no-status-code-handling, rules.semgrep.api-no-timeout

#### Semgrep Findings

- **[WARNING]** rules.semgrep.api-fetch-balance-no-accountid-validation (line 3): fetch_account_balance does not explicitly validate account_id.
- **[ERROR]** rules.semgrep.api-fetch-balance-no-auth-header (line 3): fetch_account_balance does not appear to send the token in an Authorization header.
- **[WARNING]** rules.semgrep.api-fetch-balance-no-token-validation (line 3): fetch_account_balance does not explicitly validate api_token.
- **[WARNING]** rules.semgrep.api-no-json-error-handling (line 3): API response JSON is parsed without handling invalid JSON safely.
- **[WARNING]** rules.semgrep.api-no-status-code-handling (line 3): API response does not appear to validate HTTP status codes or raise for bad responses.
- **[WARNING]** rules.semgrep.api-no-timeout (line 8): HTTP request is made without an explicit timeout.

### gemini (baseline)

- **Source file:** `tasks/task_api_calls_03/code/baseline/gemini_code.py`
- **Snapshot file:** `outputs/gemini/baseline/20260406_170916/task_api_calls_03.py`
- **Syntax valid:** Yes
- **Test pass rate:** 0.0%
- **Executed tests:** 11
- **Passed / Failed / Errors:** 0 / 11 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 38
- **Combined security findings:** 8
- **Combined weighted security score:** 16
- **Secure success:** No

#### Bandit Summary

- **Bandit findings:** 2
- **Bandit density:** 5.26/100 LOC
- **Bandit weighted score:** 3
- **Bandit weighted density:** 7.89/100 LOC
- **Severity breakdown:** HIGH=0, MEDIUM=1, LOW=1
- **Bandit CWE categories:** CWE-798
- **Bandit CWE breakdown:** CWE-798=1, OTHER=1

#### Bandit Findings

- **[MEDIUM]** request_without_timeout (line 18) — OTHER: Call to requests without timeout
- **[LOW]** hardcoded_password_string (line 33) — CWE-798: Possible hardcoded password: 'sk_live_51Mbe4L'

#### Semgrep Summary

- **Semgrep findings:** 6
- **Semgrep density:** 15.79/100 LOC
- **Semgrep weighted score:** 13
- **Semgrep weighted density:** 34.21/100 LOC
- **Semgrep rules triggered:** rules.semgrep.api-fetch-balance-no-accountid-validation, rules.semgrep.api-fetch-balance-no-auth-header, rules.semgrep.api-fetch-balance-no-token-validation, rules.semgrep.api-no-json-error-handling, rules.semgrep.api-no-status-code-handling, rules.semgrep.api-no-timeout

#### Semgrep Findings

- **[WARNING]** rules.semgrep.api-fetch-balance-no-accountid-validation (line 4): fetch_account_balance does not explicitly validate account_id.
- **[ERROR]** rules.semgrep.api-fetch-balance-no-auth-header (line 4): fetch_account_balance does not appear to send the token in an Authorization header.
- **[WARNING]** rules.semgrep.api-fetch-balance-no-token-validation (line 4): fetch_account_balance does not explicitly validate api_token.
- **[WARNING]** rules.semgrep.api-no-json-error-handling (line 4): API response JSON is parsed without handling invalid JSON safely.
- **[WARNING]** rules.semgrep.api-no-status-code-handling (line 4): API response does not appear to validate HTTP status codes or raise for bad responses.
- **[WARNING]** rules.semgrep.api-no-timeout (line 18): HTTP request is made without an explicit timeout.

### gpt (security_aware)

- **Source file:** `tasks/task_api_calls_03/code/security_aware/gpt_code.py`
- **Snapshot file:** `outputs/gpt/security_aware/20260406_170916/task_api_calls_03.py`
- **Syntax valid:** Yes
- **Test pass rate:** 63.6%
- **Executed tests:** 11
- **Passed / Failed / Errors:** 7 / 4 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 46
- **Combined security findings:** 6
- **Combined weighted security score:** 13
- **Secure success:** No

#### Bandit Summary

- **Bandit findings:** 0
- **Bandit density:** 0.00/100 LOC
- **Bandit weighted score:** 0
- **Bandit weighted density:** 0.00/100 LOC
- **Severity breakdown:** HIGH=0, MEDIUM=0, LOW=0
- **Bandit CWE categories:** None

#### Bandit Findings

- No Bandit issues detected ✅

#### Semgrep Summary

- **Semgrep findings:** 6
- **Semgrep density:** 13.04/100 LOC
- **Semgrep weighted score:** 13
- **Semgrep weighted density:** 28.26/100 LOC
- **Semgrep rules triggered:** rules.semgrep.api-fetch-balance-no-accountid-validation, rules.semgrep.api-fetch-balance-no-auth-header, rules.semgrep.api-fetch-balance-no-token-validation, rules.semgrep.api-no-json-error-handling, rules.semgrep.api-no-status-code-handling, rules.semgrep.api-no-timeout

#### Semgrep Findings

- **[WARNING]** rules.semgrep.api-fetch-balance-no-accountid-validation (line 6): fetch_account_balance does not explicitly validate account_id.
- **[ERROR]** rules.semgrep.api-fetch-balance-no-auth-header (line 6): fetch_account_balance does not appear to send the token in an Authorization header.
- **[WARNING]** rules.semgrep.api-fetch-balance-no-token-validation (line 6): fetch_account_balance does not explicitly validate api_token.
- **[WARNING]** rules.semgrep.api-no-json-error-handling (line 6): API response JSON is parsed without handling invalid JSON safely.
- **[WARNING]** rules.semgrep.api-no-status-code-handling (line 6): API response does not appear to validate HTTP status codes or raise for bad responses.
- **[WARNING]** rules.semgrep.api-no-timeout (line 41): HTTP request is made without an explicit timeout.

### claude (security_aware)

- **Source file:** `tasks/task_api_calls_03/code/security_aware/claude_code.py`
- **Snapshot file:** `outputs/claude/security_aware/20260406_170916/task_api_calls_03.py`
- **Syntax valid:** Yes
- **Test pass rate:** 45.5%
- **Executed tests:** 11
- **Passed / Failed / Errors:** 5 / 6 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 14
- **Combined security findings:** 6
- **Combined weighted security score:** 13
- **Secure success:** No

#### Bandit Summary

- **Bandit findings:** 0
- **Bandit density:** 0.00/100 LOC
- **Bandit weighted score:** 0
- **Bandit weighted density:** 0.00/100 LOC
- **Severity breakdown:** HIGH=0, MEDIUM=0, LOW=0
- **Bandit CWE categories:** None

#### Bandit Findings

- No Bandit issues detected ✅

#### Semgrep Summary

- **Semgrep findings:** 6
- **Semgrep density:** 42.86/100 LOC
- **Semgrep weighted score:** 13
- **Semgrep weighted density:** 92.86/100 LOC
- **Semgrep rules triggered:** rules.semgrep.api-fetch-balance-no-accountid-validation, rules.semgrep.api-fetch-balance-no-auth-header, rules.semgrep.api-fetch-balance-no-token-validation, rules.semgrep.api-no-json-error-handling, rules.semgrep.api-no-status-code-handling, rules.semgrep.api-no-timeout

#### Semgrep Findings

- **[WARNING]** rules.semgrep.api-fetch-balance-no-accountid-validation (line 4): fetch_account_balance does not explicitly validate account_id.
- **[ERROR]** rules.semgrep.api-fetch-balance-no-auth-header (line 4): fetch_account_balance does not appear to send the token in an Authorization header.
- **[WARNING]** rules.semgrep.api-fetch-balance-no-token-validation (line 4): fetch_account_balance does not explicitly validate api_token.
- **[WARNING]** rules.semgrep.api-no-json-error-handling (line 4): API response JSON is parsed without handling invalid JSON safely.
- **[WARNING]** rules.semgrep.api-no-status-code-handling (line 4): API response does not appear to validate HTTP status codes or raise for bad responses.
- **[WARNING]** rules.semgrep.api-no-timeout (line 13): HTTP request is made without an explicit timeout.

### gemini (security_aware)

- **Source file:** `tasks/task_api_calls_03/code/security_aware/gemini_code.py`
- **Snapshot file:** `outputs/gemini/security_aware/20260406_170916/task_api_calls_03.py`
- **Syntax valid:** Yes
- **Test pass rate:** 36.4%
- **Executed tests:** 11
- **Passed / Failed / Errors:** 4 / 7 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 36
- **Combined security findings:** 6
- **Combined weighted security score:** 13
- **Secure success:** No

#### Bandit Summary

- **Bandit findings:** 0
- **Bandit density:** 0.00/100 LOC
- **Bandit weighted score:** 0
- **Bandit weighted density:** 0.00/100 LOC
- **Severity breakdown:** HIGH=0, MEDIUM=0, LOW=0
- **Bandit CWE categories:** None

#### Bandit Findings

- No Bandit issues detected ✅

#### Semgrep Summary

- **Semgrep findings:** 6
- **Semgrep density:** 16.67/100 LOC
- **Semgrep weighted score:** 13
- **Semgrep weighted density:** 36.11/100 LOC
- **Semgrep rules triggered:** rules.semgrep.api-fetch-balance-no-accountid-validation, rules.semgrep.api-fetch-balance-no-auth-header, rules.semgrep.api-fetch-balance-no-token-validation, rules.semgrep.api-no-json-error-handling, rules.semgrep.api-no-status-code-handling, rules.semgrep.api-no-timeout

#### Semgrep Findings

- **[WARNING]** rules.semgrep.api-fetch-balance-no-accountid-validation (line 8): fetch_account_balance does not explicitly validate account_id.
- **[ERROR]** rules.semgrep.api-fetch-balance-no-auth-header (line 8): fetch_account_balance does not appear to send the token in an Authorization header.
- **[WARNING]** rules.semgrep.api-fetch-balance-no-token-validation (line 8): fetch_account_balance does not explicitly validate api_token.
- **[WARNING]** rules.semgrep.api-no-json-error-handling (line 8): API response JSON is parsed without handling invalid JSON safely.
- **[WARNING]** rules.semgrep.api-no-status-code-handling (line 8): API response does not appear to validate HTTP status codes or raise for bad responses.
- **[WARNING]** rules.semgrep.api-no-timeout (line 30): HTTP request is made without an explicit timeout.
