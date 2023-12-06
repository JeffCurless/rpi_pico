import sys
from parser import Parser

debugFile = False
debugCmds = False

CMD_MOVE         = "move"
CMD_TURNRIGHT    = "turnRight"
CMD_TURNLEFT     = "turnLeft"
CMD_DROPBALL     = "dropBall"
CMD_TAKEBALL     = "takeBall"
CMD_FRONTCLEAR   = "frontIsClear"
CMD_FRONTBLOCKED = "frontIsBlocked"
CMD_LEFTCLEAR    = "leftIsClear"
CMD_LEFTBLOCKED  = "leftIsBlocked"
CMD_RIGHTCLEAR   = "rightIsClear"
CMD_RIGHTBLOCKED = "rightIsBlocked"
CMD_FACINGNORTH  = "facingNorth"
CMD_FACINGEAST   = "facingEast"
CMD_FACINGSOUTH  = "facingSouth"
CMD_FACINGWEST   = "facingWest"
CMD_WHILE        = "while"
CMD_END          = "}"
CMD_BALLSPRESENT = "ballsPresent"
CMD_NOBALLS      = "noBallsPresent"
CMD_FOR          = "for"
CMD_RANGE        = "range"
CMD_IF           = "if"
CMD_ELSE         = "else"
CMD_FUNCTION     = "function"

#
# Instruction - Class that contains an specific command, and if
#               that command is capable, contains nested commands
#
class Instruction:
    def __init__(self,line,cmd,condition=False,loop=False):
        self.linenum       = line
        self.cmd           = cmd
        self.index         = 0
        self.range         = 0
        self.condition     = condition
        self.loopCondition = loop
        self.isLoop        = False
        self.instructions  = []
        self.elseCmds      = []
        self.skipCond      = False
        self.executeElse   = False
        self.funcName      = ""
        self.isDefinition  = False

    #
    # reportProblem - Report an error to the debug console
    #
    def reportProblem(self,message):
        print( "Error on line %d, error is %s"%(self.linenum,message))
        
    #
    # getCmd - Get the instruction name
    #
    def getCmd(self):
        return self.cmd
    
    #
    # __repr__ - Display the object when asked
    #
    def __repr__(self):
        return f"{self.linenum}:{self.cmd}:{self.condition}:{self.loopCondition}"
    
    #
    # __str__ - test to display when we convert this object to a string
    #
    def __str__(self):
        return f"{self.linenum}:{self.cmd}"
    
    #
    # __iter__ - For those instructions that contain sub-instructions,
    #            make sure we can iterate over them.
    #
    def __iter__(self):
        if self.skipCond:
            self.index = 1
        else:
            self.index = 0
        self.parent = self
        return self
    
    #
    # __next__ - Obtain the next item we are processing when dealing
    #            with an iterator
    #
    def __next__(self):
        if self.executeElse:
            cmds = self.elseCmds
        else:
            cmds = self.instructions
        
        if self.index >= len(cmds):
            if self.isLoop:
                self.index = 0
            else:
                raise StopIteration
                    
        cmd = cmds[self.index]
        if self.index == 0:
            cmd.condition = True
        self.index += 1
        return cmd
    
    #
    # getFirst - Obtain the first sub-instruction from an instruction
    #            that contains sub-instructions...
    #            Hacky way to support if/else
    #
    def getFirst(self):
        cmd = self.instructions[0]
        self.skipCond = True
        return cmd
    
    #
    # switchToElse - Switch to the secondary ELSE portion of an IF
    #
    def switchToElse(self):
        self.executeElse = True
        self.index       = 0
        self.skipCond    = False
       
#
# Program - The program.  A program consists of a number of instructions,
#           some of those instructions contain sub-instructions.  While
#           not the best way to do this, it does allow for a single pass
#           read and convert of the file, as well as eliminating jumps etc.
#
class Program:
    def __init__(self, filename ):
        self.filename = filename
        self.cmdList   = [CMD_MOVE,CMD_TURNRIGHT,CMD_TURNLEFT,
                          CMD_DROPBALL,CMD_TAKEBALL,
                          CMD_FRONTCLEAR,CMD_FRONTBLOCKED,
                          CMD_LEFTCLEAR,CMD_LEFTBLOCKED,
                          CMD_RIGHTCLEAR,CMD_RIGHTBLOCKED,
                          CMD_BALLSPRESENT, CMD_NOBALLS,
                          CMD_FACINGNORTH, CMD_FACINGEAST,CMD_FACINGSOUTH,CMD_FACINGWEST,
                          CMD_WHILE,CMD_FOR,CMD_END,CMD_FUNCTION,
                          CMD_IF,CMD_ELSE,CMD_RANGE]
        self.cmdCond   = [CMD_FRONTCLEAR,CMD_FRONTBLOCKED,CMD_BALLSPRESENT,CMD_NOBALLS]
        self.cmdLoop   = [CMD_WHILE, CMD_FOR]
        self.cmdBranch = [CMD_IF,CMD_ELSE]
        self.cmdFunct  = [CMD_FUNCTION]
        self.userFuncs = []
        self.stack     = []
        self.createProgram()
        
    #
    # reset - Reset instructions
    #
    def reset( self ):
        self.instructions = []
        self.index        = 0
    #
    # __iter__ - Setup the iterator for walking the instructions of a program
    #
    def __iter__(self):
        self.index = 0
        return self
        
    #
    # __next__ - Fetch the next instruction within an iterator.  When we
    #            step outside of the instruction set, raise the StopIteration
    #            Exception so python knows we are done iterating
    #
    def __next__(self):
        if self.index < len(self.instructions):
            cmd = self.instructions[self.index]
            self.index += 1
            return cmd
        else:
            raise StopIteration
        
    #
    # isValidInstruction - Determine if the passed in command is a valid
    #                      instruction or not.
    #
    def isValidInstruction( self, cmd ):
        if cmd in self.cmdList:
            return True
        return False
    
    #
    # isCommandConditional - Determine if the command given is a conditional
    #                        operator or not.
    #
    def isCommandConditional( self, cmd ):
        if cmd in self.cmdCond:
            return True
        return False
    
    #
    # isCommandLoop - Is this command some kind of looping instruction?
    #
    def isCommandLoop( self, cmd ):
        if cmd in self.cmdLoop:
            return True
        return False
    
    #
    # isBranch - Is this command a branching instruction?
    #
    def isBranch( self, cmd ):
        if cmd in self.cmdBranch:
            return True
        return False
    
    #
    # isCommandFunction - Is the command a function (lamba or whatever)
    #
    def isCommandFunction( self, cmd ):
        if cmd in self.cmdFunct:
            return True
        return False
    
    #
    # isUserFunction - 
    #
    def isUserFunction( self, cmd ):
        if cmd in self.userFuncs:
            return True
        return False
    
    #
    #
    #
    def FindUserFunction( self, linenum, line, loop ):
        for cmd in self.instructions:
            if cmd.cmd == CMD_FUNCTION:
                if cmd.funcName == line:
                    return cmd
        raise Exception( f"Calling an undefined function: {line}" )
    #
    # createProgram - Read in the data file and create the instructions.
    #
    # This code has a number of special cases that probably should be
    # eliminator or reduced.  The special cases all revolve around conditional
    # based instructions:
    #
    #     while <condition>
    #     for <condition>
    #     if <condition>
    #
    # Would be better if the "if" case was modified to separate the conditional
    # from the rest body of the if/else.  This way the code to implement the
    # execution of the if could simply run the conditional, and based on the
    # result, execute the "true" or the "false" result.
    #
    def createProgram(self):
        self.reset()       # Reset the instruction storage!
        
        parser    = Parser()
        lines     = parser.parse( self.filename )
        if debugFile:
            for item in lines:
                print( item )
        linenum   = 0
        current   = self.instructions
        loopCond  = False
        Condition = False
        lastCmd   = None
        lastIf    = None
        sameLine  = False
        haveFunction = False
        for line in lines:
            if sameLine == False:
                linenum += 1
            
            if len(line) == 0:
                continue
            
            if debugCmds: print( f"{linenum} : {line}" )

            if lastCmd and (lastCmd.cmd == CMD_FOR) and (line != CMD_RANGE):
                raise Exception( f"Invalid condition after FOR, line {linenum}:{line}" )
                
            if lastCmd and (lastCmd.cmd == CMD_RANGE):
                if debugCmds: print( "Set range to {line}" )
                lastCmd.range = int(line)
                lastCmd = None
                sameLine = False
                continue
            
            if self.isValidInstruction( line ):
                if line == CMD_END:
                    current = self.stack.pop()
                    if debugCmds: print( "Stack depth is " + str(len(self.stack)))
                else:
                    lastCmd = Instruction( linenum, line, loop=loopCond )
                    current.append( lastCmd )
            elif haveFunction:
                if debugCmds: print( f"Defined function: {line}" )
                lastCmd.funcName = line
                self.userFuncs.append(line)
                haveFunction = False
                sameLine = False
                continue
            elif self.isUserFunction( line ):
                if debugCmds: print( f"User calling function: {line}" )
                lastCmd = self.FindUserFunction( linenum, line, loop=loopCond)
                current.append(lastCmd)
            else:
                raise Exception( f"Invalid Instruction in file \"{self.filename}\" line {linenum}:{line}" )
            
            loopCond = False
            sameLine = False
            if self.isCommandConditional( line ):
                current[-1].condition = True
            if self.isCommandLoop( line ):
                current[-1].isLoop = True
                self.stack.append(current)
                if debugCmds: print( "Stack depth = " + str(len(self.stack)))
                current = current[-1].instructions
                loopCond = True
                sameLine = True
            if self.isCommandFunction( line ):
                lastCmd.isDefinition = True
                self.stack.append(current)
                if debugCmds: print( "Stack depth = " + str(len(self.stack)))
                current = current[-1].instructions
                sameLine = True
                haveFunction = True
            if line == CMD_RANGE:
                sameLine = True
            if line == CMD_IF:
                self.stack.append(current)
                if debugCmds: print( "Stack depth = " + str(len(self.stack)))
                current = current[-1].instructions
                lastIf = lastCmd
                sameLine = True
            if line == CMD_ELSE:
                if lastIf:
                    self.stack.append(current)
                    if debugCmds: print( "Stack depth = " + str(len(self.stack)))
                    current = lastIf.elseCmds
                    lastIf = None
                else:
                    raise Exception( f"Else with no IF in file \"{self.filename}\" line {linenum}:{line}" )
