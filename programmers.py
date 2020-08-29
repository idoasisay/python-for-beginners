import requests
from bs4 import BeautifulSoup

PROGRAMMERS_URL = 'https://programmers.co.kr/job?_=1598625231768&job_position%5Btags%5D%5B%5D=Python'

def extract_programmers_pages():
  result = requests.get(PROGRAMMERS_URL)
  soup = BeautifulSoup(result.text, "html.parser")

  pagination = soup.find("ul", {"class": "pagination"})
  pages = pagination.find_all("a", {"class": "page-link"})[1:-1]

  count = 0
  for link in pages:
    pages[count] = int(link.string)
    count += 1

  max_page = pages[-1]
  return max_page

def extract_programmers_jobs(last_pages):
  jobs = []
  for page in range(1, last_pages + 1):
    result = requests.get(f"{PROGRAMMERS_URL}&page={page}")
    soup = BeautifulSoup(result.text, "html.parser")
    li = soup.find_all("li", {"class": "list-position-item"})
    for content in li:
      title = content.find("h5", {"class": "position-title"}).find("a").string
      company = content.find("h6", {"class": "company-name"}).string
      print(title, company)

  return jobs
