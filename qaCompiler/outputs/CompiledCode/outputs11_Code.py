from splinter import Browser
from time import sleep

SLASH = "/"

def step (browser, loop = False):
	return step1(browser, loop)

def step1(browser, loop = False):
	url = "https://www.google.ca/"
	if not (url.endswith(SLASH)):
		url += SLASH
	browser.visit(url)

	if browser.url!= 'http://www.google.ca/':
		return "1"

	if loop:
		return
	return step2(browser, loop)

def step2(browser, loop = False):
	browser.reload()

	if browser.url!= 'http://www.google.ca/':
		return "2"

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

