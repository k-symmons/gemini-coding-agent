from google import genai
from google.genai import types

from call_functions import available_functions, call_function
from config import MODEL
from system_prompt import system_prompt


def generate_content(
    client: genai.Client, messages: list[types.Content], verbose: bool
) -> None | str:
    response = client.models.generate_content(
        model=MODEL,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        if response.text:
            return response.text
        if not response.text:
            raise Exception("No response text generated")

    function_responses: list[types.Part] = []
    if response.function_calls:
        for function_call in response.function_calls:
            result = call_function(function_call, verbose)
            if (
                not result.parts
                or not result.parts[0].function_response
                or not result.parts[0].function_response.response
            ):
                raise RuntimeError(f"Empty function_response for {function_call.name}")

            if verbose:
                print(f"-> {result.parts[0].function_response.response}")
            function_responses.append(result.parts[0])

    messages.append(types.Content(role="user", parts=function_responses))
