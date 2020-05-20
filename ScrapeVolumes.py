import csv, glob, re, os, pickle, logging
import pandas as pd
from WSJ_Classes import Issue
import numpy as np
from time import sleep
from selenium import webdriver
logging.basicConfig(filename='missing_vols.log',level=logging.WARNING)


# click all buttons on a page
def click_buttons(buttons_list):
	for button in buttons_list:
		try:
			button.click()
		except Exception:
			continue

# get initial page
def get_wsj_collection(webpage):
	# open page and select links
	url = webpage
	wd = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'))
	wd.get(url)

	sleep(5)
	# expanding the drop down menus, must click twice to reveal all
	python_button = wd.find_elements_by_css_selector('.disclosuretriggerDelayArea')
	click_buttons(python_button)
	sleep(15)

	python_button = wd.find_elements_by_css_selector('.disclosuretriggerDelayArea')
	click_buttons(python_button)
	sleep(15)

	volumes = []
	links = wd.find_elements_by_css_selector('.resultitemanchor')
	for link in links:
		volumes.append(link.get_attribute('href'))

	wd.close()

	return volumes

def get_ToC_from_volume(vol_url):
	url = vol_url
	wd = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'))
	wd.get(url)

	sleep(1)

	# click buttons, three times
	python_button = wd.find_elements_by_css_selector('.disclosuretriggerDelayArea')
	click_buttons(python_button)
	sleep(5)
	python_button = wd.find_elements_by_css_selector('.disclosuretriggerDelayArea')
	click_buttons(python_button)
	sleep(5)
	python_button = wd.find_elements_by_css_selector('.disclosuretriggerDelayArea')
	click_buttons(python_button)
	sleep(5)


	# get date using regex on metadata table
	links = wd.find_elements_by_css_selector('.metatable')
	for data in links:

		pattern = r"(公開年月日)(.*)(\n)"  # "date issued"
		g = re.search(pattern, data.text)
		if g:
			date = g.group(2).strip()

		pattern = r"(ページ数)(.*)(\n)"  # "total number of pages"
		p = re.search(pattern, data.text)
		if p:
			pages = p.group(2).strip()[:-1]

	# instantiate the WSJ Issue with date and url
	issue = Issue(date, pages, url)

	# fill section titles
	links = wd.find_elements_by_css_selector('.resultiteminfo-magazine .title')
	for title in links:
		issue.add_section_title(title.text)

	# fill section details
	links = wd.find_elements_by_css_selector('.supplement')
	for detail in links:
		issue.add_section_detail(detail.text)

	wd.close()

	return issue


def main():
	# get list of urls of all WSJ volumes
	volumes = get_wsj_collection(webpage = 'https://mediaarts-db.bunka.go.jp/id/C119459')
	print(volumes)

	# fill in Issues. [date, url, titles, details]
	issues = []
	missing = []
	for url in volumes[-200:-150]:
		print('volume index number: ' + str(volumes.index(url)))
		try:
			issue = get_ToC_from_volume(url)
			issues.append(issue)
		except:
			logging.warning('volume index: ' + str(volumes.index(url)) + ' and url: ' + str(url))



	# save collection of Issues into pickle
	with open('WSJ_issues.pickle', 'wb') as f:
		pickle.dump(issues, f, pickle.HIGHEST_PROTOCOL)



if __name__ == '__main__':
	main()
