import os
import sqlite3
import requests
import random
from bs4 import BeautifulSoup

class classs():
    def __init__(self, subject=None, number=None, online=None, lec=None, tut=None, tst=None, credit=None, name=None,
                 description=None, ID=None, faculty=None, level=None, term=None, year=None):
        self.subject = subject
        self.number = number
        self.online = online
        self.lec = lec
        self.tut = tut
        self.tst = tst
        self.credit = credit
        self.name = name
        self.description = description
        self.ID = ID
        self.faculty = faculty
        self.level = level
        self.term = term
        self.year = year

    # given class ID (stat444 for instance) generates class details from DB
    def _gen_class(self):
        if not self.ID:
            raise Exception('Cant acquire class without class ID')
        if not self.year:
            raise Exception('Cant acquire class without class year')
        if not self.term:
            raise Exception('Cant acquire class without class term')
        select_statement = ('SELECT DISTINCT (classs.number, classs.online, classs.lec, classs.tut, classs.tst, classs.credit, classs.name, '
                      'classs.description, classs.faculty, classs.level, classs.ID) ')
        from_statement = 'FROM classs, offered '
        where_statement = 'offered.ID="{0}" AND classs.ID="{0}" AND offered.term="{1}" AND offered.year="{2}"'.format(self.ID,self.term,self.year)
        sql = select_statement + from_statement + where_statement
        dirr = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect("{}/classes.db".format(dirr))
        c = conn.cursor()
        row = c.execute(sql).fetchone()
        (self.subject, self.number, self.online, self.lec, self.tut,
        self.tst, self.credit, self.name, self.description, self.faculty,
         self.level, self.ID) = row

    '''
    gen_random_class:
        PURPOSE
            - make this class instance a random class that satisfies the given arguments
        ARGUMENTS
            - faculty (str) faculty this class is in (if none, we don't constrain this)
            - level (int) class level (is this a 100 level course? ) must be 0 or 100 or 200 or 300 or 400.
            - program (str) 'CO', 'MATH', 'ECON', etc.  if not in the given faculty, will return no results
            - notin (list) list of ids ([stat441, stat442, ..]) that this class can't be
            - term: 'F', 'W', or 'S'.  can't be none.
            - year: 2013, 2017, etc.  must be defined.
        RETURNS
            - self
    '''
    def gen_random_class(self, faculty=None, level=None, program=None, notin=None, term='F', year=2013):
        if not (term and year):
            raise Exception('gotta have a year and term.')

        select_term = ('SELECT DISTINCT classs.subject, classs.number, classs.online, classs.lec, classs.tut, classs.tst, classs.credit, classs.name, '
                      'classs.description, classs.faculty, classs.level, classs.ID ')
        from_term = 'FROM classs, offered '
        where_term = 'WHERE offered.ID=classs.ID AND offered.term="{}" AND offered.year="{}" '.format(term,year)
        if faculty:
            where_term += 'AND classs.faculty="{}" '.format(faculty)
        if level:
            where_term += 'AND classs.level="{}" '.format(level)
        if program:
            where_term += 'AND classs.subject="{}" '.format(program)
        sql = select_term + from_term + where_term
        print(sql)
        dirr = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect("{}/classes.db".format(dirr))
        c = conn.cursor()
        rows = c.execute(sql).fetchall()
        rows_clean = list(filter(lambda x: x[-1] not in notin, rows))
        row = random.choice(rows_clean)
        (self.subject, self.number, self.online, self.lec, self.tut,
         self.tst, self.credit, self.name, self.description,
         self.faculty, self.level, self.ID) = row
        self.term = term
        self.year = year
        return self





# class programs
class Program():
    def __init__(self, faculty, major, code, coop_students):
        self.faculty = faculty
        self.major = major
        self.coop_students = coop_students

class Department():
    def __init__(self, programs, program_codes, department):
        self.department = department
        self.programs = programs

# Math Department.  We'll only do this one department, and treat everything else as OTHER; just to save some time.
MATH = Department(department='MATH', programs=[
        Program('MATH', 'Actuarial Science', ['MATH', 'ACTSC'], 490),
        Program('MATH', 'Applied Mathematics', ['MATH', 'AMATH'], 168),
        Program('MATH', 'Business Administration and Computer Science', ['MATH', 'BE', 'CS'], 192),
        Program('MATH', 'Business Administration and Mathematics', ['BE', 'MATH'], 245),
        Program('MATH', 'Chartered Professional Accountancy', ['ACC', 'MATH'], 195),
        Program('MATH', 'Combinatorics & Optimization', ['MATH', 'CO'], 119),
        Program('MATH', 'Computational Mathematics',['MATH', 'CS'], 61),
        Program('MATH', 'Computer Science',['MATH', 'CS'], 2623),
        Program('MATH', 'Financial Analysis and Risk Management',['AFM','MATH'], 632),
        Program('MATH', 'Information Technology Management',['MATH','CS'], 20),
        Program('MATH', 'Health Informatics',['MATH', 'HLTH'], 15),
        Program('MATH', 'Mathematics/Business Administration', ['MATH','BE'], 401),
        Program('MATH', 'Mathematical Studies', ['MATH'], 202),
        Program('MATH', 'Mathematics/Teaching', ['MATH'], 69),
        Program('MATH', 'Pure Mathematics', ['MATH', 'PMATH'], 84),
        Program('MATH', 'Software Engineering', ['SE', 'MATH'], 495),
        Program('MATH', 'Statistics', ['STAT', 'MATH'], 384),
        Program('MATH', 'Mathematics', ['MATH'], 1773),
        Program('MATH', 'Mathematical Economics', ['MATH', 'ECON'], 36),
        Program('MATH', 'Mathematical Finance', ['MATH', 'FINAN'], 53),
        Program('MATH', 'Mathematical Physics', ['MATH', 'PHYS'], 140),
    ], program_codes = [
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
)


if __name__ == '__main__':
    c = classs()
    c.gen_random_class(faculty='OTHER', level=100, term='F', year=2013)
    print(c.ID, c.year, c.term)
    pass




'''
'SCIENCE'
'Biochemistry'
'Biology'
'Biomedical Sciences'
'Life Physics'
'Psychology'
'Chemistry'
'Medicinal Chemistry'
'Materials and Nanosciences'
'Physics'
'Mathematical Physics'
'Physics and Astronomy'
'Earth Sciences'
'Honours Science'
'Science and Business'
'Biotechnology/Chartered Professional Accountancy'
'Biotechnology/Economics'
'Environmental Science'
'Science and Aviation'


'ENVIRONMENT'
'Environment and Business'
'Environment, Resources and Sustainability'
'Geography and Aviation'
'Geography and Environmental Management'
'Geomatics'
'International Development'
'Knowledge Integration'
'Planning'



'ENGINEERING'
'Architectural Engineering'
'Architecture'
'Biomedical Engineering'
'Chemical Engineering'
'Civil Engineering'
'Computer Engineering'
'Electrical Engineering'
'Environmental Engineering'
'Geological Engineering'
'Management Engineering'
'Mechanical Engineering'
'Mechatronics Engineering'
'Nanotechnology Engineering'
'Software Engineering'
'Systems Design Engineering'


'ARTS'
'Anthropology'
'Economics'
'Legal Studies'
'Peace and Conflict Studies'
'Political Science'
'Psychology'
'Sexuality, Marriage, and Family Studies'
'Social Development Studies*'
'Sociology'
'Womens Studies'
'Classical Studies'
'English'
'History'
'Medieval Studies'
'Philosophy'
'Religious Studies'
'Speech Communication'
'Fine Arts'
'Music'
'Theatre and Performance'
'French'
'German'
'Spanish'
'''


