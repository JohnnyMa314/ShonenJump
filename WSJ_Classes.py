class Issue:
	def __init__(self, date, pages, url):
		self.date = date
		self.pages = pages
		self.url = url
		self.section_titles = []
		self.section_details = []

	def get_date(self):
		return self.date

	def get_pages(self):
		return self.pages

	def get_url(self):
		return self.url

	def add_section_title(self, title):
		self.section_titles.append(title)

	def get_titles(self):
		return self.section_titles

	def add_section_detail(self, detail):
		self.section_details.append(detail)

	def get_details(self):
		return self.section_details

	def get_sections(self):
		return list(map(lambda x, y: (x, y), self.section_titles, self.section_details))

