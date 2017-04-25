from splinter import Browser
from time import sleep

SLASH = "/"

def refreshwebpage_step (browser, loop = False):
	return refreshwebpage_step1(browser, loop)

def refreshwebpage_step1(browser, loop = False):
	browser.reload()

	if browser.url!= 'https://www.youtube.com/results?search_query=test':
		return "refreshwebpage:1"

	return refreshwebpage_step6(browser,loop)

	if loop:
		return
	return

def step (browser, loop = False):
	return step1(browser, loop)

def step1(browser, loop = False):
	url = "https://www.youtube.com/"
	if not (url.endswith(SLASH)):
		url += SLASH
	browser.visit(url)

	if browser.url!= 'https://www.youtube.com/':
		return "1"

	if len(browser.find_by_id("search-btn"))>0:
		return step8(browser,loop)

	else:
		return step9(browser,loop)

	if loop:
		return
	return step3(browser, loop)

def step3(browser, loop = False):
	return step10(browser,loop)

	if loop:
		return
	return

def step8(browser, loop = False):
	for c in range (5):
		err=refreshwebpage_step(browser, loop=True)
		if not (err == None) and not (err.isspace()) and not (len(err) == 0):
			return "8"

	if loop:
		return
	return step9(browser, loop)

def step9(browser, loop = False):
	browser.find_by_id("masthead-search-term").first.type(str(int(6) - int(2)))

	if loop:
		return
	return step10(browser, loop)

def step10(browser, loop = False):
	return

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

