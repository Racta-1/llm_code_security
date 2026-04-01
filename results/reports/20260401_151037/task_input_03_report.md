# Security Pipeline Results
**Task:** task_input_03  
**Run ID:** 20260401_151037  
**Generated:** 2026-04-01 15:10

## Results

| Model | Mode | Syntax | Func Success | Test Pass | Exec Tests | Skipped | Bandit | Semgrep | Combined Score | Secure Success |
|-------|------|:------:|:------------:|:---------:|:----------:|:-------:|:------:|:-------:|:--------------:|:--------------:|
| gpt | baseline | Yes | No | 66.7% | 15 | 0 | 0 | 5 | 9 | No |- **Semgrep CWE categories:** None
| claude | baseline | Yes | No | 73.3% | 15 | 0 | 0 | 5 | 9 | No |- **Semgrep CWE categories:** None
| gemini | baseline | Yes | No | 66.7% | 15 | 0 | 0 | 5 | 9 | No |- **Semgrep CWE categories:** None
| gpt | security_aware | Yes | No | 93.3% | 15 | 0 | 0 | 6 | 11 | No |- **Semgrep CWE categories:** None
| claude | security_aware | Yes | No | 93.3% | 15 | 0 | 0 | 5 | 9 | No |- **Semgrep CWE categories:** None
| gemini | security_aware | Yes | No | 0.0% | 0 | 0 | 0 | 5 | 11 | No |- **Semgrep CWE categories:** None

## Detailed Breakdown

### gpt (baseline)

- **Source file:** `tasks/task_input_03/code/baseline/gpt_code.py`
- **Snapshot file:** `outputs/gpt/baseline/20260401_151037/task_input_03.py`
- **Syntax valid:** Yes
- **Test pass rate:** 66.7%
- **Executed tests:** 15
- **Passed / Failed / Errors:** 10 / 5 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 22
- **Combined security findings:** 5
- **Combined weighted security score:** 9
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

- **Semgrep findings:** 5
- **Semgrep density:** 22.73/100 LOC
- **Semgrep weighted score:** 9
- **Semgrep weighted density:** 40.91/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.query-no-empty-key-check, rules.semgrep.query-no-malformed-input-handling, rules.semgrep.query-no-repeated-key-handling, rules.semgrep.query-no-url-decoding

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string.
- **[WARNING]** rules.semgrep.query-no-empty-key-check (line 3): Query parser does not explicitly reject empty parameter names.
- **[WARNING]** rules.semgrep.query-no-malformed-input-handling (line 3): Query parser does not appear to handle malformed query strings safely.
- **[INFO]** rules.semgrep.query-no-repeated-key-handling (line 3): Query parser does not appear to define handling for repeated keys.
- **[WARNING]** rules.semgrep.query-no-url-decoding (line 3): Query parser does not appear to decode URL-encoded characters.

### claude (baseline)

- **Source file:** `tasks/task_input_03/code/baseline/claude_code.py`
- **Snapshot file:** `outputs/claude/baseline/20260401_151037/task_input_03.py`
- **Syntax valid:** Yes
- **Test pass rate:** 73.3%
- **Executed tests:** 15
- **Passed / Failed / Errors:** 11 / 4 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 8
- **Combined security findings:** 5
- **Combined weighted security score:** 9
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

- **Semgrep findings:** 5
- **Semgrep density:** 62.50/100 LOC
- **Semgrep weighted score:** 9
- **Semgrep weighted density:** 112.50/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.query-no-empty-key-check, rules.semgrep.query-no-malformed-input-handling, rules.semgrep.query-no-repeated-key-handling, rules.semgrep.query-no-url-decoding

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string.
- **[WARNING]** rules.semgrep.query-no-empty-key-check (line 3): Query parser does not explicitly reject empty parameter names.
- **[WARNING]** rules.semgrep.query-no-malformed-input-handling (line 3): Query parser does not appear to handle malformed query strings safely.
- **[INFO]** rules.semgrep.query-no-repeated-key-handling (line 3): Query parser does not appear to define handling for repeated keys.
- **[WARNING]** rules.semgrep.query-no-url-decoding (line 3): Query parser does not appear to decode URL-encoded characters.

### gemini (baseline)

- **Source file:** `tasks/task_input_03/code/baseline/gemini_code.py`
- **Snapshot file:** `outputs/gemini/baseline/20260401_151037/task_input_03.py`
- **Syntax valid:** Yes
- **Test pass rate:** 66.7%
- **Executed tests:** 15
- **Passed / Failed / Errors:** 10 / 5 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 14
- **Combined security findings:** 5
- **Combined weighted security score:** 9
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

- **Semgrep findings:** 5
- **Semgrep density:** 35.71/100 LOC
- **Semgrep weighted score:** 9
- **Semgrep weighted density:** 64.29/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.query-no-empty-key-check, rules.semgrep.query-no-malformed-input-handling, rules.semgrep.query-no-repeated-key-handling, rules.semgrep.query-no-url-decoding

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string.
- **[WARNING]** rules.semgrep.query-no-empty-key-check (line 3): Query parser does not explicitly reject empty parameter names.
- **[WARNING]** rules.semgrep.query-no-malformed-input-handling (line 3): Query parser does not appear to handle malformed query strings safely.
- **[INFO]** rules.semgrep.query-no-repeated-key-handling (line 3): Query parser does not appear to define handling for repeated keys.
- **[WARNING]** rules.semgrep.query-no-url-decoding (line 3): Query parser does not appear to decode URL-encoded characters.

### gpt (security_aware)

- **Source file:** `tasks/task_input_03/code/security_aware/gpt_code.py`
- **Snapshot file:** `outputs/gpt/security_aware/20260401_151037/task_input_03.py`
- **Syntax valid:** Yes
- **Test pass rate:** 93.3%
- **Executed tests:** 15
- **Passed / Failed / Errors:** 14 / 1 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 40
- **Combined security findings:** 6
- **Combined weighted security score:** 11
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
- **Semgrep density:** 15.00/100 LOC
- **Semgrep weighted score:** 11
- **Semgrep weighted density:** 27.50/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.query-manual-split-parsing, rules.semgrep.query-no-empty-key-check, rules.semgrep.query-no-malformed-input-handling, rules.semgrep.query-no-repeated-key-handling, rules.semgrep.query-no-url-decoding

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string.
- **[WARNING]** rules.semgrep.query-no-empty-key-check (line 3): Query parser does not explicitly reject empty parameter names.
- **[WARNING]** rules.semgrep.query-no-malformed-input-handling (line 3): Query parser does not appear to handle malformed query strings safely.
- **[INFO]** rules.semgrep.query-no-repeated-key-handling (line 3): Query parser does not appear to define handling for repeated keys.
- **[WARNING]** rules.semgrep.query-no-url-decoding (line 3): Query parser does not appear to decode URL-encoded characters.
- **[WARNING]** rules.semgrep.query-manual-split-parsing (line 24): Query string appears to be parsed manually instead of using urllib.parse facilities.

### claude (security_aware)

- **Source file:** `tasks/task_input_03/code/security_aware/claude_code.py`
- **Snapshot file:** `outputs/claude/security_aware/20260401_151037/task_input_03.py`
- **Syntax valid:** Yes
- **Test pass rate:** 93.3%
- **Executed tests:** 15
- **Passed / Failed / Errors:** 14 / 1 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 26
- **Combined security findings:** 5
- **Combined weighted security score:** 9
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

- **Semgrep findings:** 5
- **Semgrep density:** 19.23/100 LOC
- **Semgrep weighted score:** 9
- **Semgrep weighted density:** 34.62/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.query-no-empty-key-check, rules.semgrep.query-no-malformed-input-handling, rules.semgrep.query-no-repeated-key-handling, rules.semgrep.query-no-url-decoding

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string.
- **[WARNING]** rules.semgrep.query-no-empty-key-check (line 3): Query parser does not explicitly reject empty parameter names.
- **[WARNING]** rules.semgrep.query-no-malformed-input-handling (line 3): Query parser does not appear to handle malformed query strings safely.
- **[INFO]** rules.semgrep.query-no-repeated-key-handling (line 3): Query parser does not appear to define handling for repeated keys.
- **[WARNING]** rules.semgrep.query-no-url-decoding (line 3): Query parser does not appear to decode URL-encoded characters.

### gemini (security_aware)

- **Source file:** `tasks/task_input_03/code/security_aware/gemini_code.py`
- **Snapshot file:** `outputs/gemini/security_aware/20260401_151037/task_input_03.py`
- **Syntax valid:** Yes
- **Test pass rate:** 0.0%
- **Executed tests:** 0
- **Passed / Failed / Errors:** 0 / 0 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 18
- **Combined security findings:** 5
- **Combined weighted security score:** 11
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

- **Semgrep findings:** 5
- **Semgrep density:** 27.78/100 LOC
- **Semgrep weighted score:** 11
- **Semgrep weighted density:** 61.11/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.json-missing-required-key-check, rules.semgrep.json-no-age-type-validation, rules.semgrep.json-no-json-library, rules.semgrep.json-no-malformed-json-handling

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string.
- **[WARNING]** rules.semgrep.json-missing-required-key-check (line 3): JSON parser does not explicitly validate presence of required keys.
- **[WARNING]** rules.semgrep.json-no-age-type-validation (line 3): JSON parser does not explicitly validate that age is an integer.
- **[ERROR]** rules.semgrep.json-no-json-library (line 3): JSON input appears to be parsed without using the json library.
- **[WARNING]** rules.semgrep.json-no-malformed-json-handling (line 3): JSON parser does not appear to handle malformed JSON safely.
