from splinter import Browser

SLASH = "/"

def step(browser):
    return step1(browser)

def step1(browser):
    url=r"C:/Users/Bzr/Dropbox/4th%20year/compiler/qa/Sprint2/test.html"

    browser.visit(url)
    #Checking Step 1
    if browser.url != url:
        print (browser.url)
        print (url)
        return step2(browser)

def step2(browser):
    strConcat = browser.find_by_id("1").first.value + browser.find_by_id("4").first.value
    browser.find_by_id("userInput").type(strConcat)

    return step3(browser)

def step3(browser):
    numCalc = float(browser.find_by_id("num1").first.value) - float(browser.find_by_id("num2").first.value)
    
    browser.find_by_id("userInput").type(str(numCalc))

    return

def checkSteps():
    browser=Browser('chrome')
    err = step(browser);

    #program is done
    #browser.quit()

    #return the errors if exist
    if not (err == None) and not (err.isspace()) and not (len(err) == 0):
        return "Program failed on step: " + err + "\n"
        
    return ("Program finished executed without errors.")

if __name__ == '__main__':
    print(checkSteps())
