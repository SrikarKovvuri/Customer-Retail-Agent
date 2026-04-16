"""Five quick eval cases — run with: python eval.py"""

from agent import run_agent

CASES = [
    {
        "name": "Off-by-one in range",
        "input": (
            "```python\ndef first_n(n):\n    return [i for i in range(1, n)]\n"
            "print(first_n(5))\n```\n\n"
            "Expected [1, 2, 3, 4, 5] but got [1, 2, 3, 4]."
        ),
        "should_mention": "range",
    },
    {
        "name": "Mutable default argument",
        "input": (
            "```python\ndef append_to(val, lst=[]):\n    lst.append(val)\n"
            "    return lst\n\nprint(append_to(1))\nprint(append_to(2))\n```\n\n"
            "Second call returns [1, 2] instead of [2]."
        ),
        "should_mention": "default",
    },
    {
        "name": "Integer division",
        "input": (
            "```python\ndef avg(a, b):\n    return a + b / 2\n\n"
            "print(avg(3, 7))\n```\n\n"
            "Expected 5.0 but got 6.5."
        ),
        "should_mention": "parenthes",
    },
    {
        "name": "KeyError on missing dict key",
        "input": (
            "```python\nd = {'a': 1}\nprint(d['b'])\n```\n\n"
            "Getting a KeyError."
        ),
        "should_mention": "get",
    },
    {
        "name": "Infinite loop",
        "input": (
            "```python\ni = 0\nwhile i < 10:\n    print(i)\n```\n\n"
            "The program hangs and never finishes."
        ),
        "should_mention": "increment",
    },
]


def main() -> None:
    passed = 0
    for i, case in enumerate(CASES, 1):
        print(f"\n{'='*60}")
        print(f"Case {i}: {case['name']}")
        print("="*60)
        answer = run_agent(case["input"])
        print(answer[:600])
        hit = case["should_mention"].lower() in answer.lower()
        status = "PASS" if hit else "FAIL"
        if hit:
            passed += 1
        print(f"\n>> keyword '{case['should_mention']}' found: {status}")

    print(f"\n{'='*60}")
    print(f"Result: {passed}/{len(CASES)} passed")


if __name__ == "__main__":
    main()
