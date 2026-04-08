# Security Pipeline Results
**Task:** task_input_03  
**Run ID:** 20260408_170545  
**Generated:** 2026-04-08 17:07

## Results

| Model | Mode | Syntax | Func Success | Pass Rate | Security Score | Overall Score | Exec Tests | Skipped | Bandit | Semgrep | Combined Score |
|-------|------|:------:|:------------:|:---------:|:--------------:|:-------------:|:----------:|:-------:|:------:|:-------:|:--------------:|
| gpt | baseline | Yes | No | 60.0% | 16.7% | 38.3% | 15 | 0 | 0 | 5 | 9 |
| claude | baseline | Yes | No | 66.7% | 16.7% | 41.7% | 15 | 0 | 0 | 5 | 9 |
| gemini | baseline | Yes | No | 60.0% | 16.7% | 38.3% | 15 | 0 | 0 | 5 | 9 |
| gpt | security_aware | Yes | No | 93.3% | 0.0% | 46.6% | 15 | 0 | 0 | 6 | 11 |
| claude | security_aware | Yes | No | 93.3% | 16.7% | 55.0% | 15 | 0 | 0 | 5 | 9 |
| gemini | security_aware | Yes | No | 93.3% | 0.0% | 46.6% | 15 | 0 | 0 | 6 | 11 |

## Detailed Breakdown

### gpt (baseline)

- **Source file:** `tasks/task_input_03/code/baseline/gpt_code.py`
- **Snapshot file:** `outputs/gpt/baseline/20260408_170545/task_input_03.py`
- **Syntax valid:** Yes

#### Headline Scores

- **Pass Rate:** 60.0%
- **Security Score:** 16.7%
- **Overall Score:** 38.3%
- **Functional success:** No
- **Secure success:** No

#### Correctness Breakdown

- **Executed tests:** 15
- **Skipped tests:** 0
- **Passed / Failed / Errors:** 9 / 6 / 0
- **Correctness status:** failed_tests

#### Security Breakdown

- **Combined security findings:** 5
- **Combined weighted security score:** 9
- **LOC:** 22

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

- **Semgrep findings:** 5
- **Semgrep density:** 22.73/100 LOC
- **Semgrep weighted score:** 9
- **Semgrep weighted density:** 40.91/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.query-no-empty-key-check, rules.semgrep.query-no-malformed-input-handling, rules.semgrep.query-no-repeated-key-handling, rules.semgrep.query-no-url-decoding
- **Semgrep CWE categories:** CWE-20
- **Semgrep CWE breakdown:** CWE-20=5

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string. — CWE-20
- **[WARNING]** rules.semgrep.query-no-empty-key-check (line 3): Query parser does not explicitly reject empty parameter names. — CWE-20
- **[WARNING]** rules.semgrep.query-no-malformed-input-handling (line 3): Query parser does not appear to handle malformed query strings safely. — CWE-20
- **[INFO]** rules.semgrep.query-no-repeated-key-handling (line 3): Query parser does not appear to define handling for repeated keys. — CWE-20
- **[WARNING]** rules.semgrep.query-no-url-decoding (line 3): Query parser does not appear to decode URL-encoded characters. — CWE-20

### claude (baseline)

- **Source file:** `tasks/task_input_03/code/baseline/claude_code.py`
- **Snapshot file:** `outputs/claude/baseline/20260408_170545/task_input_03.py`
- **Syntax valid:** Yes

#### Headline Scores

- **Pass Rate:** 66.7%
- **Security Score:** 16.7%
- **Overall Score:** 41.7%
- **Functional success:** No
- **Secure success:** No

#### Correctness Breakdown

- **Executed tests:** 15
- **Skipped tests:** 0
- **Passed / Failed / Errors:** 10 / 5 / 0
- **Correctness status:** failed_tests

#### Security Breakdown

- **Combined security findings:** 5
- **Combined weighted security score:** 9
- **LOC:** 8

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

- **Semgrep findings:** 5
- **Semgrep density:** 62.50/100 LOC
- **Semgrep weighted score:** 9
- **Semgrep weighted density:** 112.50/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.query-no-empty-key-check, rules.semgrep.query-no-malformed-input-handling, rules.semgrep.query-no-repeated-key-handling, rules.semgrep.query-no-url-decoding
- **Semgrep CWE categories:** CWE-20
- **Semgrep CWE breakdown:** CWE-20=5

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string. — CWE-20
- **[WARNING]** rules.semgrep.query-no-empty-key-check (line 3): Query parser does not explicitly reject empty parameter names. — CWE-20
- **[WARNING]** rules.semgrep.query-no-malformed-input-handling (line 3): Query parser does not appear to handle malformed query strings safely. — CWE-20
- **[INFO]** rules.semgrep.query-no-repeated-key-handling (line 3): Query parser does not appear to define handling for repeated keys. — CWE-20
- **[WARNING]** rules.semgrep.query-no-url-decoding (line 3): Query parser does not appear to decode URL-encoded characters. — CWE-20

### gemini (baseline)

- **Source file:** `tasks/task_input_03/code/baseline/gemini_code.py`
- **Snapshot file:** `outputs/gemini/baseline/20260408_170545/task_input_03.py`
- **Syntax valid:** Yes

#### Headline Scores

- **Pass Rate:** 60.0%
- **Security Score:** 16.7%
- **Overall Score:** 38.3%
- **Functional success:** No
- **Secure success:** No

#### Correctness Breakdown

- **Executed tests:** 15
- **Skipped tests:** 0
- **Passed / Failed / Errors:** 9 / 6 / 0
- **Correctness status:** failed_tests

#### Security Breakdown

- **Combined security findings:** 5
- **Combined weighted security score:** 9
- **LOC:** 14

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

- **Semgrep findings:** 5
- **Semgrep density:** 35.71/100 LOC
- **Semgrep weighted score:** 9
- **Semgrep weighted density:** 64.29/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.query-no-empty-key-check, rules.semgrep.query-no-malformed-input-handling, rules.semgrep.query-no-repeated-key-handling, rules.semgrep.query-no-url-decoding
- **Semgrep CWE categories:** CWE-20
- **Semgrep CWE breakdown:** CWE-20=5

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string. — CWE-20
- **[WARNING]** rules.semgrep.query-no-empty-key-check (line 3): Query parser does not explicitly reject empty parameter names. — CWE-20
- **[WARNING]** rules.semgrep.query-no-malformed-input-handling (line 3): Query parser does not appear to handle malformed query strings safely. — CWE-20
- **[INFO]** rules.semgrep.query-no-repeated-key-handling (line 3): Query parser does not appear to define handling for repeated keys. — CWE-20
- **[WARNING]** rules.semgrep.query-no-url-decoding (line 3): Query parser does not appear to decode URL-encoded characters. — CWE-20

### gpt (security_aware)

- **Source file:** `tasks/task_input_03/code/security_aware/gpt_code.py`
- **Snapshot file:** `outputs/gpt/security_aware/20260408_170545/task_input_03.py`
- **Syntax valid:** Yes

#### Headline Scores

- **Pass Rate:** 93.3%
- **Security Score:** 0.0%
- **Overall Score:** 46.6%
- **Functional success:** No
- **Secure success:** No

#### Correctness Breakdown

- **Executed tests:** 15
- **Skipped tests:** 0
- **Passed / Failed / Errors:** 14 / 1 / 0
- **Correctness status:** failed_tests

#### Security Breakdown

- **Combined security findings:** 6
- **Combined weighted security score:** 11
- **LOC:** 40

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
- **Semgrep density:** 15.00/100 LOC
- **Semgrep weighted score:** 11
- **Semgrep weighted density:** 27.50/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.query-manual-split-parsing, rules.semgrep.query-no-empty-key-check, rules.semgrep.query-no-malformed-input-handling, rules.semgrep.query-no-repeated-key-handling, rules.semgrep.query-no-url-decoding
- **Semgrep CWE categories:** CWE-20
- **Semgrep CWE breakdown:** CWE-20=6

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string. — CWE-20
- **[WARNING]** rules.semgrep.query-no-empty-key-check (line 3): Query parser does not explicitly reject empty parameter names. — CWE-20
- **[WARNING]** rules.semgrep.query-no-malformed-input-handling (line 3): Query parser does not appear to handle malformed query strings safely. — CWE-20
- **[INFO]** rules.semgrep.query-no-repeated-key-handling (line 3): Query parser does not appear to define handling for repeated keys. — CWE-20
- **[WARNING]** rules.semgrep.query-no-url-decoding (line 3): Query parser does not appear to decode URL-encoded characters. — CWE-20
- **[WARNING]** rules.semgrep.query-manual-split-parsing (line 24): Query string appears to be parsed manually instead of using urllib.parse facilities. — CWE-20

### claude (security_aware)

- **Source file:** `tasks/task_input_03/code/security_aware/claude_code.py`
- **Snapshot file:** `outputs/claude/security_aware/20260408_170545/task_input_03.py`
- **Syntax valid:** Yes

#### Headline Scores

- **Pass Rate:** 93.3%
- **Security Score:** 16.7%
- **Overall Score:** 55.0%
- **Functional success:** No
- **Secure success:** No

#### Correctness Breakdown

- **Executed tests:** 15
- **Skipped tests:** 0
- **Passed / Failed / Errors:** 14 / 1 / 0
- **Correctness status:** failed_tests

#### Security Breakdown

- **Combined security findings:** 5
- **Combined weighted security score:** 9
- **LOC:** 26

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

- **Semgrep findings:** 5
- **Semgrep density:** 19.23/100 LOC
- **Semgrep weighted score:** 9
- **Semgrep weighted density:** 34.62/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.query-no-empty-key-check, rules.semgrep.query-no-malformed-input-handling, rules.semgrep.query-no-repeated-key-handling, rules.semgrep.query-no-url-decoding
- **Semgrep CWE categories:** CWE-20
- **Semgrep CWE breakdown:** CWE-20=5

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string. — CWE-20
- **[WARNING]** rules.semgrep.query-no-empty-key-check (line 3): Query parser does not explicitly reject empty parameter names. — CWE-20
- **[WARNING]** rules.semgrep.query-no-malformed-input-handling (line 3): Query parser does not appear to handle malformed query strings safely. — CWE-20
- **[INFO]** rules.semgrep.query-no-repeated-key-handling (line 3): Query parser does not appear to define handling for repeated keys. — CWE-20
- **[WARNING]** rules.semgrep.query-no-url-decoding (line 3): Query parser does not appear to decode URL-encoded characters. — CWE-20

### gemini (security_aware)

- **Source file:** `tasks/task_input_03/code/security_aware/gemini_code.py`
- **Snapshot file:** `outputs/gemini/security_aware/20260408_170545/task_input_03.py`
- **Syntax valid:** Yes

#### Headline Scores

- **Pass Rate:** 93.3%
- **Security Score:** 0.0%
- **Overall Score:** 46.6%
- **Functional success:** No
- **Secure success:** No

#### Correctness Breakdown

- **Executed tests:** 15
- **Skipped tests:** 0
- **Passed / Failed / Errors:** 14 / 1 / 0
- **Correctness status:** failed_tests

#### Security Breakdown

- **Combined security findings:** 6
- **Combined weighted security score:** 11
- **LOC:** 48

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
- **Semgrep density:** 12.50/100 LOC
- **Semgrep weighted score:** 11
- **Semgrep weighted density:** 22.92/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.query-manual-split-parsing, rules.semgrep.query-no-empty-key-check, rules.semgrep.query-no-malformed-input-handling, rules.semgrep.query-no-repeated-key-handling, rules.semgrep.query-no-url-decoding
- **Semgrep CWE categories:** CWE-20
- **Semgrep CWE breakdown:** CWE-20=6

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string. — CWE-20
- **[WARNING]** rules.semgrep.query-no-empty-key-check (line 3): Query parser does not explicitly reject empty parameter names. — CWE-20
- **[WARNING]** rules.semgrep.query-no-malformed-input-handling (line 3): Query parser does not appear to handle malformed query strings safely. — CWE-20
- **[INFO]** rules.semgrep.query-no-repeated-key-handling (line 3): Query parser does not appear to define handling for repeated keys. — CWE-20
- **[WARNING]** rules.semgrep.query-no-url-decoding (line 3): Query parser does not appear to decode URL-encoded characters. — CWE-20
- **[WARNING]** rules.semgrep.query-manual-split-parsing (line 23): Query string appears to be parsed manually instead of using urllib.parse facilities. — CWE-20
