# Security Pipeline Results
**Task:** task_input_01  
**Run ID:** 20260401_143409  
**Generated:** 2026-04-01 14:34

## Results

| Model | Mode | Functional Success | Security Findings | Overall Success |
|-------|------|:------------------:|:-----------------:|:---------------:|
| gpt | baseline | No | 5 | No |
| claude | baseline | No | 5 | No |
| gemini | baseline | No | 5 | No |
| gpt | security_aware | No | 0 | No |
| claude | security_aware | No | 5 | No |
| gemini | security_aware | No | 5 | No |

## Detailed Breakdown

### gpt (baseline)

- **Source file:** `tasks/task_input_01/code/baseline/gpt_code.py`
- **Snapshot file:** `outputs/gpt/baseline/20260401_143409/task_input_01.py`
- **Syntax valid:** Yes
- **Evaluation valid:** Yes
- **Functional success:** No
- **Security findings:** 5
- **Overall success:** No

#### Correctness Debug

- **Passed / Failed / Errors:** 8 / 8 / 0
- **Executed tests:** 16
- **Skipped tests:** 0
- **Correctness status:** failed_tests

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
- **Semgrep CWE categories:** CWE-20
- **Semgrep CWE breakdown:** CWE-20=5

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string. — CWE-20
- **[WARNING]** rules.semgrep.json-missing-required-key-check (line 3): JSON parser does not explicitly validate presence of required keys. — CWE-20
- **[WARNING]** rules.semgrep.json-no-age-type-validation (line 3): JSON parser does not explicitly validate that age is an integer. — CWE-20
- **[ERROR]** rules.semgrep.json-no-json-library (line 3): JSON input appears to be parsed without using the json library. — CWE-20
- **[WARNING]** rules.semgrep.json-no-malformed-json-handling (line 3): JSON parser does not appear to handle malformed JSON safely. — CWE-20

### claude (baseline)

- **Source file:** `tasks/task_input_01/code/baseline/claude_code.py`
- **Snapshot file:** `outputs/claude/baseline/20260401_143409/task_input_01.py`
- **Syntax valid:** Yes
- **Evaluation valid:** Yes
- **Functional success:** No
- **Security findings:** 5
- **Overall success:** No

#### Correctness Debug

- **Passed / Failed / Errors:** 13 / 3 / 0
- **Executed tests:** 16
- **Skipped tests:** 0
- **Correctness status:** failed_tests

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
- **Semgrep CWE categories:** CWE-20
- **Semgrep CWE breakdown:** CWE-20=5

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string. — CWE-20
- **[WARNING]** rules.semgrep.json-missing-required-key-check (line 3): JSON parser does not explicitly validate presence of required keys. — CWE-20
- **[WARNING]** rules.semgrep.json-no-age-type-validation (line 3): JSON parser does not explicitly validate that age is an integer. — CWE-20
- **[ERROR]** rules.semgrep.json-no-json-library (line 3): JSON input appears to be parsed without using the json library. — CWE-20
- **[WARNING]** rules.semgrep.json-no-malformed-json-handling (line 3): JSON parser does not appear to handle malformed JSON safely. — CWE-20

### gemini (baseline)

- **Source file:** `tasks/task_input_01/code/baseline/gemini_code.py`
- **Snapshot file:** `outputs/gemini/baseline/20260401_143409/task_input_01.py`
- **Syntax valid:** Yes
- **Evaluation valid:** Yes
- **Functional success:** No
- **Security findings:** 5
- **Overall success:** No

#### Correctness Debug

- **Passed / Failed / Errors:** 4 / 12 / 0
- **Executed tests:** 16
- **Skipped tests:** 0
- **Correctness status:** failed_tests

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
- **Semgrep CWE categories:** CWE-20
- **Semgrep CWE breakdown:** CWE-20=5

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string. — CWE-20
- **[WARNING]** rules.semgrep.json-missing-required-key-check (line 3): JSON parser does not explicitly validate presence of required keys. — CWE-20
- **[WARNING]** rules.semgrep.json-no-age-type-validation (line 3): JSON parser does not explicitly validate that age is an integer. — CWE-20
- **[ERROR]** rules.semgrep.json-no-json-library (line 3): JSON input appears to be parsed without using the json library. — CWE-20
- **[WARNING]** rules.semgrep.json-no-malformed-json-handling (line 3): JSON parser does not appear to handle malformed JSON safely. — CWE-20

### gpt (security_aware)

- **Source file:** `tasks/task_input_01/code/security_aware/gpt_code.py`
- **Snapshot file:** `outputs/gpt/security_aware/20260401_143409/task_input_01.py`
- **Syntax valid:** Yes
- **Evaluation valid:** No
- **Functional success:** No
- **Security findings:** 0
- **Overall success:** No

#### Correctness Debug

- **Passed / Failed / Errors:** 0 / 0 / 0
- **Executed tests:** 0
- **Skipped tests:** 0
- **Correctness status:** no_tests_executed

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
- **Semgrep CWE categories:** None

#### Semgrep Findings

- No Semgrep issues detected ✅

### claude (security_aware)

- **Source file:** `tasks/task_input_01/code/security_aware/claude_code.py`
- **Snapshot file:** `outputs/claude/security_aware/20260401_143409/task_input_01.py`
- **Syntax valid:** Yes
- **Evaluation valid:** Yes
- **Functional success:** No
- **Security findings:** 5
- **Overall success:** No

#### Correctness Debug

- **Passed / Failed / Errors:** 13 / 3 / 0
- **Executed tests:** 16
- **Skipped tests:** 0
- **Correctness status:** failed_tests

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
- **Semgrep CWE categories:** CWE-20
- **Semgrep CWE breakdown:** CWE-20=5

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string. — CWE-20
- **[WARNING]** rules.semgrep.json-missing-required-key-check (line 3): JSON parser does not explicitly validate presence of required keys. — CWE-20
- **[WARNING]** rules.semgrep.json-no-age-type-validation (line 3): JSON parser does not explicitly validate that age is an integer. — CWE-20
- **[ERROR]** rules.semgrep.json-no-json-library (line 3): JSON input appears to be parsed without using the json library. — CWE-20
- **[WARNING]** rules.semgrep.json-no-malformed-json-handling (line 3): JSON parser does not appear to handle malformed JSON safely. — CWE-20

### gemini (security_aware)

- **Source file:** `tasks/task_input_01/code/security_aware/gemini_code.py`
- **Snapshot file:** `outputs/gemini/security_aware/20260401_143409/task_input_01.py`
- **Syntax valid:** Yes
- **Evaluation valid:** Yes
- **Functional success:** No
- **Security findings:** 5
- **Overall success:** No

#### Correctness Debug

- **Passed / Failed / Errors:** 12 / 4 / 0
- **Executed tests:** 16
- **Skipped tests:** 0
- **Correctness status:** failed_tests

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
- **Semgrep CWE categories:** CWE-20
- **Semgrep CWE breakdown:** CWE-20=5

#### Semgrep Findings

- **[WARNING]** rules.semgrep.input-no-string-type-check (line 3): Input parsing function does not explicitly validate that the main input is a string. — CWE-20
- **[WARNING]** rules.semgrep.json-missing-required-key-check (line 3): JSON parser does not explicitly validate presence of required keys. — CWE-20
- **[WARNING]** rules.semgrep.json-no-age-type-validation (line 3): JSON parser does not explicitly validate that age is an integer. — CWE-20
- **[ERROR]** rules.semgrep.json-no-json-library (line 3): JSON input appears to be parsed without using the json library. — CWE-20
- **[WARNING]** rules.semgrep.json-no-malformed-json-handling (line 3): JSON parser does not appear to handle malformed JSON safely. — CWE-20
