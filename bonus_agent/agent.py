import json
from openai import OpenAI

from prompts import SYSTEM_PROMPT
from tools import TOOL_SCHEMA, run_python_code

MAX_TOOL_ROUNDS = 6


def run_agent(user_message: str, *, model: str = "gpt-4o-mini") -> str:
    client = OpenAI()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    for _ in range(MAX_TOOL_ROUNDS):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=[TOOL_SCHEMA],
            temperature=0.0,
        )
        choice = response.choices[0]

        if choice.finish_reason == "tool_calls":
            assistant_msg = choice.message.model_dump()
            messages.append(assistant_msg)

            for tc in choice.message.tool_calls:
                args = json.loads(tc.function.arguments)
                tool_result = run_python_code(args["code"])
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": tool_result,
                })
        else:
            return choice.message.content or ""

    return "[Agent reached maximum tool-call rounds without a final answer.]"
