import pickle, os, csv, glob, re
from WSJ_Classes import Issue
from datetime import datetime
import pandas as pd

# takes Issue object and return data frame with issue date, manga title, and relative rankings
def df_from_issue(WSJ_issue):
	issue = WSJ_issue
	titles = issue.get_titles()
	details = issue.get_details()
	vol_pages = issue.get_pages()
	start_pages = get_page_numbers(details)  # get page number from detail text
	num_color = get_num_color_pages(details) # get number of color pages (default 0)

	# make a df from columns.
	df = pd.DataFrame(list(zip(titles, details, num_color, start_pages)), columns = ['manga', 'details', 'num_color', 'start_page'])
	df = df.sort_values(by = ['start_page']) # sort by page order
	df['num_pages'] = list(df.start_page.diff()[1:]) + [int(vol_pages)-int(df.start_page[-1:])] # row diff of start page, shifted down. for last entry, subtract from total pages in volume.
	df['issue_date'] = [datetime.strptime(issue.get_date(), '%Y-%m-%d')] * len(df)
	df['issue_no'] = [issue.get_issue()] * len(df)

	return df

def get_page_numbers(details):
	# get page numbers by regex in details text
	pg = []
	for item in details:
		x = re.findall(r'[0-9]*\.[0-9]', item)
		num = float(x[-1]) # make page number string into int (last match is always pg#)
		pg.append(num)

	return pg

def get_num_color_pages(details):
	num_colors = []
	for item in details:
		x = re.search('色カラー', item) # search for the term "色カラー"
		if x is not None:   # if there is a color page
			num_colors.append(item[x.start()-1])  # number before "色カラー" indicating number of color pages
		else:
			num_colors.append(0)  # otherwise, no color pages

	return num_colors

def issues_to_df(issues):
	df = pd.DataFrame()
	# for each issue, get information out and place into a data frame
	for issue in issues:
		df = df.append(df_from_issue(issue))  # creates a DataFrame from Issue class

	return df

def main():
	# open data as list of WSJ Issue class.
	with open('WSJ_issues_310521.pickle', 'rb') as f:
		issues = pickle.load(f)

	df = issues_to_df(issues)

	# saves data for only manga works
	manga_df = df[df['details'].str.contains('マンガ作品')]
	manga_df = df.drop_duplicates(['manga', 'issue_date']) # TEMPORARY SOLUTION: NEED TO ADD TOTAL NUMBER OF PAGES TOGETHER, COLOR BINARY, ETC.

	manga_df.to_csv('WSJ_data.csv')

if __name__ == '__main__':
	main()
