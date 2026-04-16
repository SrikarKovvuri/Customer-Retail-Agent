"""Terminal interface for the Python debugging agent."""

import sys
from agent import run_agent

SEPARATOR = "---"


def read_multiline(prompt: str) -> str:
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == SEPARATOR:
            break
        lines.append(line)
    return "\n".join(lines)


def main() -> None:
    print("=== Python Debugging Agent ===")
    print(f"Paste your buggy code, then type '{SEPARATOR}' on its own line.")
    print("Type 'quit' to exit.\n")

    while True:
        code = read_multiline(">> Paste code (end with ---):")
        if code.strip().lower() == "quit":
            break

        error = input(">> Optional error / wrong-output description (Enter to skip): ").strip()

        user_msg = f"```python\n{code}\n```"
        if error:
            user_msg += f"\n\nError / wrong output:\n{error}"

        print("\n[Thinking...]\n")
        try:
            answer = run_agent(user_msg)
        except Exception as e:
            print(f"Agent error: {e}\n")
            continue

        print(answer)
        print()


if __name__ == "__main__":
    main()
