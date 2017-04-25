import xml.etree.ElementTree as ET
import sys

# Static variables
STR_PROGRAM         = "Program"
STR_MAINCLASS       = "MainClass"
STR_VARIANT         = "variant"
STR_SETOFFUNCTIONS  = "SetOfFunction"
STR_STEP            = "step"
STR_SETOFSTEPS      = "SetOfSteps"
STR_STEP            = "Step"
STR_STEPLINE        = "StepLine"
STR_STEPNUMBER      = "StepNumber"
STR_INTEGER         = "Integer"
STR_STMT            = "Stmt"
STR_IFSTMT          = "IfStmt"
STR_EXIT            = "Exit"
STR_URL             = "URL"
STR_RESULT          = "Result"
STR_OBJECTEXPR      = "ObjectExpr"
STR_STRINGLITERAL   = "String_literal"
STR_INTEGERTIME     = "IntegerTime"
STR_ID              = "ID"
STR_OTHERWISESTMT   = "OtherwiseStmt"
STR_SHOULDPHRASE    = "ShouldPhrase"
STR_INTEGEREXPR     = "IntegerExpr"
STR_STRINGEXPR      = "StringExpr"
STR_PLUS            = "Plus"
STR_MINUS           = "Minus"
#String for the output code
outputCode = ""

#Global variables for checking
functionNames=[]
usedFunctions=[]
stepsDefined=[]
stepsUsed=[]
errorText=''
currentURL=''
graph = {}
global preprocessorDic
preprocessorDic = {}
global liveNodes
liveNodes = {}
global loopNodes
loopNodes = []
global gotoNodes
gotoNodes = []
global concatList
concatList = []
global childParentGraph
childParentGraph ={}


# Gets the root of the xml
def getTreeRoot(xmlLocation = '../../outputs/outputs15.html.xml'):
    tree = ET.parse(xmlLocation)
    root = tree.getroot()
    return root

def addToError(errorMsg, numTab = 1):
    global errorText
    for i in range (numTab):
        errorText +="\t"
    errorText+="print(\"ERROR: " + errorMsg + "\")\n"
    print ("ERROR: " + errorMsg)
    
# this creates the output code in a file format and appends newline at the end
def addToLine (result, numTab = 0):
    global outputCode
    for i in range (numTab):
        outputCode +="\t"
    outputCode += result + "\n"

def addToGraph(parent,node):
    global graph
    if(parent in graph):
        graph[parent].add(node)
    else:
        graph[parent]=set([node])
        
        

# this creates the output code in a file format and appends newline at the end
def addNewLineToLine ():
    global outputCode
    outputCode += "\n"

def addPreprocessorLines(preprocessorFileName):
    global preprocessorDic
    if(preprocessorFileName!=''):
        with open(preprocessorFileName) as f:
            for line in f:
                preprocessorDic[line.split("=")[0].strip()]=line.split("=")[1].strip()

# Creates the initial block
def createInitialBlock (preprocessorFileName):
    addToLine ("from splinter import Browser")
    addToLine ("from time import sleep")
    addNewLineToLine()
    addToLine ("SLASH = \"/\"")
    addNewLineToLine()

# create def
def createDef(stepNumber, functionName):
    defLine = "def "
    if (functionName != ""):
        defLine += functionName + "_"
        stepsUsed.append(functionName+"_step"+stepNumber)
    else:
        stepsUsed.append(functionName+"step"+stepNumber)
    
    defLine += "step"+ str(stepNumber) +"(browser, loop = False):"
    return defLine

# create the def for the first def
def createStepDef(functionName):
    defLine = "def "
    if (functionName != ""):
        defLine += functionName + "_"
    
    defLine += "step (browser, loop = False):"
    return defLine

# Create step()
def createFirstStepFunction(functionName, nextStepNumber):
    if (functionName in liveNodes or len(liveNodes)==0):
        addToLine(createStepDef(functionName))
        if (functionName != ""):
            addToLine ("return " + functionName +"_step" + str(nextStepNumber) + "(browser, loop)", 1)
            addToGraph(functionName,functionName +"_step" + str(nextStepNumber))
        else:
            addToLine ("return step" + str(nextStepNumber) + "(browser, loop)", 1)
            addToGraph("","step" + str(nextStepNumber))
        addNewLineToLine()      

# Returns the variant # of the given element
def getVariant(e):
    return e.attrib.get(STR_VARIANT)

# Handles the objectExpr
def objectExprHandler (objExpr):
    global currentURL
    variant = getVariant(objExpr)
    
    if (variant == "0"):
        # TODO: this is not handled
        # DocumentObj:DocumentObject THAT:That HAVE:Have VALUE:Value STRING_LITERAL:String_literal
        return 
    elif (variant == "1"):
        #LOCALITYINDIC:LocalityIndic DocumentObj:DocumentObject
        return "browser.html"
    elif (variant == "2"):
        #DocumentObj:DocumentObject WITH:With ATTRIBUTE:Attribute STRING_LITERAL:String_literal
        return 'browser.find_by_id("' +objExpr.find(STR_STRINGLITERAL).text+ '").first'      
    elif (variant == "3"):
        #DocumentObj:DocumentObject WITH:With VALUE:Value STRING_LITERAL:String_literal
        return 'browser.find_by_id("' +objExpr.find(STR_STRINGLITERAL).text+ '")'      
    elif (variant == "4"):
        # TODO: this is not handled
        # DocumentObj:DocumentObject POSITIONINDIC:Positionindic URL:URL
        return 
    elif (variant == "5"):
        #LOCALITYINDIC:LocalityIndic URL_LITERAL:URL_Literal;
        return "browser.url"
    elif (variant == "6"):
        #PREDEFINED:Predefined ID:ID
        return preprocessorDic[objExpr.find(STR_ID).text]
    else:
        addToError("unhandled objExpr")

# this creates the loop for the step
def loopStep (stmt, stepNumber, tabOffSet = 0, functionName = ""):
    times = stmt.find(STR_INTEGERTIME).find(STR_INTEGER).text
    
    graphFunctionName = functionName if functionName=="" else functionName+"_"

    loopStepNumber = stmt.find(STR_STEPNUMBER).find(STR_INTEGER).text
    global loopNodes
    loopNodes.append(graphFunctionName +"step"+loopStepNumber)

    addToLine ("for c in range (" + times + '):', 1 + tabOffSet)
    addToLine ("err=" + graphFunctionName + "step" + loopStepNumber + "(browser, loop=True)", 2 + tabOffSet)
    addToLine ("if not (err == None) and not (err.isspace()) and not (len(err) == 0):", 2 + tabOffSet)
    addToLine ('return "' +  stepNumber + '"', 3 + tabOffSet)

def checkFunctionName(functionId):
    global functionNames

    return functionId in functionNames

# this creates the loop for the function
def doFunction (stmt, stepNumber, tabOffSet = 0, calledFromFunctionName=""):
    global usedFunctions
    
    times = stmt.find(STR_INTEGERTIME)
    times_variant = getVariant(times)
    # ERROR checking: check if functionId exists
    functionId = stmt.find(STR_ID).text
    if (calledFromFunctionName!=""):
        addToGraph(calledFromFunctionName+"_step"+stepNumber,functionId)
    else:
        addToGraph("step"+stepNumber,functionId)
    
    if (checkFunctionName(functionId)):
        usedFunctions.append(functionId)
        if (times_variant == "0"):
            
            times = stmt.find(STR_INTEGERTIME).find(STR_INTEGER).text
            
            addToLine ("for c in range (" + times + '):', 1 + tabOffSet)
            addToLine ("err=" + functionId + "_step(browser, loop=True)", 2 + tabOffSet)
            addToLine ("if not (err == None) and not (err.isspace()) and not (len(err) == 0):", 2 + tabOffSet)
            addToLine ('return "' +  stepNumber + '"', 3 + tabOffSet)

        elif (times_variant == "1"):     
            addToLine ("err=" + functionId + "_step(browser,loop=False)", 1 + tabOffSet)
            addToLine ("if not (err == None) and not (err.isspace()) and not (len(err) == 0):", 1 + tabOffSet)
            addToLine ('return "' +  stepNumber + '"', 2 + tabOffSet)

    else:
        addToError(functionId +" does not exist")

# creates code for going to url
def goToURL (stmt, stepNumber, tabOffSet = 0):
    global currentURL
    URL = stmt.find(STR_URL).text
    currentURL=URL
    addToLine ("url = \"" + URL +"\"", 1 + tabOffSet)
    addToLine ("if not (url.endswith(SLASH)):", 1 + tabOffSet)
    addToLine ("url += SLASH", 2 + tabOffSet)
    addToLine ("browser.visit(url)", 1 + tabOffSet)

# creates code for going to certain step
def goToStep(stmt, stepNumber, tabOffSet = 0, functionName=""):
    returnFunctionName = ""
    global gotoNodes
    
    goStepNumber = stmt.find(STR_STEPNUMBER).find(STR_INTEGER).text
    
    if (functionName == ""):
        returnFunctionName = "step"
    else:
        returnFunctionName = functionName + "_step"
        
    addToLine ("return " + returnFunctionName + goStepNumber+ "(browser,loop)" ,1 + tabOffSet)
    
    gotoNodes.append(returnFunctionName + goStepNumber)
    addToGraph(returnFunctionName+stepNumber,returnFunctionName + goStepNumber)

# handles stringExpr, returns python code
def stringExprHandler (strExpr):
    variant = getVariant(strExpr)
       
    if (variant == "0"):
        #STRING_LITERAL:String_literal
        return '"' +strExpr.find(STR_STRINGLITERAL).text + '"'
    elif (variant == "1"):
        #TEXT:Text FROM:From ObjectExpr:ObjectExpr
        obj = objectExprHandler(strExpr.find(STR_OBJECTEXPR))
        return obj + ".value"
    elif (variant == "2"):
        #TEXT:Text FROM:From ObjectExpr:ObjectExpr StrOperation:StrOperation StringExpr:StringExpr
        plus = strExpr.find(STR_PLUS)
        
        if (plus is not None):
            obj1 = objectExprHandler(strExpr.findall(STR_OBJECTEXPR)[0])
            obj2 = objectExprHandler(strExpr.findall(STR_OBJECTEXPR)[1])
            
            return obj1 + ".value + "+obj2+ ".value"
        else:
            addToError("strExpr variant 2 missing plus")
            return

    elif (variant == "3"):
        #STRING_LITERAL:String_literal StrOperation:StrOperation StringExpr:StringExpr;
        plus = strExpr.find(STR_PLUS)      
        
        if (plus is not None):
            if (len(strExpr.findall(STR_STRINGLITERAL))>1):
                return '"' +strExpr.findall(STR_STRINGLITERAL)[0].text + '"' + " + "+'"' +strExpr.findall(STR_STRINGLITERAL)[1].text + '"'
            else:
                obj = objectExprHandler(strExpr.find(STR_OBJECTEXPR))
                return '"' +strExpr.find(STR_STRINGLITERAL).text + '"' + " + "+obj+ ".value"
        else:
            addToError("strExpr variant 2 missing plus")
            return
    else:
        addToError("unhandled InterExpr")  

# provides code for entering string
def enterString (stmt, stepNumber, tabOffSet = 0):
    # TODO This needs to be polished
    objExpr = stmt.find(STR_OBJECTEXPR)
    obj = objectExprHandler(objExpr)

    if (stmt.find(STR_STRINGLITERAL) is not None):
        userInput = '"' + stmt.find(STR_STRINGLITERAL).text + '"'
    elif (stmt.find(STR_STRINGEXPR) is not None):
        userInput = (stringExprHandler(stmt.find(STR_STRINGEXPR)))
    
    addToLine (obj + '.type(' + userInput + ')', 1 + tabOffSet)

# handles integerExpr, returns python code
def integerExprHandler (intExpr):
    variant = getVariant(intExpr)
    
    if (variant == "0"):
        #INTEGER:Integer
        return '"' +intExpr.find(STR_INTEGER).text + '"'
    elif (variant == "1"):
        #NUMBER:Number FROM:From ObjectExpr:ObjectExpr
        obj = objectExprHandler(intExpr.find(STR_OBJECTEXPR))
        return obj + ".value"
    elif (variant == "2"):
        #NUMBER:Number FROM:From ObjectExpr:ObjectExpr IntOperation:IntOperation IntegerExpr:IntegerExpr
        plus = intExpr.find(STR_PLUS)
        minus = intExpr.find(STR_MINUS)
                
        obj1 = objectExprHandler(intExpr.findall(STR_OBJECTEXPR)[0])
        obj2 = objectExprHandler(intExpr.findall(STR_OBJECTEXPR)[1])
        
        if (plus is None):
            return "int("+obj1 + ".value"+ ") - int("+obj2+ ".value"+ ")"
        elif (minus is None):
            return "int("+obj1 + ".value"+ ") + int("+obj2+ ".value"+ ")"
        else:
            addToError("unhandled integerExpr variant:3")
    elif (variant == "3"):
        #INTEGER:Integer IntOperation:IntOperation IntegerExpr:IntegerExpr;
        plus = intExpr.find(STR_PLUS)
        minus = intExpr.find(STR_MINUS)
        
        # This checks for double int operation
        if (len(intExpr.findall(STR_INTEGER))>1):
            if (plus is None):
                return "int("+intExpr.findall(STR_INTEGER)[0].text+ ") - int("+intExpr.findall(STR_INTEGER)[1].text+ ")"
            elif (minus is None):
                return "int("+intExpr.findall(STR_INTEGER)[0].text+ ") + int("+intExpr.findall(STR_INTEGER)[1].text+ ")"
        else:               
            obj = objectExprHandler(intExpr.find(STR_OBJECTEXPR))
    
            if (plus is None):
                return "int("+intExpr.find(STR_INTEGER).text+ ") - int("+obj+ ".value"+ ")"
            elif (minus is None):
                return "int("+intExpr.find(STR_INTEGER).text+ ") + int("+obj+ ".value"+ ")"
            else:
                addToError(" unhandled integerExpr variant:3")
    else:
        addToError("unhandled InterExpr")
        
# provides code for entering integer        
def enterInteger (stmt, stepNumber, tabOffSet = 0 ):
    # TODO This needs to be extended
    objExpr = stmt.find(STR_OBJECTEXPR)
    obj = objectExprHandler(objExpr)
    if (stmt.find(STR_INTEGER) is not None):
        userInput = stmt.find(STR_INTEGER).text
        userInput = '"' + userInput + '"'
    else:
        intExpr = stmt.find(STR_INTEGEREXPR)
        userInput = "str(" + integerExprHandler(intExpr) + ")"
        
    
    addToLine (obj + '.type(' + userInput + ')', 1 + tabOffSet)

# provides code for clicking button
def clickButton (stmt, stepNumber, tabOffSet= 0 ):
    objExpr = stmt.find(STR_OBJECTEXPR)
    
    obj = objectExprHandler(objExpr)
    addToLine ("oldURL=browser.url", 1 + tabOffSet)
    addToLine (obj + ".click()", 1 + tabOffSet)
    addToLine ("sleep(1)", 1 + tabOffSet)
    addToLine ("d = 0", 1 + tabOffSet)
    addToLine ("newURL = browser.url", 1 + tabOffSet)
    addToLine ('while oldURL == newURL or browser.evaluate_script("document.readyState")!="complete":', 1 + tabOffSet)
    addToLine ("sleep(0.1)", 2 + tabOffSet)
    addToLine ("d+=1", 2 + tabOffSet)
    addToLine ("if d>1000:", 2 + tabOffSet)
    addToLine ('return "' + stepNumber +'"', 3 + tabOffSet)     

# provides code for reloading website
def reloadWebsite (stmt, stepNumber, tabOffSet= 0):
    addToLine ("browser.reload()", 1 + tabOffSet)

def checkCurrentURL (functionName, stepNumber):
    global currentURL
    if (currentURL=='' and functionName == ""):
        addToError("step " + str(stepNumber) + " cannot be ran before webpage is loaded")
        
# handles stmt and calls the corresponding function
def stmtHandler(stmt, stepNumber, tabOffSet = 0, functionName=""):
    variant = getVariant(stmt)
    graphFunctionName = functionName if functionName=="" else functionName+"_"
    
    if (variant == "0"):
        #DO:Do StepNumber:StepNumber IntegerTime:IntegerTime
        loopStep(stmt, stepNumber, tabOffSet, functionName)
        addToGraph(graphFunctionName+"step"+stepNumber,graphFunctionName+"step"+str(int(stepNumber)+1))
    elif (variant == "1"):
        #DO:Do ID:ID IntegerTime:IntegerTime
        addToGraph(graphFunctionName+"step"+stepNumber,graphFunctionName+"step"+str(int(stepNumber)+1))
        doFunction(stmt, stepNumber, tabOffSet, functionName)        
    elif (variant == "2"):
        #GO:Go TO:To URL:URL
        addToGraph(graphFunctionName+"step"+stepNumber,graphFunctionName+"step"+str(int(stepNumber)+1))
        goToURL(stmt, stepNumber, tabOffSet)        
    elif (variant == "3"):
        #GO:Go TO:To StepNumber:StepNumber
        goToStep(stmt, stepNumber, tabOffSet, functionName)        
    elif (variant == "4"):
        #ENTER:Enter StringExpr:StringExpr INTO:Into ObjectExpr:ObjectExpr
        addToGraph(graphFunctionName+"step"+stepNumber,graphFunctionName+"step"+str(int(stepNumber)+1))
        checkCurrentURL (functionName, stepNumber)
        enterString(stmt, stepNumber, tabOffSet) 
    elif (variant == "5"):
        #ENTER:Enter IntegerExpr:IntegerExpr INTO:Into ObjectExpr:ObjectExpr
        addToGraph(graphFunctionName+"step"+stepNumber,graphFunctionName+"step"+str(int(stepNumber)+1))
        checkCurrentURL (functionName, stepNumber)
        enterInteger(stmt, stepNumber, tabOffSet)        
    elif (variant == "6"):
        #CLICK:Click ObjectExpr:ObjectExpr
        addToGraph(graphFunctionName+"step"+stepNumber,graphFunctionName+"step"+str(int(stepNumber)+1))
        checkCurrentURL (functionName, stepNumber)
        clickButton (stmt, stepNumber, tabOffSet)           
    elif (variant == "7"):
        #REFRESH:Refresh ObjectExpr:ObjectExpr
        addToGraph(graphFunctionName+"step"+stepNumber,graphFunctionName+"step"+str(int(stepNumber)+1))
        checkCurrentURL (functionName, stepNumber)
        reloadWebsite (stmt, stepNumber, tabOffSet)
    else:
        addToError("unhandled stmt")
        
    addNewLineToLine()  

# handles if statements
def ifStmtHandler(ifStmt, stepNumber, functionName = ""):
    checkCurrentURL (functionName, stepNumber)
    objExpr = ifStmt.find(STR_OBJECTEXPR)
    obj = objectExprHandler(objExpr)
    stmt = ifStmt.find(STR_STMT)
    addToLine ("if len(" + obj + ")>0:", 1)
    stmtHandler (stmt, stepNumber, 1, functionName)
    graphFunctionName = functionName if functionName=="" else functionName+"_"
    if (ifStmt.find(STR_OTHERWISESTMT)):
        
        addToLine ("else:", 1)
        owStmt = ifStmt.find(STR_OTHERWISESTMT)
        #Only adds next step to graph if theres not two gotos
        if(not ( (getVariant(stmt)==3 or getVariant(stmt)==1) and (getVariant(owStmt)==3 or getVariant(owStmt)==1))):
            addToGraph(graphFunctionName+"step"+stepNumber,graphFunctionName+"step"+str(int(stepNumber)+1))
        elseStmt = owStmt.find(STR_STMT)
        stmtHandler (elseStmt, stepNumber, 1, functionName)
    else:
        addToGraph(graphFunctionName+"step"+stepNumber,graphFunctionName+"step"+str(int(stepNumber)+1))

# provides code for should have value
def shouldHaveValue (should, stepNumber):
    s = should.find(STR_STRINGLITERAL).text
    return ".value != '" + s + "':"

# provides code for should contain
def shouldContain (should, stepNumber):
    s = should.find(STR_STRINGLITERAL).text
    return '.find("' + s + '") == -1:'    

# provides code for should be URL
def shouldBeURL (should, stepNumber):
    url = should.find(STR_URL).text
    return "!= '"+url+"':"    
 
# handles shouldphrases
def shouldHandler (should, stepNumber):
    variant = getVariant(should)
    
    if (variant == "0"):
        #SHOULD:Should HAVE:Have VALUE:Value STRING_LITERAL:String_literal
        return shouldHaveValue (should, stepNumber)
    elif (variant == "1"):
        #SHOULD:Should CONTAIN:Contain STRING_LITERAL:String_literal
        return shouldContain (should, stepNumber)
    elif (variant == "2"):
        #SHOULD:Should BE:Be URL:URL;
        return shouldBeURL (should, stepNumber)
    else:
        addToError("unhandled shouldphrase: " + stepNumber)
 
# handles result
def resultHandler(result, stepNumber, functionName = ""):
    variant = getVariant(result)

    graphFunctionName = functionName if functionName=="" else functionName+":"
    
    if (variant == "0"):
        #ObjectExpr:ObjectExpr ShouldPhrase:ShouldPhrase
        objExpr = result.find(STR_OBJECTEXPR)
        obj = objectExprHandler(objExpr)       
        should = result.find(STR_SHOULDPHRASE)   
        
        addToLine ("if " + obj + shouldHandler(should, stepNumber), 1)
        addToLine ('return "' + graphFunctionName +  stepNumber +'"', 2)
        addNewLineToLine()  
    #elif (variant == "1"): do nothing

# creates code for the last return statement of the function
def stepLastReturn (num, functionName = ""):          
    addToLine ("if loop:", 1)
    addToLine ("return", 2)

    returnFunctionName = ""
    if (functionName == ""):
        returnFunctionName = "step"
        
    else:
        returnFunctionName = functionName + "_step"

    if (num != ""):
        addToLine ("return " + returnFunctionName + num + "(browser, loop)", 1)
    else:
        addToLine ("return", 1)
    addNewLineToLine()  

def checkIfParentIsLoop(child):
    if child not in childParentGraph: #does not have parent
        return True
    for parent in childParentGraph[child]:
        if parent in loopNodes:
            return True
        if parent == "" or "step" not in parent:
            return True
    return False
        
# Handles step
def stepHandler (setOfSteps, functionName = ""):
    stepSize = len(setOfSteps.getchildren())
    stepCount = 0
    previousStep=0
    for step in setOfSteps:
        stepLine = step.find(STR_STEPLINE)
        stepNumber = stepLine.find(STR_STEPNUMBER)
        numLiteral = stepNumber.find(STR_INTEGER).text
        graphFunctionName = functionName if functionName=="" else functionName+"_"

        #checks if the node is live, if its not just skip the step, if live nodes is empty then it goes ahead with the step
        if ((graphFunctionName+"step"+numLiteral) in liveNodes or len(liveNodes)==0):
            
            if(int(numLiteral)<previousStep):
                addToError("step order is off in "+functionName+ " step "+numLiteral)
            previousStep=int(numLiteral)

            #TODO check graph check loop

            
            if((graphFunctionName+"step"+numLiteral) in loopNodes or (graphFunctionName+"step"+numLiteral) in gotoNodes or checkIfParentIsLoop(graphFunctionName+"step"+numLiteral)):
                addToLine(createDef(numLiteral, functionName))   

                   
            
            stepLineVariant = getVariant(stepLine)
            
            #stmt
            if (stepLineVariant == "0"): 
                stmt = stepLine.find(STR_STMT)
                result = stepLine.find(STR_RESULT)
                
                if (stmt is None and stepLine.find(STR_EXIT) is not None):  
                    addToLine ("return", 1)
                    addNewLineToLine()  
                elif (stmt is None):
                    addToError("unhandled special stmt case")
                else:              
                    stmtHandler(stmt, numLiteral,0, functionName)
                    resultHandler(result, numLiteral, functionName)
    
            #ifstmt  
            elif (stepLineVariant == "1"):       
                ifStmt = stepLine.find(STR_IFSTMT)
                ifStmtHandler(ifStmt,numLiteral, functionName)
            
            stepCount += 1
            
            if ((graphFunctionName+"step"+str(int(numLiteral)+1)) not in concatList):
                #this is to prevent calling functions that are dead and have been removed
                if (stepCount < stepSize and (graphFunctionName+"step"+str(int(numLiteral)+1)) in liveNodes):
                    if((graphFunctionName+"step"+numLiteral) in loopNodes or (graphFunctionName+"step"+str(int(numLiteral)+1)) in loopNodes or (graphFunctionName+"step"+str(int(numLiteral)+1)) in gotoNodes):
                        stepLastReturn(str(int(numLiteral) + 1), functionName)
                else:
                    stepLastReturn("")
 
# error checking can be implemented here
# To check for XX.fine ("") == None, if the object does not exist
def mainClassHandler (mainClass,functionName = ""):   
    setOfSteps = mainClass.find (STR_SETOFSTEPS)
    firstStep = setOfSteps.find(STR_STEP)
    firstStepLine = firstStep.find(STR_STEPLINE)
    firstStepNumber = firstStepLine.find(STR_STEPNUMBER)
    StepNumber = firstStepNumber.find(STR_INTEGER).text
    
    createFirstStepFunction(functionName,StepNumber)
    stepHandler(setOfSteps)

# DEBUG: check if the element is None
def checkXMLElement (e, eName):
    if (e is None):
        print ("WARNING: " + eName + " is None")
        
# DEBUG: prints out the child elements
def xmlTest (xml):
    for child in xml:
        print(child)

# handles set of functions
def setOfFunctionsHandler(setOfFunctions):
    for function in setOfFunctions:
        functionID = function.find (STR_ID).text
        functionNames.append(functionID)
        setOfSteps = function.find(STR_SETOFSTEPS)
        firstStep = setOfSteps.find(STR_STEP)
        firstStepLine = firstStep.find(STR_STEPLINE)
        firstStepNumber = firstStepLine.find(STR_STEPNUMBER)
        StepNumber = firstStepNumber.find(STR_INTEGER).text
        createFirstStepFunction(functionID, StepNumber)
        stepHandler(setOfSteps, functionID)

# creates the checkSteps() functions
def createCheckStepsFunction():
    addToLine("def checkSteps():", 0)
    addToLine("browser=Browser('chrome')", 1)
    addToLine("err = step(browser)", 1)
    addToLine("#program is done", 1)
    addToLine("browser.quit()", 1)    
    addToLine("#return the failed step", 1)
    addToLine("if not (err == None) and not (err.isspace()) and not (len(err) == 0):", 1)
    addToLine('return "Program failed on step: " + err + "\\n"', 2)    
    addToLine('return "The testcase passed"', 1)
    addNewLineToLine()

# creates the main functions
def createMainFunction():
    addToLine("if __name__ == '__main__':")
    addToLine("print(checkSteps())", 1)
    addNewLineToLine()

def printWarnings():
    global usedFunctions
    global functionNames
    
    for func in functionNames :
            if (func not in  usedFunctions and len(liveNodes)==0):
                addToLine("print(\"WARNING: " + func +" was removed because it was never used.\")",1)
                print ("WARNING: " + func +" was removed because it was never used.")
                
def checkErrors():
    global outputCode
    global errorText
    if (errorText!=""):
        outputCode = ""
        addToLine ("if __name__ == '__main__':")
        outputCode +=errorText


def compileXMLtoPython (xmlPath = 'concatCodeTest01.html.xml', outputFileName = 'compiledCode.py',preprocessorFileName = ''):
    root = getTreeRoot('../../outputs/' + xmlPath)
    addPreprocessorLines(preprocessorFileName)


    createInitialBlock(preprocessorFileName)
    
    if (root.tag == STR_PROGRAM):
        for child in root:
            childTag = child.tag
            
            if (child.tag == STR_SETOFFUNCTIONS):
                setOfFunctionsHandler(child)
    
    if (root.tag == STR_PROGRAM):
        for child in root:
            childTag = child.tag
            
            if (childTag == STR_MAINCLASS):
                mainClassHandler(child)
                
    createCheckStepsFunction()
    createMainFunction()

    #Error checking
    checkErrors()
    printWarnings()
    
    f = open('../../outputs/CompiledCode/' + outputFileName, 'w+')
    f.write("")
    f.write(outputCode)
    f.close
  
#from http://eddmann.com/posts/depth-first-search-and-breadth-first-search-in-python/
def bfs(graph, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            if (vertex in graph):
                queue.extend(graph[vertex] - visited)
    return visited    
    
# MAIN FUNCTION
if (__name__ == "__main__"):
    if (len(sys.argv) == 3):
        xmlLocation = sys.argv[1]
        outputFileName= sys.argv[2]
        compileXMLtoPython(xmlLocation, outputFileName)
    elif (len(sys.argv) == 4):
        xmlLocation = sys.argv[1]
        outputFileName= sys.argv[2]
        preprocessorFileName= sys.argv[3]
        compileXMLtoPython(xmlLocation, outputFileName,preprocessorFileName)
    else:
        compileXMLtoPython()
        
    '''
    for k, v in graph.items():
        print(k, v)

    print ("==============")        
    print (loopNodes)
    print ("==============")        
    '''
    #global liveNodes
    liveNodes = bfs(graph,"")
    childParentGraph = {}
    for k, v in graph.items():
        for i in v:
            if(i in childParentGraph):
                childParentGraph[i].add(k)
            else:
                childParentGraph[i]=set([k])
    
    #global functionNames
    functionNames=[]
    
    #global usedFunctions
    usedFunctions=[]
    
    #global stepsDefined
    stepsDefined=[]
    
    #global stepsUsed
    stepsUsed=[]

    #global errorText
    errorText=''
    
    #global currentURL
    currentURL=''
    
    #global graph
    #graph = {}
    
    #global outputCode
    outputCode=""
    
    #global preprocessorDic
    preprocessorDic = {}

    if (len(sys.argv) == 3):
        xmlLocation = sys.argv[1]
        outputFileName= sys.argv[2]
        compileXMLtoPython(xmlLocation, outputFileName)
    elif (len(sys.argv) == 4):
        xmlLocation = sys.argv[1]
        outputFileName= sys.argv[2]
        preprocessorFileName= sys.argv[3]
        compileXMLtoPython(xmlLocation, outputFileName,preprocessorFileName)
    else:
        compileXMLtoPython()


    #define setOfSteps
    #define setofFunctions
    
    #define createStep(functionname = "") that creates step(browser, loop = false), or function_step if param is provided.
    #return the first step
    
    #define createStepFunc (functionname = "") run everysingle step, calls step function
    
    #define statemenFunct ()
    
    
    #
    #
    
