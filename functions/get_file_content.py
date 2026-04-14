import os
import io
from google import genai
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Get contents from a specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file located relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_file_content( *, working_directory, file_path ):

  file_content = ''
  max_read = 10000

  try:
    working_dir_abs = os.path.abspath( working_directory )
    target_file = os.path.normpath( os.path.join( working_dir_abs, file_path ) )
    valid_target_file = os.path.commonpath( [ working_dir_abs, target_file ] ) == working_dir_abs
  except Exception as err:
    return f'Error: File or Path issue - { err }'


#  print( working_dir_abs )
#  print( target_file )
#  print( valid_target_file )

  try:
    if not valid_target_file:
      raise Exception( f'Error: Cannot read "{ file_path }" as it is outside the permitted working directory' )
    elif not os.path.exists( target_file ):
      raise Exception( f'Error: File not found or is not a regular file: "{ file_path }" - exist' )
    elif not os.path.isfile( target_file ):
      raise Exception( f'Error: File not found or is not a regular file: "{ file_path }" - file' )
  except Exception as err:
    return f'Error: Target validation issue - { err }'

  try:
    with open( target_file, 'r', encoding='utf-8' ) as file:
      file_content = file.read( max_read )
      if file.read( 1 ):
        file_content += f'[...File "{ file_path }" truncated at { max_read } characters]'
  except Exception as err:
    return f'Error: Target read issue - { err }'

  return file_content
