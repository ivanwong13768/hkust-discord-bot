from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import *
from bs4 import BeautifulSoup
import re

# TODO: implement this
def parse_course_name(course_name_string: str) -> tuple[str, str, int]:     # course code, course name, credit count
    temp = course_name_string.split(' - ')
    course_code = temp[0][:4] + temp[0][5:]
    course_name = ' - '.join(temp[1:]).split(' (')[0]
    credit = int(re.search("[0-9] units{0,1}", course_name_string)[0][0])
    return (course_code, course_name, credit)

# TODO: implement this
def parse_req_string(req_string: str) -> list:
    brackets = re.findall("\(.*\)", req_string)
    # idea: recursively deal with brackets -> return and append back to tree?
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
def scrape() -> list:
    # headless mode, remove GUI
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options = options)
    try:
        # TODO:
        # - get different semesters and store them in files
        # - extract elements using selenium instead of painful bs4
        driver.get("https://w5.ab.ust.hk/wcq/cgi-bin/2430/subject/COMP")
        # driver.find_element(By.PARTIAL_LINK_TEXT, "")
        html = driver.page_source
        # input() # hold webdriver until key input
    finally:
        driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    courses = {}
    courses_html = soup.find_all('div', class_= 'course')
    for course_html in courses_html:
        course_name_string = course_html.find('div', class_ = 'subject').text
        course_code, course_name, credits = parse_course_name(course_name_string)
        class_attr = course_html.find('div', class_ = 'courseattr')
        pop_up_detail = class_attr.find('div', class_ = 'popupdetail')
        detail_table = pop_up_detail.find('table')
        if detail_table != None:
            course_detail = dict()
            rows = detail_table.find_all('tr')
            for r in rows:
                row_header = r.find_all('th')
                row_data = r.find_all('td')
                for i, j in zip(row_header, row_data):
                    course_detail.update({i.text.lower() : j.text}) 
            courses.update({course_code : (course_name, credits, course_detail)})
        else:
            print(pop_up_detail)
            print(f"{course_code} is not scraped.")
    return courses