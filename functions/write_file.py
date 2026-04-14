import os
import io
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write contents to a specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The ile to write relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text to be written to the file.",
            ),
        },
    ),
)


def write_file( *, working_directory, file_path, content ):

  file_content = ''
  max_read = 10000

  if not isinstance( content, str ):
    return f'Error: Content is not valid string.'

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
      raise Exception( f'Error: Cannot write to "{ file_path }" as it is outside the permitted working directory' )


#    elif not os.path.exists( target_file ):
#      raise Exception( f'Error: File not found or is not a regular file: "{ file_path }" - exist' )
    elif os.path.isdir( target_file ):
      raise Exception( f'Error: Cannot write to "{ file_path }" as it is a directory' )
  except Exception as err:
    return f'Error: Target validation issue - { err }'

  try:
    with open( target_file, 'w', encoding='utf-8' ) as file:
      file_content = file.write( content )
  except Exception as err:
    return f'Error: Target write issue - { err }'

  return f'Successfully wrote to "{ file_path }" ({ file_content } characters written)'
