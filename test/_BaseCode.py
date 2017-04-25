from splinter import Browser

SLASH = "/"

def step(browser):
    return 

def checkSteps():
    browser=Browser('chrome')
    err = step(browser);

    #program is done
    browser.quit()

    #return the errors if exist
    if not (err == None) and not (err.isspace()) and not (len(err) == 0):
        return "Program finished executed, but it contains errors: \n" + err
        
    return ("Program finished executed without errors.")

if __name__ == '__main__':
    print(checkSteps())
