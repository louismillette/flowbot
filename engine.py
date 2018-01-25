import sqlite3
import os
import re
import math
import requests
from bs4 import BeautifulSoup

'''
engine.py python scraper.  Broken into components:
    - The Scraper:
        Base Class for our project.  For all subsequent scraping submodules, this collection of methods
        are the ones each class requires and uses.
    - The MATH faculty class scraper:
        take our base class, override methods for clean usage in the math department
    - other faculty class scraper?  If we do another class maybe
'''


# Base class for all school classes
class Scrape():
    # set up local sqlite3 DB for class data dump
    def setUpDBLocal(self):
        dirr = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect("{}/classes.db".format(dirr))
        c = conn.cursor()
        try:
            c.execute(( 'CREATE TABLE classs'
                        '(subject TEXT, '
                        'number TEXT, '
                        'online INTEGER, '
                        'lec INTEGER, '
                        'tut INTEGER, '
                        'tst INTEGER, '
                        'credit REAL, '
                        'name TEXT, '
                        'description TEXT, '
                        'ID TEXT NOT NULL, '
                        'faculty TEXT, '
                        'level INTEGER, '
                        'PRIMARY KEY (ID), '
                        'UNIQUE (ID))'))
        except:
            pass
        try:
            c.execute(( 'CREATE TABLE classs'
                        '(subject TEXT, '
                        'number TEXT, '
                        'online INTEGER, '
                        'lec INTEGER, '
                        'tut INTEGER, '
                        'tst INTEGER, '
                        'credit REAL, '
                        'name TEXT, '
                        'description TEXT, '
                        'ID TEXT NOT NULL, '
                        'faculty TEXT, '
                        'level INTEGER, '
                        'PRIMARY KEY (ID), '
                        'UNIQUE (ID))'))
        except:
            pass
        try:
        # each entry is a class term/year combination, for that class being available in that year/term
            c.execute(('CREATE TABLE offered'
                        '(ID TEXT, '
                        'term TEXT, ' # F,W,S
                        'year INTEGER, ' # 2017, 2016, etc
                        'offID TEXT, '
                        'FOREIGN KEY (ID) REFERENCES classs(ID), '
                        'PRIMARY KEY (offID), '
                        'UNIQUE (offID)); '))
        except:
            pass # offered table already exists
        conn.commit()
        return conn

    '''
    storeClasses:
        PURPOSE
            - goes through search links, scrape texts, put them in the DB
        ARGUMENTS
            - getClasses (function) takes a url and returns a list of html chunks, a chunk for each class
            - getDetails (function) takes a class html chunk and returns dict of class details
            - urls (list) is a list of the urls (str) for the program classes
            - years (list) is a list of years (str) corrispondong 1-1 with the above urls
            - conn is the DB connection
            - all arguments are optional, if not provided we'll try to find class attributes of the arg name
        RETURNS
            - None
    '''
    def storeClasses(self, getClasses=None, getDetails=None, urls=None, years=None, faculty=None, conn=None):
        if not getClasses:
            try:
                getClasses = self.getClasses
            except:
                raise Exception('getClasses Not Defined')
        if not getDetails:
            try:
                getDetails = self.getDetails
            except:
                raise Exception('getDetails Not Defined')
        if not urls:
            try:
                urls = self.urls
            except:
                raise Exception('urls Not Defined')
        if not years:
            try:
                years = self.years
            except:
                raise Exception('years Not Defined')
        if not conn:
            try:
                conn = self.conn
            except:
                raise Exception('conn Not Defined')
        if not faculty:
            try:
                faculty = self.faculty
            except:
                raise Exception('faculty Not Defined')
        c = conn.cursor()
        for url,year in zip(urls[:-1],years[:-1]):
            classes = getClasses(url)
            for classs in classes:
                details = getDetails(classs)
                for offer in details['offered']:
                    c.execute(('INSERT INTO offered '
                               'VALUES ("{0}","{1}","{2}", "{0}{2}{1}")').format(details['ID'], offer, int(year)))
        conn.commit()
        # only need the rest of the details for the last URL
        classes = getClasses(urls[-1])
        year = years[-1]
        for classs in classes:
            details = getDetails(classs)
            # print(('INSERT INTO classs(subject, number, online, lec, tut, tst, credit, name, description, ID, faculty) '
            #         'SELECT "{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}", "{10}" '
            #         'WHERE NOT EXISTS (SELECT * FROM classs WHERE subject="{9}"); ').format(
            #     details['subject'], details['number'], details['online'],
            #     details['lec'], details['tut'], details['tst'], details['credit'],
            #     details['name'], details['description'], details['ID'],faculty,
            # ))
            c.execute(('INSERT INTO classs(subject, number, online, lec, tut, tst, credit, name, description, ID, faculty, level) '
                    'SELECT "{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}" '
                    'WHERE NOT EXISTS (SELECT * FROM classs WHERE subject="{9}"); ').format(
                details['subject'], details['number'], details['online'],
                details['lec'], details['tut'], details['tst'], details['credit'],
                details['name'], details['description'], details['ID'], faculty,
                details['level']
            ))
            for offer in details['offered']:
                # print(('INSERT INTO offered '
                #            'VALUES ("{}","{}","{}");').format(details['ID'], offer, year))
                c.execute(('INSERT INTO offered '
                           'VALUES ("{0}","{1}","{2}", "{0}{2}{1}")').format(details['ID'], offer, int(year)))
        conn.commit()
        return self

# builds faculty/program by scrpaeing and putting in DB
class Build(Scrape):
    def __init__(self, faculty, program):
        self.urls = [
            'http://www.ucalendar.uwaterloo.ca/1314/COURSE/course-{}.html'.format(program),
            'http://www.ucalendar.uwaterloo.ca/1415/COURSE/course-{}.html'.format(program),
            'http://www.ucalendar.uwaterloo.ca/1516/COURSE/course-{}.html'.format(program),
            'http://www.ucalendar.uwaterloo.ca/1617/COURSE/course-{}.html'.format(program),
            'http://www.ucalendar.uwaterloo.ca/1718/COURSE/course-{}.html'.format(program),
        ]
        self.setUpDBLocal()
        self.years = ['2013','2014','2015','2016','2017']
        dirr = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect("{}/classes.db".format(dirr))
        self.faculty = faculty

    # takes url (string) spits out html text (str) for each class
    def getClasses(self, url):
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html5lib')
        blurbs = soup.find_all('center')
        blurbs = [ele.find_all('tbody')[0] for ele in blurbs]
        return blurbs

    # takes html text (str) for each class and spits out dict of class and attributes
    def getDetails(self, blurb):
        rows = blurb.find_all('tr')
        # row 0 : subject, number, componenet, and credit
        row0 = rows[0].find_all('td')
        row0td0 = row0[0].text.split(' ')
        subject = row0td0[0]
        number = row0td0[1]
        level = math.floor(int(re.search(r'\d+', number).group())/100)*100
        credit = float(row0td0[3])
        LEC = False
        TUT = False
        TST = False
        components = row0td0[2].split(',')
        if 'LEC' in components:
            LEC = True
        if 'TUT' in components:
            TUT = True
        if 'TST' in components:
            TST = True
        # row 1: formal name of course
        row1 = rows[1].text
        name = row1
        # row 2: course description and offered
        try:
            row2 = rows[2].text
            discription = row2.split('Offered')[0][:-3]
            offered = row2.split('Offered')[1][2:-1].split(',')
        except:
            # this occurs if the class is ONLY offered online, or there was an error and the offered terms are not present (MATH 116 or MATH 52 or MATH 97).
            # we'll just pretend its offered every term, cause uwflow will create it in the term its registered if it doesn't know.
            discription = ''
            offered = ['F','W','S']
        # row 6: online?
        online = False
        try:
            row6 = rows[6].text
            if 'Also offered Online' in row6:
                online=True
        except:
            pass
        return {
            'ID': subject.lower() + number,
            'subject': subject.lower(),
            'number': number,
            'online': int(online),
            'lec': int(LEC),
            'tut': int(TUT),
            'tst': int(TST),
            'credit': credit,
            'name': name,
            'offered':offered,
            'description': discription,
            'level': level,
        }

if __name__ == '__main__':
    # construct mathematics classes
    program_codes = [
        'ACTSC',
        'AMATH',
        'CO',
        'COMM',
        'CS',
        'MATH',
        'MATBUS',
        'MATHEL',
        'PMATH',
        'SE',
        'STAT',
    ]
    for program in program_codes:
        # break
        Build(faculty='MATH', program=program).storeClasses()
        print('Finished {}'.format(program))
    OTHER = [
        'BE',
        'ACC',
        'AFM',
        'HLTH',
        'FINAN',
        'PHYS',
        'ECON',
    ]
    for program in OTHER:
        # break
        Build(faculty='OTHER', program=program).storeClasses()
        print('Finished {}'.format(program))




