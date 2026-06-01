import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    # api key stuff
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Failed to load API key from .env")

    # gemini
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=messages
    )

    if response.usage_metadata is None:
        raise RuntimeError("failed to get an answer from Gemini")

    if args.verbose:
        print(
            f"User prompt: {args.user_prompt}\n"
            f"Prompt tokens: {response.usage_metadata.prompt_token_count}\n"
            f"Response tokens: {response.usage_metadata.candidates_token_count}\n"
        )

    print(f"Response: {response.text}")


if __name__ == "__main__":
    main()
