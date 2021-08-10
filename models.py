from exts import db
import shortuuid
import enum
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result


class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(50), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    user = db.Column(db.Integer)


class Problem(db.Model):
    __tablename__ = 'problem'
    prob_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    course_id = db.Column(db.Integer)
    user = db.Column(db.String(100), nullable=False)


class HighlightProbModel(db.Model):
    __tablename__ = 'highlight_prob'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prob_id = db.Column(db.Integer, db.ForeignKey("problem.prob_id"))
    create_time = db.Column(db.DateTime, default=datetime.now)

    prob = db.relationship("Problem", backref="highlight")

class CollectProb(db.Model):
    __tablename__ = 'collect_prob'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    prob_id = db.Column(db.Integer, db.ForeignKey("problem.prob_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    prob = db.relationship("Problem", backref='collect')
    user = db.relationship("User", backref='collect')

class Classes(db.Model):
    __tablename__ = 'class'
    class_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(200), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"))
    course = db.relationship("Course", backref='classes')

class ClasseStudent(db.Model):
    __tablename__ = 'class_student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id = db.Column(db.Integer, db.ForeignKey("class.class_id"))
    stud_id = db.Column(db.String(100), db.ForeignKey("student.id"))
    join_time = db.Column(db.DateTime, default=datetime.now)
    classes = db.relationship("Classes", backref='students')
    students = db.relationship("Student", backref='classes')


#homework
class Homework(db.Model):
    __tablename__ = 'homework'
    hw_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    ddl = db.Column(db.String(200), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("class.class_id"))
    classes = db.relationship("Classes", backref='hws')

class HWProb(db.Model):
    __tablename__ = 'homework_prob'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    prob_id = db.Column(db.Integer, db.ForeignKey("problem.prob_id"))
    hw_id = db.Column(db.Integer, db.ForeignKey("homework.hw_id"))

    prob = db.relationship("Problem", backref='hwprob')
    hw = db.relationship("Homework", backref='hwprob')

class HWProb_score(db.Model):
    __tablename__ = 'hw_prob_score'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hw_prob_id = db.Column(db.Integer, db.ForeignKey("homework_prob.id"))
    stu_id = db.Column(db.String(100), db.ForeignKey("student.id"))
    score = db.Column(db.Integer)
    submit = db.Column(db.Integer)

    hw_prob = db.relationship("HWProb", backref='score')
    student = db.relationship("Student", backref='prob_score')

class HW_score(db.Model):
    __tablename__ = 'hw_score'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hw_id = db.Column(db.Integer, db.ForeignKey("homework.hw_id"))
    stu_id = db.Column(db.String(100), db.ForeignKey("student.id"))
    score = db.Column(db.Integer)

    hw = db.relationship("Homework", backref='score')
    student = db.relationship("Student", backref='hw_score')


#student
class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    UNKNOW = 3

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    telephone = db.Column(db.String(11), nullable=False, unique=True)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), unique=True)
    realname = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)
    join_time = db.Column(db.DateTime, default=datetime.now)
    code = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop("password")
        super(Student, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self._password, rawpwd)


class ForbinComment(db.Model):
    __tablename__ = 'forbin_comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(100), db.ForeignKey("student.id"))
    create_time = db.Column(db.DateTime, default=datetime.now)

    student = db.relationship("Student", backref="forb")


#comment
class Comment(db.Model):
    __tablename__ = 'comment'
    com_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    cleaned_text = db.Column(db.Text)
    keyword = db.Column(db.Text)
    sentiment = db.Column(db.Integer)
    prob_id = db.Column(db.Integer, db.ForeignKey("problem.prob_id"))
    author_id = db.Column(db.String(100), db.ForeignKey("student.id"))

    prob = db.relationship("Problem", backref='comments')
    author = db.relationship("Student", backref='comments')

class ReportComment(db.Model):
    __tablename__ = 'report_comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    com_id = db.Column(db.Integer, db.ForeignKey("comment.com_id"))
    reporter_id = db.Column(db.String(100), db.ForeignKey("student.id"))

    comment = db.relationship("Comment", backref='report')
    reporter = db.relationship("Student", backref='report_com')




class BannerModel(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)



