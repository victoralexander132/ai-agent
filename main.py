import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


def main():
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    model_name = "gemini-2.0-flash-001"
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    is_verbose = False
    if len(sys.argv) < 2:
        print("Prompt must be provided")
        sys.exit(1)

    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            is_verbose = True
    user_prompt = sys.argv[1]
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    MAX_ITERATIONS = 20
    for n in range(MAX_ITERATIONS):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )
            if response.candidates:
                for candidate in response.candidates:
                    if candidate.content:
                        messages.append(candidate.content)

            if response.function_calls:
                for fun in response.function_calls:
                    print(f"- Calling function: {fun.name}")
                    function_result = call_function(fun, is_verbose)
                    tool_msg = types.Content(role="user", parts=function_result.parts)
                    messages.append(tool_msg)
                    if not function_result.parts[0].function_response.response:
                        raise Exception("Error calling function")
            else:
                if response.text:
                    print(response.text)
                    break

        except Exception as e:
            print(f"Error: {e}")

    if is_verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
