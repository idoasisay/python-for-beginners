import requests
from bs4 import BeautifulSoup

SARAMIN_URL = 'http://www.saramin.co.kr/zf_user/jobs/list/job-category?page=1&cat_key=40426&search_optional_item=n&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle'


# 마지막 페이지를 구해서
def get_last_page():
    so_api = requests.get(SARAMIN_URL)
    soup = BeautifulSoup(so_api.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"}).find_all("a")
    last_page = int(pagination[-1].get_text(strip=True))
    return last_page


def extract_job(html):
    company = html.find("div", {"class": "company_nm"}).find("a")["title"]
    company_info = html.find("div", {"class": "notification_info"})
    title = company_info.find("a")["title"]
    location = html.find("div", {
        "class": "company_info"
    }).find("p", {
        "class": "work_place"
    }).string
    experience = html.find("div", {
        "class": "recruit_condition"
    }).find("p").string
    job_link = company_info.find("a")["href"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "experience": experience,
        "job_link": f"http://www.saramin.co.kr/{job_link}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(1, last_page + 1):
        print(f"{page} 페이지 구인 광고를 크롤링 중입니다...")
        so_api = requests.get(
            f"http://www.saramin.co.kr/zf_user/jobs/list/job-category?page={page}&cat_key=40426&search_optional_item=n&search_done=y&panel_count=y&isAjaxRequest=0&page_count=50&sort=RL&type=job-category&is_param=1&isSearchResultEmpty=1&isSectionHome=0&searchParamCount=1#searchTitle"
        )
        soup = BeautifulSoup(so_api.text, "html.parser")
        li = soup.find_all("div", {"class": "list_item"})
        for content in li:
            job = extract_job(content)
            jobs.append(job)
    print(jobs)
    return jobs


# 마지막 페이지를 토대로 크롤링
def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs
