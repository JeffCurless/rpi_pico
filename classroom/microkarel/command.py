import sys
#from karelcmds import *
debugCmds = False

CMD_MOVE         = "move"
CMD_TURNRIGHT    = "turnRight"
CMD_TURNLEFT     = "turnLeft"
CMD_DROPBALL     = "dropBall"
CMD_TAKEBALL     = "takeBall"
CMD_FRONTCLEAR   = "frontIsClear"
CMD_WHILE        = "while"
CMD_END          = "end"
CMD_FRONTBLOCKED = "frontIsBlocked"
CMD_BALLSPRESENT = "ballsPresent"
CMD_NOBALLS      = "noBallsPresent"
CMD_FOR          = "for"

#
#
#
class Instruction:
    def __init__(self,line,cmd,condition=False,loop=False):
        self.linenum       = line
        self.cmd           = cmd
        self.index         = 0
        self.condition     = condition
        self.loopCondition = loop
        self.isLoop        = False
        self.instructions  = []

    def reportProblem(self,message):
        print( "Error on line %d, error is %s"%(self.linenum,message))
        
    def getCmd(self):
        return self.cmd
    
    def __repr__(self):
        return f"{self.linenum}:{self.cmd}:{self.condition}:{self.loopCondition}"
    
    def __str__(self):
        return f"{self.linenum}:{self.cmd}"
    
    def __iter__(self):
        self.index = 0
        self.parent = self
        return self
    
    def __next__(self):
        if self.index >= len(self.instructions):
            if self.isLoop:
                self.index = 0
            else:
                raise StopIteration
                    
        cmd = self.instructions[self.index]
        if self.index == 0:
            cmd.condition = True
        self.index += 1
        return cmd
#
#
#
class Program:
    def __init__(self, filename ):
        self.filename = filename
        self.instructions = []
        self.index   = 0
        self.cmdList = [CMD_MOVE,CMD_TURNRIGHT,CMD_TURNLEFT,CMD_DROPBALL,CMD_TAKEBALL,
                        CMD_FRONTCLEAR,CMD_WHILE,CMD_END,CMD_FRONTBLOCKED,CMD_BALLSPRESENT,CMD_NOBALLS]
        self.cmdCond = [CMD_FRONTCLEAR,CMD_FRONTBLOCKED,CMD_BALLSPRESENT,CMD_NOBALLS]
        self.cmdLoop = [CMD_WHILE, CMD_FOR]
        self.createProgram()

        
    def __iter__(self):
        self.index = 0
        return self
        
    def __next__(self):
        if self.index < len(self.instructions):
            cmd = self.instructions[self.index]
            self.index += 1
            return cmd
        else:
            raise StopIteration
        
    #
    #
    #
    def isValidInstruction( self, cmd ):
        if cmd in self.cmdList:
            return True
        return False
    
    #
    # 
    #
    def isCommandConditional( self, cmd ):
        if cmd in self.cmdCond:
            return True
        return False
    
    def isCommandLoop( self, cmd ):
        if cmd in self.cmdLoop:
            return True
        return False
    
    #
    # readFile - Open the instruction file and read the information in, make sure that
    # we create the array of instructions for translation.
    #
    def readFile(self):
        file = open( self.filename, "r" )
        lines = []
        while True:
            line = file.readline()

            if not line:
                break
            
            line = line.lstrip()
            line = line.rstrip()
            if self.isComment( line ):
                lines.append(line)
            else:
                temp = line.split()
                for x in temp:
                    lines.append(x)
        
        print( lines )
        file.close()
        return lines
    
    #
    #
    #
    def isComment(self,line):
        if len(line) <= 0:
            return True
        if line[0] == '#':
            return True
        return False
    
    #
    #
    #
    def createProgram(self):
        lines = self.readFile()
        linenum = 0
        self.instructions = []
        current = self.instructions
        loopCond = False
        Condition = False
        for line in lines:
            if loopCond == False:
                linenum += 1
                
            if self.isComment(line):
                continue
            
            if debugCmds: print( f"{linenum} : {line}" )
            
            if self.isValidInstruction( line ):
                if line == CMD_END:
                    current = self.instructions
                    if debugCmds:
                        print( "Reset Current : " + str( current ))
                else:
                    current.append( Instruction( linenum, line, loop=loopCond  ) )
            else:
                raise Exception( f"Invalid Instruction in file \"{self.filename}\" line {linenum}:{line}" )
            
            loopCond = False
            if self.isCommandConditional( line ):
                current[-1].condition = True
            if self.isCommandLoop( line ):
                current[-1].isLoop = True
                current = current[-1].instructions
                loopCond = True
                
