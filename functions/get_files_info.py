import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info( *, working_directory, directory="." ):

  file_list = ''

  try:
    working_dir_abs = os.path.abspath( working_directory )
    target_dir = os.path.normpath( os.path.join( working_dir_abs, directory ) )
    valid_target_dir = os.path.commonpath( [ working_dir_abs, target_dir ] ) == working_dir_abs
  except Exception as err:
    return f'Error: File or Path issue - { err }'

  try:
    if not valid_target_dir:
      raise Exception( f'Error: Cannot list "{ target_dir }" as it is outside the permitted working directory' )
    elif not ( os.path.exists( target_dir ) and os.path.isdir( target_dir ) ):
      raise Exception( f'Error: "{ target_dir }" is not a directory' )
  except Exception as err:
    return f'Error: Target validation issue - { err }'

  try:
    dir_list = os.listdir( target_dir )
  except Exception as err:
    return f'Error: Dir list issue - { err }'

  try:
    for item in dir_list:
      item_info = os.stat( os.path.join( target_dir, item ) )
      item_is_dir = os.path.isdir( os.path.join( target_dir, item ) )
      file_list += f'{ item }: file_size={ item_info.st_size } bytes, is_dir={ item_is_dir }\n'
  except Exception as err:
    return f'Error: Problem gathering file info - { err }'

  return file_list
