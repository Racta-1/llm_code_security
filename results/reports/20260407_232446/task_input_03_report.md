# Security Pipeline Results
**Task:** task_input_03  
**Run ID:** 20260407_232446  
**Generated:** 2026-04-07 23:26

## Results

| Model | Mode | Syntax | Func Success | Pass Rate | Security Score | Overall Score | Exec Tests | Skipped | Bandit | Semgrep | Combined Score |
|-------|------|:------:|:------------:|:---------:|:--------------:|:-------------:|:----------:|:-------:|:------:|:-------:|:--------------:|
| gpt | baseline | Yes | No | 60.0% | 100.0% | 80.0% | 15 | 0 | 0 | 0 | 0 |
| claude | baseline | Yes | No | 66.7% | 100.0% | 83.3% | 15 | 0 | 0 | 0 | 0 |
| gemini | baseline | Yes | No | 60.0% | 100.0% | 80.0% | 15 | 0 | 0 | 0 | 0 |
| gpt | security_aware | Yes | No | 93.3% | 100.0% | 96.7% | 15 | 0 | 0 | 0 | 0 |
| claude | security_aware | Yes | No | 93.3% | 100.0% | 96.7% | 15 | 0 | 0 | 0 | 0 |
| gemini | security_aware | Yes | No | 0.0% | 100.0% | 50.0% | 0 | 0 | 0 | 0 | 0 |

## Detailed Breakdown

### gpt (baseline)

- **Source file:** `tasks/task_input_03/code/baseline/gpt_code.py`
- **Snapshot file:** `outputs/gpt/baseline/20260407_232446/task_input_03.py`
- **Syntax valid:** Yes

#### Headline Scores

- **Pass Rate:** 60.0%
- **Security Score:** 100.0%
- **Overall Score:** 80.0%
- **Functional success:** No
- **Secure success:** Yes

#### Correctness Breakdown

- **Executed tests:** 15
- **Skipped tests:** 0
- **Passed / Failed / Errors:** 9 / 6 / 0
- **Correctness status:** failed_tests

#### Security Breakdown

- **Combined security findings:** 0
- **Combined weighted security score:** 0
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

- **Semgrep findings:** 0
- **Semgrep density:** 0.00/100 LOC
- **Semgrep weighted score:** 0
- **Semgrep weighted density:** 0.00/100 LOC
- **Semgrep rules triggered:** None
- **Semgrep CWE categories:** None

#### Semgrep Findings

- No Semgrep issues detected ✅

### claude (baseline)

- **Source file:** `tasks/task_input_03/code/baseline/claude_code.py`
- **Snapshot file:** `outputs/claude/baseline/20260407_232446/task_input_03.py`
- **Syntax valid:** Yes

#### Headline Scores

- **Pass Rate:** 66.7%
- **Security Score:** 100.0%
- **Overall Score:** 83.3%
- **Functional success:** No
- **Secure success:** Yes

#### Correctness Breakdown

- **Executed tests:** 15
- **Skipped tests:** 0
- **Passed / Failed / Errors:** 10 / 5 / 0
- **Correctness status:** failed_tests

#### Security Breakdown

- **Combined security findings:** 0
- **Combined weighted security score:** 0
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

- **Semgrep findings:** 0
- **Semgrep density:** 0.00/100 LOC
- **Semgrep weighted score:** 0
- **Semgrep weighted density:** 0.00/100 LOC
- **Semgrep rules triggered:** None
- **Semgrep CWE categories:** None

#### Semgrep Findings

- No Semgrep issues detected ✅

### gemini (baseline)

- **Source file:** `tasks/task_input_03/code/baseline/gemini_code.py`
- **Snapshot file:** `outputs/gemini/baseline/20260407_232446/task_input_03.py`
- **Syntax valid:** Yes

#### Headline Scores

- **Pass Rate:** 60.0%
- **Security Score:** 100.0%
- **Overall Score:** 80.0%
- **Functional success:** No
- **Secure success:** Yes

#### Correctness Breakdown

- **Executed tests:** 15
- **Skipped tests:** 0
- **Passed / Failed / Errors:** 9 / 6 / 0
- **Correctness status:** failed_tests

#### Security Breakdown

- **Combined security findings:** 0
- **Combined weighted security score:** 0
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

- **Semgrep findings:** 0
- **Semgrep density:** 0.00/100 LOC
- **Semgrep weighted score:** 0
- **Semgrep weighted density:** 0.00/100 LOC
- **Semgrep rules triggered:** None
- **Semgrep CWE categories:** None

#### Semgrep Findings

- No Semgrep issues detected ✅

### gpt (security_aware)

- **Source file:** `tasks/task_input_03/code/security_aware/gpt_code.py`
- **Snapshot file:** `outputs/gpt/security_aware/20260407_232446/task_input_03.py`
- **Syntax valid:** Yes

#### Headline Scores

- **Pass Rate:** 93.3%
- **Security Score:** 100.0%
- **Overall Score:** 96.7%
- **Functional success:** No
- **Secure success:** Yes

#### Correctness Breakdown

- **Executed tests:** 15
- **Skipped tests:** 0
- **Passed / Failed / Errors:** 14 / 1 / 0
- **Correctness status:** failed_tests

#### Security Breakdown

- **Combined security findings:** 0
- **Combined weighted security score:** 0
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

- **Semgrep findings:** 0
- **Semgrep density:** 0.00/100 LOC
- **Semgrep weighted score:** 0
- **Semgrep weighted density:** 0.00/100 LOC
- **Semgrep rules triggered:** None
- **Semgrep CWE categories:** None

#### Semgrep Findings

- No Semgrep issues detected ✅

### claude (security_aware)

- **Source file:** `tasks/task_input_03/code/security_aware/claude_code.py`
- **Snapshot file:** `outputs/claude/security_aware/20260407_232446/task_input_03.py`
- **Syntax valid:** Yes

#### Headline Scores

- **Pass Rate:** 93.3%
- **Security Score:** 100.0%
- **Overall Score:** 96.7%
- **Functional success:** No
- **Secure success:** Yes

#### Correctness Breakdown

- **Executed tests:** 15
- **Skipped tests:** 0
- **Passed / Failed / Errors:** 14 / 1 / 0
- **Correctness status:** failed_tests

#### Security Breakdown

- **Combined security findings:** 0
- **Combined weighted security score:** 0
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

- **Semgrep findings:** 0
- **Semgrep density:** 0.00/100 LOC
- **Semgrep weighted score:** 0
- **Semgrep weighted density:** 0.00/100 LOC
- **Semgrep rules triggered:** None
- **Semgrep CWE categories:** None

#### Semgrep Findings

- No Semgrep issues detected ✅

### gemini (security_aware)

- **Source file:** `tasks/task_input_03/code/security_aware/gemini_code.py`
- **Snapshot file:** `outputs/gemini/security_aware/20260407_232446/task_input_03.py`
- **Syntax valid:** Yes

#### Headline Scores

- **Pass Rate:** 0.0%
- **Security Score:** 100.0%
- **Overall Score:** 50.0%
- **Functional success:** No
- **Secure success:** Yes

#### Correctness Breakdown

- **Executed tests:** 0
- **Skipped tests:** 0
- **Passed / Failed / Errors:** 0 / 0 / 0
- **Correctness status:** failed_tests

#### Security Breakdown

- **Combined security findings:** 0
- **Combined weighted security score:** 0
- **LOC:** 18

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
