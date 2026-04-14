from functions.get_file_content import get_file_content

#   need to fit the right output in boot dev buffer
#     needs to see:
#       def main():
#       def _apply_operator(self, operators, values)
#       Error:

print( "---------------------" )
print( get_file_content( 'calculator', 'lorem.txt' )[ -75: ] )
print( "---------------------" )
print( get_file_content( 'calculator', 'main.py' )[ 100:155 ] )
print( "---------------------" )
print( get_file_content( 'calculator', 'pkg/calculator.py' )[ 1150:1300 ] )
print( "---------------------" )
print( get_file_content( 'calculator', '/bin/cat' ) )
print( "---------------------" )
print( get_file_content( 'calculator', 'pkg/does_not_exist.py' ) )
print( "---------------------" )
print( get_file_content( 'calculator', 'pkg' ) )
print( "---------------------" )

#   full output except for random first doc

#print( "---------------------" )
#print( get_file_content( 'calculator', 'lorem.txt' )[ -75: ] )
#print( "---------------------" )
#print( get_file_content( 'calculator', 'main.py' ) )
#print( "---------------------" )
#print( get_file_content( 'calculator', 'pkg/calculator.py' ) )
#print( "---------------------" )
#print( get_file_content( 'calculator', '/bin/cat' ) )
#print( "---------------------" )
#print( get_file_content( 'calculator', 'pkg/does_not_exist.py' ) )
#print( "---------------------" )
#print( get_file_content( 'calculator', 'pkg' ) )
#print( "---------------------" )
