import requests
from bs4 import BeautifulSoup

PROGRAMMERS_URL = 'https://programmers.co.kr/job?_=1598625231768&job_position%5Btags%5D%5B%5D=Python'


# 페이지 번호 뽑기
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


# 잡 서칭
def extract_job(html):
    position_title = html.find("h5", {"class": "position-title"}).find("a")
    title = position_title.string
    company = html.find("h6", {"class": "company-name"}).string
    company_info = html.find("ul", {"class": "company-info"})
    experience = company_info.find("li", {"class": "experience"}).text.strip()
    location = company_info.find("li", {"class": "location"})
    if location in company_info:
        location = location.text.strip()
    else:
        location = '장소 불문'
    job_link = position_title["href"]

    return {
        'title': title,
        'company': company,
        'experience': experience,
        'location': location,
        'job_link': f"https://programmers.co.kr{job_link}"
    }


# 배열에 담아서 여러 개
def extract_programmers_jobs(last_pages):
  jobs = []
  for page in range(1, last_pages + 1):
    print(f"{page} 페이지 프로그래머스 구인 광고를 크롤링 중입니다...")
    result = requests.get(f"{PROGRAMMERS_URL}&page={page}")
    soup = BeautifulSoup(result.text, "html.parser")
    li = soup.find_all("li", {"class": "list-position-item"})
    for content in li:
        job = extract_job(content)
        jobs.append(job)
  return jobs

# 최종 값
def get_jobs():
  last_page = extract_programmers_pages()
  jobs = extract_programmers_jobs(last_page)
  return jobs