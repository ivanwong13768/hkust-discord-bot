from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import *
from bs4 import BeautifulSoup

# TODO: implement this
def parse_req_string(req_string: str) -> list:
    pass

# what if we use tree instead of pure lists
# class Tree:
#     pass

class Course:
    name = ""
    pre_req = []
    co_req = []
    exclusion = []
    
    def __init__(self, name: str, pre_req: str = "", co_req: str = "", exclusion: str = ""):
        self.name = name
        self.pre_req = parse_req_string(pre_req)
        self.co_req = parse_req_string(co_req)
        self.exclusion = parse_req_string(exclusion)
        
    def can_reg(self, course_list: list):
        pre_req_fulfilled = all([pr.__fulfills(course_list) if type(pr) == Or or type(pr) == And else pr in course_list for pr in self.pre_req])
        co_req_fulfilled = all([cr.__fulfills(course_list) if type(cr) == Or or type(cr) == And else cr in course_list for cr in self.co_req])
        exclusion_fulfilled = not any([ex.__fulfills(course_list) if type(ex) == Or or type(ex) == And else ex in course_list for ex in self.exclusion])
        return pre_req_fulfilled and co_req_fulfilled and exclusion_fulfilled


class Or:
    courses = []
    
    def __init__(self, courses: list):
        self.courses = courses
    
    def __fulfills(self, course_list: list):
        return any([c in course_list for c in self.courses])
        
        
class And:
    courses = []
    
    def __init__(self, courses: list):
        self.courses = courses

    def __fulfills(self, course_list: list):
        return all([c in course_list for c in self.courses])


# this function should return all the courses, idk in what form tho
def scrape():
    # headless mode, remove GUI
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options = options)
    try:
        # TODO:
        # - get different semesters and store them in files
        # - extract elements using selenium instead of painful bs4
        driver.get("https://w5.ab.ust.hk/wcq/cgi-bin/2430/")
        # driver.find_element(By.PARTIAL_LINK_TEXT, "")
        html = driver.page_source
        # input() # hold webdriver until key input
    finally:
        driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    courses_html = soup.find_all('div', class_= 'course')
    for course_html in courses_html:
        course_name = course_html.find('div', class_ = 'subject')
        pop_up_detail = course_html.find('div', class_ = 'popupdetail')
        course_detail = pop_up_detail.find('table')
        # print(course_detail)