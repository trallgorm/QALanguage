from splinter import Browser
from time import sleep

SLASH = "/"

def step (browser, loop = False):
	return step1(browser, loop)

def step1(browser, loop = False):
	if len(browser.find_by_id("Google Search"))>0:
		browser.find_by_id("Search").first.type("test")

	else:
		oldURL=browser.url
		browser.find_by_id("Google").click()
		sleep(1)
		d = 0
		newURL = browser.url
		while oldURL == newURL or browser.evaluate_script("document.readyState")!="complete":
			sleep(0.1)
			d+=1
			if d>10000:
				return "1"

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

