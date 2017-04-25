from splinter import Browser
from time import sleep

SLASH = "/"

def refreshwebpage_step (browser, loop = False):
	return refreshwebpage_step1(browser, loop)

def refreshwebpage_step1(browser, loop = False):
	browser.reload()

	if browser.url!= 'https://www.youtube.com/results?search_query=test':
		return "1"

	if loop:
		return
	return refreshwebpage_step2(browser, loop)

def refreshwebpage_step2(browser, loop = False):
	return refreshwebpage_step6(browser,loop)

	if loop:
		return
	return

def refresh13_step (browser, loop = False):
	return refresh13_step1(browser, loop)

def refresh13_step1(browser, loop = False):
	browser.reload()

	if browser.url!= 'https://www.youtube.com/results?search_query=test':
		return "1"

	if loop:
		return
	return refresh13_step2(browser, loop)

def refresh13_step2(browser, loop = False):
	return

	if loop:
		return
	return refresh13_step3(browser, loop)

def refresh13_step3(browser, loop = False):
	return refresh13_step1(browser,loop)

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

	if loop:
		return
	return step2(browser, loop)

def step2(browser, loop = False):
	browser.find_by_id("masthead-search-term").first.type("test")

	if browser.find_by_id("masthead-search-term").first.value != 'test':
		return "2"

	if loop:
		return
	return step3(browser, loop)

def step3(browser, loop = False):
	if len(browser.find_by_id("search-btn"))>0:
		return step5(browser,loop)

	else:
		return step4(browser,loop)

	if loop:
		return
	return step4(browser, loop)

def step4(browser, loop = False):
	return

	if loop:
		return
	return step5(browser, loop)

def step5(browser, loop = False):
	oldURL=browser.url
	print(22)
	browser.find_by_id("search-btn").first.click()
	print(23)
	sleep(1)
	d = 0
	newURL = browser.url
	while oldURL == newURL or browser.evaluate_script("document.readyState")!="complete":
		sleep(0.1)
		d+=1
		if d>10000:
			return "5"

	if browser.html.find("Talko") == -1:
		return "5"

	if loop:
		return
	return step6(browser, loop)

def step6(browser, loop = False):
	browser.reload()

	if browser.url!= 'https://www.youtube.com/results?search_query=test':
		return "6"

	if loop:
		return
	return step7(browser, loop)

def step7(browser, loop = False):
	for c in range (10):
		err=step6(browser, loop=True)
		if not (err == None) and not (err.isspace()) and not (len(err) == 0):
			return "7"

	if loop:
		return
	return step8(browser, loop)

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
	browser.find_by_id("masthead-search-term").first.type("doogaga" + "doo")

	if loop:
		return
	return step11(browser, loop)

def step11(browser, loop = False):
	return step3(browser,loop)

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

	print("WARNING: refresh13 is never used")
