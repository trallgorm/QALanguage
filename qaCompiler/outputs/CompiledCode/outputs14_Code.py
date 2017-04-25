from splinter import Browser
from time import sleep

SLASH = "/"

def step (browser, loop = False):
	return step1(browser, loop)

def step1(browser, loop = False):
	browser.find_by_id("Search").first.type(browser.find_by_id("InputA").first.value + browser.find_by_id("InputB").first.value)

	if loop:
		return
	return

def checkSteps():
	browser=Browser('chrome')
	err = step(browser)
	#program is done
	browser.quit()
	#return the failed step
	if not (err == None) and not (err.isspace()) and not (len(err) == 0):
		return "Program failed on step: " + err + "\n"
	return "The testcase passed"

if __name__ == '__main__':
	print(checkSteps())

