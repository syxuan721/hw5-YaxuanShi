import json
import sys
import re
from pathlib import Path


def load_manifest(manifest_path: Path) -> dict:
    with manifest_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def check_required_paths(base_dir: Path, manifest: dict):
    results = []
    for rel_path in manifest.get("required_paths", []):
        target = base_dir / rel_path
        results.append({
            "type": "required_path",
            "path": rel_path,
            "passed": target.exists(),
            "message": "Found" if target.exists() else "Missing required path"
        })
    return results


def check_required_globs(base_dir: Path, manifest: dict):
    results = []
    for pattern in manifest.get("required_globs", []):
        matches = list(base_dir.glob(pattern))
        results.append({
            "type": "required_glob",
            "pattern": pattern,
            "passed": len(matches) > 0,
            "message": f"Matched {len(matches)} file(s)" if matches else "No files matched required pattern"
        })
    return results


def check_non_empty_files(base_dir: Path, manifest: dict):
    results = []
    for rel_path in manifest.get("non_empty_files", []):
        target = base_dir / rel_path
        if not target.exists():
            results.append({
                "type": "non_empty_file",
                "path": rel_path,
                "passed": False,
                "message": "File is missing"
            })
        elif target.is_file() and target.stat().st_size > 0:
            results.append({
                "type": "non_empty_file",
                "path": rel_path,
                "passed": True,
                "message": "File exists and is non-empty"
            })
        else:
            results.append({
                "type": "non_empty_file",
                "path": rel_path,
                "passed": False,
                "message": "File exists but is empty"
            })
    return results


def check_flagged_filenames(base_dir: Path, manifest: dict):
    results = []
    flagged_patterns = manifest.get("flagged_filename_patterns", [])
    for path in base_dir.rglob("*"):
        if path.is_file():
            name = path.name.lower()
            matched = [p for p in flagged_patterns if p.lower() in name]
            if matched:
                results.append({
                    "type": "flagged_filename",
                    "path": str(path.relative_to(base_dir)),
                    "passed": False,
                    "message": f"Flagged filename pattern found: {', '.join(matched)}"
                })
    return results


def check_required_text_patterns(base_dir: Path, manifest: dict):
    results = []
    for rule in manifest.get("required_text_patterns", []):
        rel_path = rule["path"]
        patterns = rule.get("patterns", [])
        target = base_dir / rel_path

        if not target.exists() or not target.is_file():
            results.append({
                "type": "required_text_patterns",
                "path": rel_path,
                "passed": False,
                "message": "Target file is missing"
            })
            continue

        try:
            content = target.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            results.append({
                "type": "required_text_patterns",
                "path": rel_path,
                "passed": False,
                "message": f"Could not read file: {e}"
            })
            continue

        missing = []
        for pattern in patterns:
            if not re.search(pattern, content, re.IGNORECASE):
                missing.append(pattern)

        results.append({
            "type": "required_text_patterns",
            "path": rel_path,
            "passed": len(missing) == 0,
            "message": "All required patterns found" if not missing else f"Missing text pattern(s): {missing}"
        })
    return results


def summarize(results):
    fail_count = sum(1 for r in results if not r["passed"] and r["type"] != "flagged_filename")
    warning_count = sum(1 for r in results if not r["passed"] and r["type"] == "flagged_filename")

    if fail_count > 0:
        status = "FAIL"
    elif warning_count > 0:
        status = "WARNING"
    else:
        status = "PASS"

    return {
        "overall_status": status,
        "counts": {
            "total_checks": len(results),
            "failures": fail_count,
            "warnings": warning_count
        },
        "details": results
    }


def main():
    if len(sys.argv) != 3:
        print(json.dumps({
            "error": "Usage: python check_submission.py <submission_folder> <manifest.json>"
        }, indent=2))
        sys.exit(1)

    submission_folder = Path(sys.argv[1]).resolve()
    manifest_path = Path(sys.argv[2]).resolve()

    if not submission_folder.exists() or not submission_folder.is_dir():
        print(json.dumps({
            "error": "Submission folder does not exist or is not a directory"
        }, indent=2))
        sys.exit(1)

    if not manifest_path.exists() or not manifest_path.is_file():
        print(json.dumps({
            "error": "Manifest file does not exist"
        }, indent=2))
        sys.exit(1)

    manifest = load_manifest(manifest_path)

    results = []
    results.extend(check_required_paths(submission_folder, manifest))
    results.extend(check_required_globs(submission_folder, manifest))
    results.extend(check_non_empty_files(submission_folder, manifest))
    results.extend(check_flagged_filenames(submission_folder, manifest))
    results.extend(check_required_text_patterns(submission_folder, manifest))

    summary = summarize(results)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
