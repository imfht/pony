from decimal import Decimal
from datetime import date

from pony.orm.core import *

db = Database('sqlite', 'presentation.sqlite', create_db=True)
#db = Database('mysql', host="localhost", user="presentation", passwd="pony", db="presentation")
#db = Database('postgres', user='presentation', password='pony', host='localhost', database='presentation')
#db = Database('oracle', 'presentation/pony@localhost')

class Department(db.Entity):
    number = PrimaryKey(int, auto=True)
    name = Required(unicode, unique=True)
    groups = Set("Group")
    courses = Set("Course")

class Group(db.Entity):
    number = PrimaryKey(int)
    major = Required(unicode)
    dept = Required("Department")
    students = Set("Student")

class Course(db.Entity):
    name = Required(unicode)
    semester = Required(int)
    lect_hours = Required(int)
    lab_hours = Required(int)
    credits = Required(int)
    dept = Required(Department)
    students = Set("Student")
    PrimaryKey(name, semester)

class Student(db.Entity):
    # _table_ = "public", "Students"  # Schema support
    id = PrimaryKey(int, auto=True)
    name = Required(unicode)
    dob = Required(date)
    tel = Optional(str)
    picture = Optional(buffer, lazy=True)
    gpa = Required(float, default=0)
    group = Required(Group)
    courses = Set(Course, nplus1_threshold=0)

sql_debug(True)  # Output all SQL queries to stdout

db.generate_mapping(create_tables=True)
# db.generate_mapping(check_tables=True)

def populate_database():
    if select(s for s in Student).count() > 0:
        return

    d1 = Department(name="Department of Computer Science")
    d2 = Department(name="Department of Mathematical Sciences")
    d3 = Department(name="Department of Applied Physics")

    c1 = Course(name="Web Design", semester=1, dept=d1,
                       lect_hours=30, lab_hours=30, credits=3)
    c2 = Course(name="Data Structures and Algorithms", semester=3, dept=d1,
                       lect_hours=40, lab_hours=20, credits=4)

    c3 = Course(name="Linear Algebra", semester=1, dept=d2,
                       lect_hours=30, lab_hours=30, credits=4)
    c4 = Course(name="Statistical Methods", semester=2, dept=d2,
                       lect_hours=50, lab_hours=25, credits=5)

    c5 = Course(name="Thermodynamics", semester=2, dept=d3,
                       lect_hours=25, lab_hours=40, credits=4)
    c6 = Course(name="Quantum Mechanics", semester=3, dept=d3,
                       lect_hours=40, lab_hours=30, credits=5)

    g101 = Group(number=101, major='B.E. in Computer Engineering', dept=d1)
    g102 = Group(number=102, major='B.S./M.S. in Computer Science', dept=d1)
    g103 = Group(number=103, major='B.S. in Applied Mathematics and Statistics', dept=d2)
    g104 = Group(number=104, major='B.S./M.S. in Pure Mathematics', dept=d2)
    g105 = Group(number=105, major='B.E in Electronics', dept=d3)
    g106 = Group(number=106, major='B.S./M.S. in Nuclear Engineering', dept=d3)

    s1 = Student(name='John Smith', dob=date(1991, 3, 20), tel='123-456', gpa=3, group=g101,
                        courses=[c1, c2, c4, c6])
    s1 = Student(name='Matthew Reed', dob=date(1990, 11, 26), gpa=3.5, group=g101,
                        courses=[c1, c3, c4, c5])
    s1 = Student(name='Chuan Qin', dob=date(1989, 2, 5), gpa=4, group=g101,
                        courses=[c3, c5, c6])
    s1 = Student(name='Rebecca Lawson', dob=date(1990, 4, 18), tel='234-567', gpa=3.3, group=g102,
                        courses=[c1, c4, c5, c6])
    s1 = Student(name='Maria Ionescu', dob=date(1991, 4, 23), gpa=3.9, group=g102,
                        courses=[c1, c2, c4, c6])
    s1 = Student(name='Oliver Blakey', dob=date(1990, 9, 8), gpa=3.1, group=g102,
                        courses=[c1, c2, c5])
    s1 = Student(name='Jing Xia', dob=date(1988, 12, 30), gpa=3.2, group=g102,
                        courses=[c1, c3, c5, c6])
    commit()

def print_students(students):
    for s in students:
        print s.name
    print

def test_queries():
    students = select(s for s in Student)
    print_students(students)


    students = select(s for s in Student if s.gpa > 3.4 and s.dob.year == 1990)
    print_students(students)


    students = select(s for s in Student if len(s.courses) < 4)
    print_students(students)


    students = select(s for s in Student
                       if len(c for c in s.courses if c.dept.number == 1) < 4)
    print_students(students)


    students = select(s for s in Student if s.name.startswith("M"))
    print_students(students)


    students = select(s for s in Student if "Smith" in s.name)
    print_students(students)


    students = select(s for s in Student
                         if "Web Design" in s.courses.name)
    print_students(students)


    print 'Average GPA is', avg(s.gpa for s in Student)
    print


    students = select(s for s in Student
                         if sum(c.credits for c in s.courses) < 15)
    print_students(students)


    students = select(s for s in Student
                         if s.group.major == "B.E. in Computer Engineering")
    print_students(students)


    students = select(s for s in Student
                         if s.group.dept.name == "Department of Computer Science")
    print_students(students)


    students = select(s for s in Student).orderby(Student.name)
    print_students(students)


    students = select(s for s in Student).orderby(Student.name)[2:4]
    print_students(students)


    students = select(s for s in Student).orderby(Student.name.desc)
    print_students(students)


    students = select(s for s in Student) \
               .orderby(Student.group, Student.name.desc)
    print_students(students)


    students = select(s for s in Student
                         if s.group.dept.name == "Department of Computer Science"
                            and s.gpa > 3.5
                            and len(s.courses) > 3)
    print_students(students)


##if __name__ == '__main__':
##    populate_database()
##    test_queries()