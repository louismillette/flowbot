import requests
from bs4 import BeautifulSoup


# class programs
class Program():
    def __init__(self, faculty, major, code, coop_students):
        self.faculty = faculty
        self.major = major
        self.coop_students = coop_students

    # check if the classes for this department already exists in class.txt
    # otherwise grab them from online
    def get_classes(self):
        dirr = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(dirr, 'department.txt'), 'r') as file:
            data = file.readline()
        # check to make sure faculty exists
        try:
            fac = data[self.faculty]
        except:
            data[self.faculty] = {}
            with open(os.path.join(dirr, 'department.txt'), 'w+') as file:
                file.write(data)
        # faculty DEFINITELY exists now
        all_classes = {}
        for code in self.code:
            try:
                fac = data[self.faculty]
                classes = fac[code]
                all_classes[code] = [Class().fromdict(ele) for ele in classes]
                continue
            except:
                classes = []
            base_urls = [
                'http://www.ucalendar.uwaterloo.ca/1314/COURSE/course-{}.html'.format(code),
                'http://www.ucalendar.uwaterloo.ca/1415/COURSE/course-{}.html'.format(code),
                'http://www.ucalendar.uwaterloo.ca/1516/COURSE/course-{}.html'.format(code),
                'http://www.ucalendar.uwaterloo.ca/1617/COURSE/course-{}.html'.format(code),
                'http://www.ucalendar.uwaterloo.ca/1718/COURSE/course-{}.html'.format(code),
            ]
            for url in base_urls:
                r = requests.get(url).text
                soup = BeautifulSoup(r)

    def __parse(self,url):
        r = requests.get(url).text
        soup = BeautifulSoup(r)



class Department():
    def __init__(self, programs, program_codes, department):
        self.department = department
        self.programs = programs



class Class():
    def __init__(self):
        self.year = None # beggining year
        self.subject = None
        self.number = None
        self.online = False
        self.LEC = None
        self.TUT = None
        self.TST = None
        self.credit = None
        self.faculties = [] # is this only availabe to certain faculties?
        self.pre_req = [] # what other classes does this one need?
        self.anti_req = [] # what other classes does this one require u havent taken?
        self.offered = [] # when is this offered (in each year)? ['S','W','F']
        self.ID = None

    # pull data from class dict stores in department.txt
    def fromdict(self, class_dict)
        return self


# Math Department
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


