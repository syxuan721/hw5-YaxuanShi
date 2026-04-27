# Assignment Submission Checker

This repository contains my Week 5 reusable skill: **Assignment Submission Checker**.

## What the skill does
This skill checks whether a course assignment submission folder is ready to upload. It focuses on **submission packaging and completeness**, not on grading or content quality.

The skill can check:
- whether required files and folders exist
- whether required deliverables are non-empty
- whether required filename patterns are present
- whether placeholder-style filenames such as `draft` or `temp` appear
- whether required text patterns appear in a file such as `README.md`

This makes the skill useful as a narrow pre-submission check before a student uploads an assignment.

## Why I chose it
I chose this skill because it fits the Week 5 requirement that the task should **genuinely require a script**.

A model can explain submission rules, but it should not guess whether a real file exists, whether a required file is empty, or whether a README actually contains a required link or keyword. Those are deterministic checks, so they are better handled by Python.

I also chose this topic because it is narrow, realistic, and reusable. A student could reuse the same skill for multiple class projects by changing the manifest of required checks.

## How to use it
The skill lives in:

```text
.agents/skills/assignment-submission-checker/
```

To use it:
1. prepare a submission folder to inspect
2. prepare a manifest JSON file that defines the required checks
3. run the Python script with the submission folder path and manifest path

Example command:
```text
python .agents/skills/assignment-submission-checker/scripts/check_submission.py examples/pass_case .agents/skills/assignment-submission-checker/assets/example_manifest.json
```

The script returns structured JSON with:
- an overall status
- counts of failures and warnings
- detailed check results

The skill is intended for packaging checks only. It should be used when the user wants to verify submission-readiness before upload.

## What the script does

The Python script performs the deterministic part of the workflow.

It:
- scans the actual folder structure
- checks whether required paths exist
- checks whether required glob patterns match files
- checks whether required files are non-empty
- flags discouraged filename patterns such as draft, temp, final_final, or copy
- checks whether required text patterns appear in target files such as README.md

The script outputs structured JSON, which makes the results easy for an agent or user to interpret.

## What worked well

The skill successfully distinguishes between a clean submission folder and a problematic one.

In testing:
- the pass_case returned PASS
- the fail_case returned FAIL

The script was able to identify missing required text patterns and flagged filename issues. The output format was also clear and reusable, which made it easy to summarize the results for the user.

## What limitations remain

This skill has several limitations:
- it does not grade the assignment
- it does not evaluate writing quality
- it does not review code quality in depth
- it only checks rules that are explicitly included in the manifest
- text-pattern checks are simple rule checks, not deep semantic checks
- it checks submission-readiness, not whether the project fully satisfies the assignment rubric

## Repository structure

```text
.
├── README.md
├── examples/
│   ├── pass_case/
│   └── fail_case/
└── .agents/
    └── skills/
        └── assignment-submission-checker/
            ├── SKILL.md
            ├── scripts/
            │   └── check_submission.py
            ├── references/
            └── assets/
                └── example_manifest.json
```
