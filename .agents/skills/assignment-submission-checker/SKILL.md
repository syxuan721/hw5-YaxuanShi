---
name: assignment-submission-checker
description: Checks a course assignment submission folder before upload. Use when a user wants to verify that required files, folders, naming rules, and basic submission packaging requirements are satisfied.
---

# Assignment Submission Checker

## What this skill does
This skill checks whether a course assignment submission folder is complete and packaged correctly before submission. It is designed for narrow, reusable pre-submission checks rather than general project review.

## When to use this skill
Use this skill when the user wants to:
- check whether a submission folder is missing required files or folders
- verify naming rules or expected file extensions
- check whether required deliverables are empty
- check whether a README includes required information such as a video link
- get a short pre-submission fix list

## When not to use this skill
Do not use this skill when the user wants to:
- evaluate writing quality
- grade the assignment
- review code quality in depth
- judge whether the project fully satisfies a rubric beyond packaging and required-file checks
- rewrite the assignment content itself

## Expected inputs
The user should provide:
- a target submission folder to inspect
- a manifest or list of required files, folders, and checks

A manifest may include:
- required exact paths
- required glob patterns
- files that must be non-empty
- filename patterns that should be flagged
- required text patterns inside specific files

## How to use this skill
1. Identify the submission folder the user wants checked.
2. Identify the manifest or required packaging rules.
3. Run the Python script in `scripts/check_submission.py`.
4. Read the structured JSON results from the script.
5. Summarize the results clearly for the user:
   - overall status
   - missing items
   - warnings
   - the most important fixes before submission
6. Stay within scope. Report packaging and submission-readiness only.

## Script role
The script performs the deterministic part of the workflow:
- scanning the actual file tree
- checking whether required paths exist
- checking whether required files are non-empty
- checking filename patterns
- checking for required text patterns in target files

This task should not rely on prose alone because the result depends on the real file system and rule-based checks.

## Output style
Return:
- an overall status such as PASS, WARNING, or FAIL
- a short checklist of issues
- a concise fix list in priority order

## Caveats and limitations
- This skill checks packaging, not academic quality.
- This skill only checks rules that are explicitly given in the manifest.
- If the manifest is incomplete, the skill may miss course-specific requirements.
- Text-pattern checks are simple rule checks, not semantic understanding.
