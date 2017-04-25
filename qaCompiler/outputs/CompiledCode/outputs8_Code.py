from splinter import Browser
from time import sleep

SLASH = "/"

def step (browser, loop = False):
	return step1(browser, loop)

def step1(browser, loop = False):
	return step3(browser,loop)

	if loop:
		return
	return step2(browser, loop)

def step2(browser, loop = False):
	browser.find_by_id("Search").first.type("test")

	if browser.find_by_id("Search").first.value != 'test':
		return "2"

	if loop:
		return
	return step3(browser, loop)

def step3(browser, loop = False):
	oldURL=browser.url
	browser.find_by_id("Google").click()
	sleep(1)
	d = 0
	newURL = browser.url
	while oldURL == newURL or browser.evaluate_script("document.readyState")!="complete":
		sleep(0.1)
		d+=1
		if d>10000:
			return "3"

	if browser.url!= 'http://www.google.ca/':
		return "3"

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

