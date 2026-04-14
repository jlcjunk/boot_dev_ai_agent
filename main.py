#!/usr/bin/env -S uv run --script

import sys
import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

#----------------------------------------------------------------------------------------------------


def call_function( function_call, verbose=False ):
  if verbose == True:
    print( f"Calling function: { function_call.name }({ function_call.args })" )
  else:
    print( f" - Calling function: { function_call.name }" )

  function_name = function_call.name or ""

  # fmt: off
  function_map = {
    "get_file_content": get_file_content,
    "get_files_info":   get_files_info,
    "write_file":       write_file,
    "run_python_file":  run_python_file,
  }
  # fmt: on

  if function_name not in function_map:
    #    print( "didn't find function **************" )
    return types.Content(
      role="tool",
      parts=[ types.Part.from_function_response(
        name=function_name,
        response={ "error": f"Unknown function: { function_name }"},
      ) ],
    )


  #  print( '+++++++++++' )
  command_wanted = function_map[ function_name ]
  #  print( f'command_wanted: { command_wanted }' )

  command_agrs = function_call.args.copy()
  #  print( f'command_agrs: { command_agrs }' )

  command_agrs[ 'working_directory' ] = "./calculator"
  #  print( f'command_agrs: { command_agrs }' )

  command_result = command_wanted( **command_agrs )
  #  print( f'command_result: { command_result }' )
  #  print( '+++++++++++' )

  return types.Content(
    role="user",
    parts=[ types.Part.from_function_response(
      name=function_name,
      response={ "result": command_result},
    ) ],
  )


def main():
  print( "Hello from boot-dev-ai-agent!" )

  message_text = ""

  ai_candidates = []

  ai_loop_max = 20

  function_responses = []

  system_prompt = """
  You are a helpful AI coding agent.

  When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

  - List files and directories
  - Read files
  - Write files
  - Execute python scripts

  All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
  """

  load_dotenv()
  api_key = os.environ.get( "GEMINI_API_KEY" )

  if api_key == None:
    raise Exception( "API key didn't load" )

  #   create list of functions available to the AI
  available_functions = types.Tool( function_declarations=[ schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file ], )

  #   setup CLI option parser
  parser = argparse.ArgumentParser( description="Chatbot" )
  parser.add_argument( "user_prompt", type=str, help="User prompt" )
  parser.add_argument( "--verbose", action="store_true", help="Enable verbose output" )
  args = parser.parse_args()

  client = genai.Client( api_key=api_key )


  #  content  = client.models.generate_content( model='gemini-2.5-flash', contents=args.user_prompt )

  for count in range( ai_loop_max ):


    messages = [ types.Content( role="user", parts = [ types.Part( text = f'User prompt:{ args.user_prompt }' ) ] ) ] + ai_candidates + function_responses

    try:
      response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig( tools=[ available_functions ], system_instruction=system_prompt ),
      )
    except Exception as err:
      print( f'=========ERROR===============' )
      print( err )
      print( f'=========ERROR===============' )
      return 1

    if args.verbose:
      print( f'User prompt: { args.user_prompt }' )
      print( f'Prompt tokens: { response.usage_metadata.prompt_token_count }' )
      print( f'Response tokens: { response.usage_metadata.candidates_token_count }' )

  #  print( response.text )
  #  print( f'**------------\n{ response.function_calls }\n**------------\n' )

    for item in response.candidates:
      ai_candidates.append( item.content )

    if response.function_calls:
      for item in response.function_calls:
        print( f"Calling function: { item.name }({ item.args })" )
        function_call_result = call_function( item )

        if len( function_call_result.parts ) == 0:
          raise Exception( 'No parts in the response' )

        if function_call_result.parts[ 0 ].function_response is None:
          raise Exception( 'No function response' )

        if function_call_result.parts[ 0 ].function_response.response is None:
          raise Exception( 'No response in the function response' )

        function_responses.append( function_call_result )
        [ types.Content( role="user", parts = [ types.Part( text = f'User prompt:{ args.user_prompt }' ) ] ) ]

        if args.verbose:
          print( f"-> {function_call_result.parts[0].function_response.response}" )
      

#      print( f'=========ARGS===============' )
#      print( f'{ args }' )

#      print( f'=========AI SYSTEM_PROMPT===============' )
#      print( f'{ system_prompt }' )

#      print( f'=========MESSAGES===============' )
#      print( f'{ messages }' )

#      print( f'=========AI RESPONSE===============' )
#      print( f'{ response }' )

#      print( f'=========AI RESPONSE_FUNCTION_CALLS===============' )
#      print( f'{ response.function_calls }' )

#      print( f'=========AI CANDIDATES===============' )
#      print( f'{ response.candidates }' )

#      print( f'=========AI CANDIDATES_CONTENT===============' )
#      print( f'{ response.candidates[0].content }' )

      print( f'=========AI CANDIDATES FUNCTION===============' )
      print( f'name:{ response.candidates[0].content.parts[0].function_call.name }\nargs:{ response.candidates[0].content.parts[0].function_call.args }' )

#      print( f'=========AI CANDIDATES_CUMULATIVE===============' )
#      print( f'{ ai_candidates }' )

#      print( f'=========CALL_RESULT===============' )
#      print( f'{ function_call_result }' )

#      print( f'=========CALL_RESULT_CUMULATIVE==============' )
#      print( f'{ function_responses }' )

      print( f'=========END===============' )
      print( f"end loop: { count + 1 }\n\n" )

    else:

#      print( f'=========MESSAGES===============' )
#      print( f'{ messages }' )

#      print( f'=========AI RESPONSE===============' )
#      print( f'{ response }' )


      print( f'=========AI RESPONSE TEXT===============' )
      print( f'{ response.candidates[0].content.parts[0].text }' )

      print( f'=========END===============' )
      print( f"end loop: { count + 1 }\n\n" )
      break


if __name__ == "__main__":
  sys.exit( main() )
