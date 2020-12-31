import csv, glob, re, os, pickle, logging
import pandas as pd
from WSJ_Classes import Issue
import numpy as np
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
	options = Options()
	options.headless = True
	wd = webdriver.Chrome(options=options)
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

	options = Options()
	options.headless = True
	wd = webdriver.Chrome(options=options)
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
	tables = wd.find_elements_by_css_selector('.metatable')
	date = 'N/A'
	pages = 'N/A'
	for data in tables:
		pattern = r"(公開年月日)(.*)(\n)"  # "date issued"
		g = re.search(pattern, data.text)
		if g:
			date = g.group(2).strip()

		pattern = r"(ページ数)(.*)(\n)"  # "total number of pages"
		p = re.search(pattern, data.text)
		if p:
			pages = p.group(2).strip()[:-1]

	# get year and issue number from title of magazine
	top = wd.find_elements_by_css_selector('.dipTopTitleField')
	year_pat = r'[0-9]{4}'
	issue_pat = r'(表示号数)(.*)'
	y = re.search(year_pat, top[0].text)
	i = re.search(issue_pat, top[0].text)
	if y and i:
		issue_no = y.group().strip() + ' #' + i.group(2).strip()
	else:
		issue_no = 'N/A'

	# instantiate the WSJ Issue with date and url
	issue = Issue(issue_no, date, pages, vol_url)

	# fill section titles
	links = wd.find_elements_by_css_selector('.resultiteminfo-magazine .title')
	for title in links:
		issue.add_section_title(title.text)

	# fill section details
	links = wd.find_elements_by_css_selector('.supplement')
	for detail in links:
		issue.add_section_detail(detail.text)

	# check if manga list is empty
	if len(links) == 0:
		raise Exception

	wd.close()

	return issue

def fill_issue_data(url_list):
	# instantiate logging item
	logging.basicConfig(filename='missing_volume_urls.log', level=logging.WARNING)

	issues = []
	for url in url_list:
		print('volume index number: ' + str(url_list.index(url)))
		try:
			issue = get_ToC_from_volume(url)
			issues.append(issue)
			print('sucessfully added')
		except:
			print('failed to add')
			logging.warning('volume index: ' + str(url_list.index(url)) + ' and url: ' + str(url))

	return issues

def main():
	# get list of urls of all WSJ volumes
	volume_urls = get_wsj_collection(webpage = 'https://mediaarts-db.bunka.go.jp/id/C119459')
	print(volume_urls)

	issues = fill_issue_data(volume_urls)
	# save collection of Issues into pickle
	with open('WSJ_issues_090620.pickle', 'wb') as f:
		pickle.dump(issues, f, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
	main()
