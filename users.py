import os
import random
import requests
import names
import majors

# basic user model.  What is this persons activity, what is their username and password, etc.
# idd may be any random, but unique, id
class user():
    def __init__(self, first=None, last=None, country=None, id=None, gender=None, year=None, faculty=None, program=None):
        self.first_name = first
        self.middle_name = ''
        self.last_name = last
        self.gender = gender
        self.fbid = None
        self.fb_access_token = ''
        self.fb_access_token_expiry_date = ''
        self.fb_access_token_invalid = ''
        self.country = country
        self.join_date = ''
        self.email = ''
        self.password = ''
        self.friend_ids = []
        self.friend_fbids = []
        self.last_visited = None
        self.num_visits = 0
        # The last time the user visited the onboarding page
        self.last_show_onboarding = None
        # The last time the user was shown the import schedule view
        self.last_show_import_schedule = None
        # eg. mduan or 20345619 ?
        self.student_id = ''
        # eg. university_of_waterloo ?
        self.school_id = 'university_of_waterloo'
        # eg. software_engineering ?
        self.program_name = ''
        # List of UserCourse.id's
        self.course_history = []
        # Deprecated
        self.last_term_id = ''
        # Deprecated
        self.last_program_year_id = ''
        # Track the number of times the user has invited friends
        # (So we can award points if they have)
        self.num_invites = 0
        self.sent_exam_schedule_notifier_email = False
        self.sent_velocity_demo_notifier_email = False
        self.sent_raffle_notifier_email = False
        self.sent_raffle_end_notifier_email = False
        self.sent_schedule_sharing_notifier_email = False
        self.sent_course_enrollment_feb_8_email = False
        self.sent_referral_contest_email = False
        self.sent_referral_contest_end_email = False
        self.sent_welcome_email = False
        self.num_points = 0
        self.is_admin = False
        self.email_unsubscribed = False
        self.transcripts_imported = 0
        self.schedules_imported = 0
        self.last_bad_schedule_paste = None
        self.last_good_schedule_paste = None
        self.last_bad_schedule_paste_date = None
        self.last_good_schedule_paste_date = None
        self.schedule_sorry = False
        self.api_key = None
        self.last_prompted_for_review = None
        self.voted_course_review_ids = []
        self.voted_prof_review_ids = []
        self.closed_scholarship_ids = None
        # custom var:  all times shown onboarding page
        self.every_show_onboarding = []
        # custom var: all times shown import schedule page
        self.every_show_import_schedule = None
        self.birth_date = None
        self.join_source = 2
        self.referrer_id = 0
        self.id=id
        self.year = year
        self.faculty = faculty
        self.program = program

        ## generate identity
        self.gen_id()
        # self.gen_Emails()
        # self.gen_year()
        # self.gen_student_id()

    # Generate some random email account names for this user
    def gen_Emails(self):
        if country == 'china':
            # add come random numbers
            uwaterloo = '{}{}{}@edu.uwaterloo.ca'.format(first[0],last,self.id)
            gmail = '{}{}{}@gmail.com'.format(first,last,self.id)
            yahoo = '{}{}{}@yahoo.com'.format(first, last, self.id)
            proton = '{}{}{}@protonmail.com'.format(first, last, self.id)

    # generate a new user id, sets self.id as it, and returns it
    def gen_id(self):
        dirr = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(dirr, 'ids.txt'), 'r') as file:
            already_taken = file.readline()
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
            file.write(already_taken)
        self.id = id_guess
        return id_guess

    # generate the year this student is in. We'll make them all 2013 cause it doesn't matter
    def gen_year(self):
        if self.year:
            self.term = str(self.year) + random.choice('A', 'B')
        else:
            self.year = random.randint(1,5)
            self.term = str(self.year) + random.choice('A','B')

    # pick a random, never before picked, student ID
    def gen_student_id(self):
        dirr = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(dirr, 'student_ids.txt'), 'r') as file:
            ids = file.readline()
        prefix = '205'
        thousands = str(self.year * 12000)
        while 1:
            id_guess = random.randint(a=100, b=999)
            if id_guess not in ids:
                ids.append(id_guess + prefix + thousands)
                break
        with open(os.path.join(dirr, 'ids.txt'), 'w+') as file:
            file.write(ids)
        self.student_id = id_guess
        return id_guess

    def gen_faculty(self):
        pass
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
        print('hit1')
        for ID in classes:
            e = majors.classs(id=ID, term=term, year=year)._gen_class()
            pre_selected_classes.append(e)
            not_in.append(e.ID)
        # pick 14 electives
        print('hit2')
        for i in range(14-len(classes)):
            e = majors.classs().gen_random_class(faculty='OTHER', notin=not_in, term=term, year=year)
            electives.append(e)
            not_in.append(e.ID)
        # pick 12 upper year courses
        print('hit3')
        try:
            print(not_in)
            m400_1 = majors.classs().gen_random_class(faculty='MATH', program=program,level=400, notin=not_in, term='F', year=year)
        except:
            m400_1 = majors.classs().gen_random_class(faculty='MATH', program=program, level=400, notin=not_in, term='F', year=year)
        not_in.append(m400_1.ID)
        m400_2 = majors.classs().gen_random_class(faculty='MATH', program=program, level=400, notin=not_in, term=term, year=year)
        not_in.append(m400_2.ID)
        # major 300's
        print('hit4')
        for i in range(6):
            e = majors.classs().gen_random_class(faculty='MATH', program=program,level=300, notin=not_in, term=term, year=year)
            upper_300200.append(e)
            not_in.append(e.ID)
        # math 300's
        print('hit5')
        for i in range(4):
            e = majors.classs().gen_random_class(faculty='MATH', level=300, notin=not_in, term=term, year=year)
            upper_300200.append(e)
            not_in.append(e.ID)
        # math 200+'s
        print('hit6')
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
    def gen_transcript(self, year):
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
                "name":"Fall+{}".format(year),
                "programYearId": "{}A".format(curr_year),
                "courseIds":[ele.ID for ele in courses_a]

            },{
                "name": "Winter+{}".format(year),
                "programYearId": "{}B".format(curr_year),
                "courseIds": [ele.ID for ele in courses_b]
            }]
            year += 1
        transcript = {
            "coursesByTerm": course_by_term,
            "studentId": self.student_id,
            "programName": self.program
        }
        self.transcript = transcript
        return transcript


    # This user creates an account.  requires email, studentID, and classes
    def create_account(self):
        pass
if __name__ == '__main__':
    U = user(first='jon',last='public', faculty='MATH',program='cs')
    # print(U.gen_classes())