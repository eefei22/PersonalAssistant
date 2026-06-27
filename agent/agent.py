import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv(Path(__file__).parent.parent / "configs" / "config.env")

from agent.system_prompt import get_system_prompt
from agent.tools import TOOL_SCHEMAS, execute_tool

MODEL="gpt-5-nano"


def run_agent(user_message: str, conversation_history: list) -> str:
    """
    One turn of the agentic loop.
    Sends the message, handles any tool calls, returns the final text response.
    conversation_history is mutated in place so multi-turn context is preserved.
    """
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    conversation_history.append({"role": "user", "content": user_message})

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            tools=TOOL_SCHEMAS,
            messages=[{"role": "system", "content": get_system_prompt()}] + conversation_history,
        )

        message = response.choices[0].message
        conversation_history.append(message)

        if response.choices[0].finish_reason == "stop":
            return message.content or ""

        if response.choices[0].finish_reason == "tool_calls":
            tool_results = []
            for tool_call in message.tool_calls:
                name = tool_call.function.name
                inputs = json.loads(tool_call.function.arguments)
                print(f"  [tool] {name}({inputs})")
                result = execute_tool(name, inputs)
                tool_results.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

            conversation_history.extend(tool_results)


def main():
    print("Personal Assistant ready. Type 'exit' to quit.\n")
    history = []
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "bye"):
            print("Bye!")
            break

        response = run_agent(user_input, history)
        print(f"\nAssistant: {response}\n")


if __name__ == "__main__":
    main()
