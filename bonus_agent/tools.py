import json
import os
import re
import subprocess
import sys
import tempfile

DANGEROUS_PATTERNS = [
    r"\bos\.system\b",
    r"\bsubprocess\b",
    r"\bshutil\.rmtree\b",
    r"\b__import__\b",
    r"\beval\b",
    r"\bexec\b",
    r"\bopen\s*\(.*,\s*['\"]w",
    r"\brmdir\b",
    r"\bunlink\b",
]

TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "run_python_code",
        "description": (
            "Execute a snippet of Python code in an isolated process with a "
            "3-second timeout. Returns JSON with stdout, stderr, timed_out, "
            "and success fields."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The Python source code to execute.",
                },
            },
            "required": ["code"],
        },
    },
}


def run_python_code(code: str) -> str:
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, code):
            return json.dumps({
                "stdout": "",
                "stderr": f"Blocked: code matched dangerous pattern ({pattern})",
                "timed_out": False,
                "success": False,
            })

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    )
    try:
        tmp.write(code)
        tmp.close()
        result = subprocess.run(
            [sys.executable, tmp.name],
            capture_output=True,
            text=True,
            timeout=3,
        )
        return json.dumps({
            "stdout": result.stdout[-2000:],
            "stderr": result.stderr[-2000:],
            "timed_out": False,
            "success": result.returncode == 0,
        })
    except subprocess.TimeoutExpired:
        return json.dumps({
            "stdout": "",
            "stderr": "Process timed out after 3 seconds.",
            "timed_out": True,
            "success": False,
        })
    finally:
        os.unlink(tmp.name)
