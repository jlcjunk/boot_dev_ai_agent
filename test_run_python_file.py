from functions.run_python_file import run_python_file

print( "---------------------" )
print( run_python_file( working_directory="calculator", file_path="main.py" ) )
print( "---------------------" )
print( run_python_file( working_directory="calculator", file_path="main.py", args=[ "3 + 5" ] ) )
print( "---------------------" )
print( run_python_file( working_directory="calculator", file_path="main.py", args=[ "3 + 5 * 2" ] ) )
print( "---------------------" )
print( run_python_file( working_directory="calculator", file_path="tests.py" ) )
print( "---------------------" )
print( run_python_file( working_directory="calculator", file_path="../main.py" ) )
print( "---------------------" )
print( run_python_file( working_directory="calculator", file_path="nonexistent.py" ) )
print( "---------------------" )
print( run_python_file( working_directory="calculator", file_path="lorem.txt" ) )
print( "---------------------" )

#   before making named arguments

# print( "---------------------" )
# print( run_python_file( "calculator", "main.py" ) )
# print( "---------------------" )
# print( run_python_file( "calculator", "main.py", [ "3 + 5" ] ) )
# print( "---------------------" )
# print( run_python_file( "calculator", "tests.py" ) )
# print( "---------------------" )
# print( run_python_file( "calculator", "../main.py" ) )
# print( "---------------------" )
# print( run_python_file( "calculator", "nonexistent.py" ) )
# print( "---------------------" )
# print( run_python_file( "calculator", "lorem.txt" ) )
# print( "-


# truncated for boot dev

#print( "---------------------" )
#print( run_python_file( "calculator", "main.py" )[ :-15 ] )
#print( "---------------------" )
#print( run_python_file( "calculator", "main.py", [ "3 + 5" ] )[ :-15 ] )
#print( "---------------------" )
#print( run_python_file( "calculator", "tests.py" )[ :-15 ] )
#print( "---------------------" )
#print( run_python_file( "calculator", "../main.py" ) )
#print( "---------------------" )
#print( run_python_file( "calculator", "nonexistent.py" ) )
#print( "---------------------" )
#print( run_python_file( "calculator", "lorem.txt" ) )
#print( "---------------------" )
