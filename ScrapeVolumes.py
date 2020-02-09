import csv, glob, re, os, pickle
import pandas as pd
from WSJ_Classes import Issue
import numpy as np
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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

def get_ToC_from_volume(vol_page):
	url = vol_page
	wd = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver'))
	wd.get(url)

	sleep(1)

	# click buttons, three times
	python_button = wd.find_elements_by_css_selector('.disclosuretriggerDelayArea')
	click_buttons(python_button)
	sleep(10)
	python_button = wd.find_elements_by_css_selector('.disclosuretriggerDelayArea')
	click_buttons(python_button)
	sleep(10)
	python_button = wd.find_elements_by_css_selector('.disclosuretriggerDelayArea')
	click_buttons(python_button)
	sleep(10)

	links = wd.find_elements_by_css_selector('.metatable')

	# get date using regex on metadata table
	for data in links:
		pattern = r"(公開年月日)(.*)(\n)"  # "date issued"
		g = re.search(pattern, data.text)
		if g:
			date = g.group(2).strip()

	# instantiate the WSJ Issue with date
	issue = Issue(date)

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

	# fill in Issues
	issues = []
	for url in volumes:
		issue = get_ToC_from_volume(url)
		issues.append(issue)

	# print to view
	for issue in issues:
		print(issue.get_date())
		print(issue.get_titles())
		print(issue.get_sections())

	# save issues into pickle
	with open('WSJ_issues.pickle', 'wb') as f:
		pickle.dump(issues, f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
	main()
