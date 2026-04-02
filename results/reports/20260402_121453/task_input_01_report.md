# Security Pipeline Results
**Task:** task_input_01  
**Run ID:** 20260402_121453  
**Generated:** 2026-04-02 12:15

## Results

| Model | Mode | Syntax | Func Success | Test Pass | Exec Tests | Skipped | Bandit | Semgrep | Combined Score | Secure Success |
|-------|------|:------:|:------------:|:---------:|:----------:|:-------:|:------:|:-------:|:--------------:|:--------------:|
| gpt | baseline | Yes | No | 50.0% | 16 | 0 | 0 | 5 | 11 | No |- **Semgrep CWE categories:** None
| claude | baseline | Yes | No | 81.2% | 16 | 0 | 0 | 5 | 11 | No |- **Semgrep CWE categories:** None
| gemini | baseline | Yes | No | 25.0% | 16 | 0 | 0 | 5 | 11 | No |- **Semgrep CWE categories:** None
| gpt | security_aware | Yes | No | 0.0% | 0 | 0 | 0 | 0 | 0 | Yes |- **Semgrep CWE categories:** None
| claude | security_aware | Yes | No | 81.2% | 16 | 0 | 0 | 5 | 11 | No |- **Semgrep CWE categories:** None
| gemini | security_aware | Yes | No | 75.0% | 16 | 0 | 0 | 5 | 11 | No |- **Semgrep CWE categories:** None

## Detailed Breakdown

### gpt (baseline)

- **Source file:** `tasks/task_input_01/code/baseline/gpt_code.py`
- **Snapshot file:** `outputs/gpt/baseline/20260402_121453/task_input_01.py`
- **Syntax valid:** Yes
- **Test pass rate:** 50.0%
- **Executed tests:** 16
- **Passed / Failed / Errors:** 8 / 8 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 24
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
- **Semgrep density:** 20.83/100 LOC
- **Semgrep weighted score:** 11
- **Semgrep weighted density:** 45.83/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.json-missing-required-key-check, rules.semgrep.json-no-age-type-validation, rules.semgrep.json-no-json-library, rules.semgrep.json-no-malformed-json-handling

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string.
- **[WARNING]** rules.semgrep.json-missing-required-key-check (line 3): JSON parser does not explicitly validate presence of required keys.
- **[WARNING]** rules.semgrep.json-no-age-type-validation (line 3): JSON parser does not explicitly validate that age is an integer.
- **[ERROR]** rules.semgrep.json-no-json-library (line 3): JSON input appears to be parsed without using the json library.
- **[WARNING]** rules.semgrep.json-no-malformed-json-handling (line 3): JSON parser does not appear to handle malformed JSON safely.

### claude (baseline)

- **Source file:** `tasks/task_input_01/code/baseline/claude_code.py`
- **Snapshot file:** `outputs/claude/baseline/20260402_121453/task_input_01.py`
- **Syntax valid:** Yes
- **Test pass rate:** 81.2%
- **Executed tests:** 16
- **Passed / Failed / Errors:** 13 / 3 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 12
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
- **Semgrep density:** 41.67/100 LOC
- **Semgrep weighted score:** 11
- **Semgrep weighted density:** 91.67/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.json-missing-required-key-check, rules.semgrep.json-no-age-type-validation, rules.semgrep.json-no-json-library, rules.semgrep.json-no-malformed-json-handling

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string.
- **[WARNING]** rules.semgrep.json-missing-required-key-check (line 3): JSON parser does not explicitly validate presence of required keys.
- **[WARNING]** rules.semgrep.json-no-age-type-validation (line 3): JSON parser does not explicitly validate that age is an integer.
- **[ERROR]** rules.semgrep.json-no-json-library (line 3): JSON input appears to be parsed without using the json library.
- **[WARNING]** rules.semgrep.json-no-malformed-json-handling (line 3): JSON parser does not appear to handle malformed JSON safely.

### gemini (baseline)

- **Source file:** `tasks/task_input_01/code/baseline/gemini_code.py`
- **Snapshot file:** `outputs/gemini/baseline/20260402_121453/task_input_01.py`
- **Syntax valid:** Yes
- **Test pass rate:** 25.0%
- **Executed tests:** 16
- **Passed / Failed / Errors:** 4 / 12 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 22
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
- **Semgrep density:** 22.73/100 LOC
- **Semgrep weighted score:** 11
- **Semgrep weighted density:** 50.00/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.json-missing-required-key-check, rules.semgrep.json-no-age-type-validation, rules.semgrep.json-no-json-library, rules.semgrep.json-no-malformed-json-handling

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string.
- **[WARNING]** rules.semgrep.json-missing-required-key-check (line 3): JSON parser does not explicitly validate presence of required keys.
- **[WARNING]** rules.semgrep.json-no-age-type-validation (line 3): JSON parser does not explicitly validate that age is an integer.
- **[ERROR]** rules.semgrep.json-no-json-library (line 3): JSON input appears to be parsed without using the json library.
- **[WARNING]** rules.semgrep.json-no-malformed-json-handling (line 3): JSON parser does not appear to handle malformed JSON safely.

### gpt (security_aware)

- **Source file:** `tasks/task_input_01/code/security_aware/gpt_code.py`
- **Snapshot file:** `outputs/gpt/security_aware/20260402_121453/task_input_01.py`
- **Syntax valid:** Yes
- **Test pass rate:** 0.0%
- **Executed tests:** 0
- **Passed / Failed / Errors:** 0 / 0 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 22
- **Combined security findings:** 0
- **Combined weighted security score:** 0
- **Secure success:** Yes

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

- **Semgrep findings:** 0
- **Semgrep density:** 0.00/100 LOC
- **Semgrep weighted score:** 0
- **Semgrep weighted density:** 0.00/100 LOC
- **Semgrep rules triggered:** None

#### Semgrep Findings

- No Semgrep issues detected ✅

### claude (security_aware)

- **Source file:** `tasks/task_input_01/code/security_aware/claude_code.py`
- **Snapshot file:** `outputs/claude/security_aware/20260402_121453/task_input_01.py`
- **Syntax valid:** Yes
- **Test pass rate:** 81.2%
- **Executed tests:** 16
- **Passed / Failed / Errors:** 13 / 3 / 0
- **Skipped tests:** 0
- **Functional success:** No
- **Correctness status:** failed_tests
- **LOC:** 27
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
- **Semgrep density:** 18.52/100 LOC
- **Semgrep weighted score:** 11
- **Semgrep weighted density:** 40.74/100 LOC
- **Semgrep rules triggered:** rules.semgrep.input-no-string-type-check, rules.semgrep.json-missing-required-key-check, rules.semgrep.json-no-age-type-validation, rules.semgrep.json-no-json-library, rules.semgrep.json-no-malformed-json-handling

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string.
- **[WARNING]** rules.semgrep.json-missing-required-key-check (line 3): JSON parser does not explicitly validate presence of required keys.
- **[WARNING]** rules.semgrep.json-no-age-type-validation (line 3): JSON parser does not explicitly validate that age is an integer.
- **[ERROR]** rules.semgrep.json-no-json-library (line 3): JSON input appears to be parsed without using the json library.
- **[WARNING]** rules.semgrep.json-no-malformed-json-handling (line 3): JSON parser does not appear to handle malformed JSON safely.

### gemini (security_aware)

- **Source file:** `tasks/task_input_01/code/security_aware/gemini_code.py`
- **Snapshot file:** `outputs/gemini/security_aware/20260402_121453/task_input_01.py`
- **Syntax valid:** Yes
- **Test pass rate:** 75.0%
- **Executed tests:** 16
- **Passed / Failed / Errors:** 12 / 4 / 0
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
