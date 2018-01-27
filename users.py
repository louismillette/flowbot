import os
import random
import requests
from bs4 import BeautifulSoup
import names
import majors
import json
import time
import re
import logging
import http.client as http_client
import names
import sqlite3

'''
user:
    PURPOSE
        - basic user model.  What is this persons activity, what is their username and password, etc.
    REQUIRED (for new users) ARGUMENTS
        - first(str) first name of our user
        - last(str) last name of our user
        - faculty(str) just MATH
        - program(str) program (CO, STAT, ACTSC, etc.)
    FUNCTIONS
        - load (id(str)) loads user of particular id into this instance
        - gen_classes(fnc) takes no arguments, generates appropriate classes
        - gen_transcript(fnc) takes no arguments, requires classes, generates useable transcript
        - create_account(fnc) creates uwflow account with given credentials
        - upload_transcript(fnc) uploads transcript to account
        - ...
'''
# basic user model.  What is this persons activity, what is their username and password, etc.
# idd may be any random, but unique, id
# given the first name, last name,
class user():
    def __init__(self, first=None, last=None, country=None, id=None, year=None, faculty=None, program=None):
        self.first_name = first
        self.last_name = last
        self.country = country
        self.join_date = ''
        self.email = ''
        self.password = ''
        self.last_visited = None
        # eg. mduan or 20345619 ?
        self.student_id = ''
        # eg. university_of_waterloo ?
        self.school_id = 'university_of_waterloo'
        # eg. software_engineering ?

        self.api_key = None

        self.id=id
        self.year = year
        self.faculty = faculty
        self.program = program

        ## generate identity
        self.gen_id()
        self.gen_Emails()
        self.gen_student_id()

    def setUpDBLocal(self):
        dirr = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect("{}/classes.db".format(dirr))
        c = conn.cursor()
        try:
            c.execute(( 'CREATE TABLE user'
                        '(id TEXT, '
                        'active INTEGER, ' # has this user been activated on flow yet?
                        'username TEXT, '
                        'password TEXT, '
                        'PRIMARY KEY (ID), '
                        'UNIQUE (ID))'))
        except:
            pass
        try:
            c.execute(( 'CREATE TABLE user_course'
                        '(user_id TEXT, '
                        'course_id TEXT, ' # has this user been activated on flow yet?
                        'PRIMARY KEY (course_id), '
                        'FOREIGN KEY (user_id) REFERENCES user (id) '))
        except:
            pass
        try:
            c.execute(( 'CREATE TABLE user_reviews'
                        '(id TEXT, '
                        'active INTEGER, ' # has this user been activated on flow yet?
                        'username TEXT, '
                        'password TEXT, '
                        'PRIMARY KEY (ID), '
                        'UNIQUE (ID))'))
        except:
            pass

    # Generate some random email account names for this user
    def gen_Emails(self):
        self.uwaterloo = '{}{}{}@edu.uwaterloo.ca'.format(self.first_name[0],self.last_name,self.id)
        self.gmail = '{}{}{}@gmail.com'.format(self.first_name,self.last_name,self.id)
        self.yahoo = '{}{}{}@yahoo.com'.format(self.first_name, self.last_name, self.id)
        self.proton = '{}{}{}@protonmail.com'.format(self.first_name, self.last_name, self.id)

    # generate a new user id, sets self.id as it, and returns it
    def gen_id(self):
        dirr = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(dirr, 'ids.txt'), 'r') as file:
            already_taken = json.loads(file.readline())
        try:
            ids = already_taken[self.first_name + self.last_name]
        except:
            already_taken[self.first_name + self.last_name] = []
            ids = []
        if len(ids) > 90:
            raise Exception('Too many usernames: {} {}'.format(self.first_name, self.last_name))
        while 1:
            id_guess = random.randint(a=100, b=999)
            if id_guess not in ids:
                already_taken[self.first_name + self.last_name].append(id_guess)
                break
        with open(os.path.join(dirr, 'ids.txt'), 'w+') as file:
            file.write(json.dumps(already_taken))
        self.id = id_guess
        return id_guess

    # pick a random, never before picked, student ID
    def gen_student_id(self):
        dirr = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(dirr, 'student_ids.txt'), 'r') as file:
            ids = json.loads(file.readline())
        prefix = '205'
        thousands = str(3 * 12)
        while 1:
            id_guess = str(random.randint(a=100, b=999))
            if id_guess not in ids:
                ids.append(str(prefix + id_guess + thousands))
                break
        with open(os.path.join(dirr, 'student_ids.txt'), 'w+') as file:
            file.write(json.dumps(ids))
        self.student_id = str(prefix + id_guess + thousands)
        return str(prefix + id_guess + thousands)

    # generate the classes this bot is in.  A dict of class ID's (stat452 for instance) may be provided,
    # if this bot should have a particular class set.
    # requires defined program and department (although we're only considering math)
    # classes are taken out of electives
    def gen_classes(self, classes=None):
        if classes == None:
            classes = []
        program = self.program
        not_in = ['math135','math136','math137','math138','cs115','cs116','stat230','stat231','math235','math237']
        electives = []
        pre_selected_classes = []
        upper_300200 = []
        term = 'F'
        year = 2013
        # pick our 'demanded' classes
        for ID in classes:
            e = majors.classs(ID=ID, term=term, year=year)._gen_class()
            pre_selected_classes.append(e)
            not_in.append(e.ID)
        # pick 14 electives
        for i in range(14-len(classes)):
            e = majors.classs().gen_random_class(faculty='OTHER', notin=not_in, term=term, year=year)
            electives.append(e)
            not_in.append(e.ID)
        # pick 12 upper year courses
        try:
            m400_1 = majors.classs().gen_random_class(faculty='MATH', program=program,level=400, notin=not_in, term='F', year=year)
        except:
            m400_1 = majors.classs().gen_random_class(faculty='MATH', program=program, level=400, notin=not_in, term='F', year=year)
        not_in.append(m400_1.ID)
        m400_2 = majors.classs().gen_random_class(faculty='MATH', program=program, level=400, notin=not_in, term=term, year=year)
        not_in.append(m400_2.ID)
        # major 300's
        for i in range(6):
            e = majors.classs().gen_random_class(faculty='MATH', program=program,level=300, notin=not_in, term=term, year=year)
            upper_300200.append(e)
            not_in.append(e.ID)
        # math 300's
        for i in range(4):
            e = majors.classs().gen_random_class(faculty='MATH', level=300, notin=not_in, term=term, year=year)
            upper_300200.append(e)
            not_in.append(e.ID)
        # math 200+'s
        for i in range(4):
            e = majors.classs().gen_random_class(faculty='MATH', level=200, notin=not_in, term=term, year=year)
            upper_300200.append(e)
            not_in.append(e.ID)
        m1 = majors.classs(ID='math135', year=year, term=term)._gen_class()
        m2 = majors.classs(ID='math136', year=year, term=term)._gen_class()
        m3 = majors.classs(ID='math137', year=year, term=term)._gen_class()
        m4 = majors.classs(ID='math138', year=year, term=term)._gen_class()
        m5 = majors.classs(ID='cs115', year=year, term=term)._gen_class()
        m6 = majors.classs(ID='cs116', year=year, term=term)._gen_class()
        m7 = majors.classs(ID='math237', year=year, term=term)._gen_class()
        m8 = majors.classs(ID='math235', year=year, term=term)._gen_class()
        m9 = majors.classs(ID='stat230', year=year, term=term)._gen_class()
        m10 = majors.classs(ID='stat231', year=year, term=term)._gen_class()
        core = [m1,m2,m3,m4,m5,m6,m7,m8,m9,m10]
        courses = core+electives+pre_selected_classes+upper_300200
        print(len(courses))
        courses_s = list(sorted(courses, key=lambda x: x.number))
        terms = {
            'term_1a': courses_s[:5],
            'term_1b': courses_s[5:10],
            'term_2a': courses_s[10:15],
            'term_2b': courses_s[15:20],
            'term_3a': courses_s[20:25],
            'term_3b': courses_s[25:30],
            'term_4a': courses_s[30:35],
            'term_4b': courses_s[35:40]
        }
        self.classes = terms
        return terms

    # creates (already parsed) transcript for this student
    # if year is provided, that is the starting year of this student
    def gen_transcript(self, year=None):
        if not year:
            year = random.choice([2013,2014,2015,2016,2017])
        if not self.classes:
            raise Exception('No classes created')
        if not self.student_id:
            raise Exception('No student ID')
        if not self.program:
            raise Exception('No Program')
        baseyear = year
        course_by_term = []
        while year <= 2017:
            curr_year = (year-baseyear) + 1
            if curr_year == 5:
                break
            courses_a = self.classes['term_{}a'.format(curr_year)]
            courses_b = self.classes['term_{}b'.format(curr_year)]
            course_by_term += [{
                "name":"Fall {}".format(year),
                "programYearId": "{}A".format(curr_year),
                "courseIds":[ele.ID for ele in courses_a]

            },{
                "name": "Winter {}".format(year),
                "programYearId": "{}B".format(curr_year),
                "courseIds": [ele.ID for ele in courses_b]
            }]
            year += 1
        transcript = {
            "coursesByTerm": course_by_term,
            "studentId": self.student_id,
            "programName": "Statistics, Honours"
        }
        self.transcript = transcript
        return transcript

    # This user creates an account.  requires email, studentID, classes, and transcript
    # returtns self.  cookies, and profile number are set internally
    # creeates session
    def create_account(self):
        self.s = requests.Session()
        get_request = self.s.get(
            url="https://uwflow.com",
            headers={
                "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"en - CA, en - GB;q = 0.9, en - US;q = 0.8, en;q = 0.7",
                "Connection":"keep-alive",
                "Host":"uwflow.com",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 63.0.3239.132 Safari / 537.36"
            }
        )
        soup = BeautifulSoup(get_request.text, "html5lib")
        csrf_token = soup.find('meta', attrs={'name':'csrf-token'})['content']
        time.sleep(2)  # be kind to the server!
        print('Sucessfuly created get request to uwflow server')
        create_user_request = self.s.post(
            url="https://uwflow.com/api/v1/signup/email",
            data={
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.uwaterloo,
                "password": str(self.id) * 4
            },
            headers={
                "Accept": "*/*",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"en - CA, en - GB;q = 0.9, en - US;q = 0.8, en;q = 0.7",
                "Connection":"keep-alive",
                "Content-Length": "106",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin":"https://uwflow.com",
                "Referer":"https://uwflow.com/",
                "Host":"uwflow.com",
                "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 63.0.3239.132 Safari / 537.36",
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRF-Token": csrf_token,
            }
        )
        try:
            json.loads(BeautifulSoup(create_user_request.text, "html5lib").find('body').text)
        except:
            print('Failed to create user')
            return self
        time.sleep(2)
        print('Sucessfuly created user')
        get_profile_request = self.s.get(
            url="https://uwflow.com/profile",
            headers={
                "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"en - CA, en - GB;q = 0.9, en - US;q = 0.8, en;q = 0.7",
                "Connection":"keep-alive",
                "Host":"uwflow.com",
                "Referer": "https://uwflow.com/",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 63.0.3239.132 Safari / 537.36"
            }
        )
        profile_url = get_profile_request.history[1].url
        profile_number = profile_url.split('/')[-1]
        self.profile_number = profile_number
        self.password = str(self.id) * 4
        print({
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.uwaterloo,
                "password": str(self.id) * 4,
                "profile": self.profile_number
        })
        return self

    # adds tancript to account
    def add_transcript(self):
        get_request = self.s.get(
            url="https://uwflow.com/onboarding",
            headers={
                "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"en - CA, en - GB;q = 0.9, en - US;q = 0.8, en;q = 0.7",
                "Connection":"keep-alive",
                "Host":"uwflow.com",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 63.0.3239.132 Safari / 537.36"
            }
        )
        soup = BeautifulSoup(get_request.text, "html5lib")
        csrf_token = soup.find('meta', attrs={'name':'csrf-token'})['content']
        self.cookies = dict(get_request.cookies)
        time.sleep(2)  # be kind to the server!
        print('Sucessfuly requested uwflow home page')
        upload_transcript_request = self.s.post(
            url="https://uwflow.com/api/transcript",
            data={"transcriptData": json.dumps(self.transcript)},
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en - CA, en - GB;q = 0.9, en - US;q = 0.8, en;q = 0.7",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://uwflow.com",
                "Referer": "https://uwflow.com/onboarding",
                "Host": "uwflow.com",
                "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 63.0.3239.132 Safari / 537.36",
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRF-Token": csrf_token,
            }
        )
        print('Sucessfuly posted transcript')
        print(self.transcript)
        print(upload_transcript_request.status_code)
        # print(BeautifulSoup(upload_transcript_request.text, 'html5lib').prettify())

    # must be course user has taken
    # rating better be 0 or 1
    def review_course(self,course, rating):
        course_term_name = list(filter(lambda x: course in x['courseIds'], self.transcript['coursesByTerm']))[0]['name']
        code = course_term_name.split(' ')[1] + ('_09' if course_term_name.split(' ')[0]=="Fall" else ('_05' if course_term_name.split(' ')[0]=="Spring" else '_01'))
        get_request = self.s.get(
            url="https://uwflow.com/course/{}".format(course),
            headers={
                "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"en - CA, en - GB;q = 0.9, en - US;q = 0.8, en;q = 0.7",
                "Connection":"keep-alive",
                "Host":"uwflow.com",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 63.0.3239.132 Safari / 537.36"
            }
        )
        time.sleep(2)
        courseId = [ele[-1] for ele in re.findall(r'{}(.*?)user_course_id":\s?\s?"(.*?)",'.format(course), get_request.text)][-1]
        soup = BeautifulSoup(get_request.text, "html5lib")
        csrf_token = soup.find('meta', attrs={'name': 'csrf-token'})['content']
        print(courseId)
        payload = {
            "id": {
                "$oid": "{}".format(courseId)
            },
            "term_id": code,
            "term_name": course_term_name,
            "course_id": course,
            "professor_id": None,
            "professor_review": {
                "comment": "",
                "privacy": "friends",
                "ratings": [
                    {
                        "name": "clarity",
                        "rating": None
                    },
                    {
                        "name": "passion",
                        "rating": None
                    }
                ],
                "num_voted_helpful": 0,
                "num_voted_not_helpful": 0,
                "user_course_id": {
                    "$oid": "{}".format(courseId)
                },
                "review_type": "prof",
                "can_vote": False
            },
            "course_review": {
                "comment": "",
                "privacy": "friends",
                "ratings": [
                    {
                        "name": "usefulness",
                        "rating": rating
                    },
                    {
                        "name": "easiness",
                        "rating": rating
                    },
                    {
                        "name": "interest",
                        "rating": rating
                    }
                ],
                "num_voted_helpful": 0,
                "num_voted_not_helpful": 0,
                "user_course_id": {
                    "$oid": "{}".format(courseId)
                },
                "review_type": "course",
                "can_vote": False
            },
            "has_reviewed": False,
            "user_id": {
                "$oid": self.profile_number
            },
            "program_year_id": "4A"
        }

        post_review_request = self.s.put(
            url="https://uwflow.com/api/user/course",
            json=payload,
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"en-US,en;q=0.5",
                "Connection":"keep-alive",
                "Content-Type": "application/json",
                "Origin":"https://uwflow.com",
                "Pragma":"no-cache",
                "Referer":"https://uwflow.com/{}".format(course),
                "Host":"uwflow.com",
                "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 63.0.3239.132 Safari / 537.36",
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRF-Token": csrf_token,
            }
        )
        # print(BeautifulSoup(post_review_request.text).prettify())
        print(post_review_request.status_code)
        print(payload)

    # log into the given username and password
    # starts new session
    def log_in(self, username, password):
        print('starting')
        self.s = requests.Session()
        get_request = self.s.get(
            url="https://uwflow.com",
            headers={
                "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en - CA, en - GB;q = 0.9, en - US;q = 0.8, en;q = 0.7",
                "Connection": "keep-alive",
                "Host": "uwflow.com",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 63.0.3239.132 Safari / 537.36"
            }
        )
        soup = BeautifulSoup(get_request.text, "html5lib")
        csrf_token = soup.find('meta', attrs={'name': 'csrf-token'})['content']
        time.sleep(2)  # be kind to the server!
        print('Sucessfuly created get request to uwflow server')
        create_user_request = self.s.post(
            url="https://uwflow.com/api/v1/login/email",
            data={
                "email": username,
                "password": password,
            },
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en - CA, en - GB;q = 0.9, en - US;q = 0.8, en;q = 0.7",
                "Connection": "keep-alive",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://uwflow.com",
                "Referer": "https://uwflow.com/",
                "Host": "uwflow.com",
                "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 63.0.3239.132 Safari / 537.36",
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRF-Token": csrf_token,
            }
        )
        print(create_user_request.status_code)
        return self


# print some cool colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == '__main__':
    # user creation and ranking protocol
    # time.sleep(random.randint(10,20) + random.randint(1000,9999)/1000)
    fname = random.choice(names.FIRST_NAMES).lower()
    lname = random.choice(names.LAST_NAMES).lower()
    # print(bcolors.OKBLUE + '[+] Starting User Creation and Rating' + bcolors.ENDC)
    # start = time.time()
    U = user(first=fname, last=lname, faculty='MATH',program='cs', year=2014)
    # U.gen_classes(classes=['stat441'])
    # print(bcolors.OKBLUE + '[+] classes generated' + bcolors.ENDC)
    # U.gen_transcript(year=2014)
    # print(bcolors.OKBLUE + '[+] transcript generated' + bcolors.ENDC)
    # U.create_account()
    # print(bcolors.OKBLUE + '[+] account generated' + bcolors.ENDC)
    # U.add_transcript()
    # print(bcolors.OKBLUE + str(U.gen_classes()) + bcolors.ENDC)
    #
    # # enable logging:
    # logging.basicConfig()
    # logging.getLogger().setLevel(logging.DEBUG)
    # requests_log = logging.getLogger("requests.packages.urllib3")
    # requests_log.setLevel(logging.DEBUG)
    # requests_log.propagate = True
    # http_client.HTTPConnection.debuglevel = 1
    # U.review_course(course='stat441', rating=0)
    # end = time.time()
    # print(bcolors.OKBLUE + '[+] Rated Course in {} seconds'.format(end-start) + bcolors.ENDC)
    U.log_in("msparks291@edu.uwaterloo.ca", "291291291291")
