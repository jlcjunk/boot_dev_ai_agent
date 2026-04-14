import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python script in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to be run.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,                     
                items=types.Schema(type=types.Type.STRING),
                description="List of string arguments to pass to the python script.",
            ),
        },
    ),
)


def run_python_file( *, working_directory, file_path, args=None ):

  output = ''

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
      raise Exception( f'Error: Cannot execute "{ file_path }" as it is outside the permitted working directory' )


#    elif not os.path.exists( target_file ):
#      raise Exception( f'Error: File not found or is not a regular file: "{ file_path }" - exist' )
    elif not os.path.isfile( target_file ):
      raise Exception( f'Error: "{ file_path }" does not exist or is not a regular file' )
    elif not file_path.endswith( ".py" ):
      raise Exception( f'Error: "{ file_path }" is not a Python file' )
  except Exception as err:
    return f'Error: Target validation issue - { err }'

  command = [ "python", target_file ]
  if args:
    command.extend( args )

  try:
    result = subprocess.run( command, capture_output=True, text=True, timeout=30, cwd=working_directory )
  except Exception as err:
    return f'Error: Execution issue - { err }'

  #print( "*********" )
  #print( result )
  #print( "*********" )
  #print( result.returncode )
  #print( "*********" )
  #print( result.stdout )
  #print( "*********" )
  #print( result.stderr )
  #print( "*********" )

  if result.returncode != 0:
    output += f'Process exited with code { result.returncode }\n'
  if not ( result.stdout or result.stderr ):
    output += f'No output produced\n'
  else:
    output += f'STDOUT: \n{ result.stdout }\n'
    output += f'STDERR: \n{ result.stderr }\n'

  return output
