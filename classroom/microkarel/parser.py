
class Parser:
    #
    # readFile - Open the instruction file and read the information.
    #
    # Make sure that we create the array of lines.  While reading in the
    # file, make sure we strip while space from the beginning and end of
    # lines, and keep comment lines together.
    #
    def __readFile(self, filename):
        file = open( filename, "r" )
        lines = []
        while True:
            line = file.readline()

            if not line:
                break
            
            line = line.lstrip()
            line = line.rstrip()
            lines.append( line )

        file.close()
        return lines
    
    #
    # isComment - Is this line a comment or not?
    #
    # A comment is defined as any line starting with a '#', or a blank line
    # 
    def __isComment(self,line):
        if len(line) <= 0:
            return True
        if line.startswith( "#" ):
            return True
        return False
    
    #
    # removeItem - Remove the "old" item from all the lines.
    #
    # Simply remove the "old" string from every line.  The string
    # is replaced with a space.
    #
    def __removeItem( self, lines, old  ):
        newLines = []
        for line in lines:
            newLines.append( line.replace( old, " " ) )
        return newLines
    
    #
    # replaceItem - Replace the old with the new
    #
    # Every instance of "old" will be replaced with "new" in the
    # instruction list
    #
    def __replaceItem( self, lines, old, new ):
        newLines = []
        for line in lines:
            newLines.append( line.replace( old, new ) )
        return newLines
    
    #
    # convertSyntax - Convert the lines to our syntax
    #
    # Convert our language syntax to the instructions that the
    # Karel interpreter will understand.
    #
    def __convertSyntax( self, lines ):
        newLine = []
        lines = self.__removeItem( lines, "{" )
        lines = self.__removeItem( lines, "(" )
        lines = self.__removeItem( lines, ")" )
        lines = self.__removeItem( lines, " var " )
        lines = self.__removeItem( lines, " in " )
        for line in lines:
            if self.__isComment( line ):
                newLine.append( "" )
            else:
                temp = line.split()
                for item in temp:
                    newLine.append(item)
       
        return newLine
    
    #
    # parse - Parse the program
    #
    # This is the main entry point for the class... Read in the file,
    # verify the syntax, and convert to instructions for the interpreter...
    #
    def parse( self, filename ):
        data = self.__readFile( filename )
        data = self.__convertSyntax( data )
        return data
   

    