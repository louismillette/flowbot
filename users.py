import random
import requests
import names

# basic user model.  What is this persons activity, what is their username and password, etc.
# idd may be any random, but unique, id
class user():
    def __init__(self, first, last, country, id=None, gender=None, year=None, faculty=None, classes=None):
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
        self.classes = classes

        ## generate identity
        self.gen_id()
        self.gen_Emails()
        self.gen_year()
        self.gen_student_id()

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

    # generate the year this student is in
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
    def gen_classes(self, classes):
        pass
# program
class program(self):
    def __init__(self, faculty):
        self.faculties = [
            'Applied Health Sciences',
            'Arts',
            'Engineering',
            'Environment',
            'Mathematics',
            'Science',
        ]
        pass
