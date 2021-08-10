from wtforms import Form, StringField, IntegerField, ValidationError, FileField
from wtforms.validators import Email,InputRequired,Length,EqualTo,Regexp
from flask import g
import cache


class LoginForm(Form):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,20,message='请输入正确格式的密码')])
    remember = IntegerField()


class RegisterForm(Form):  
    username = StringField(validators=[Length(2,20,message='请输入正确格式的用户名！')])
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}",message='请输入正确格式的密码！')])
    password_repeat = StringField(validators=[EqualTo("password",message='两次输入的密码不一致！')])
    

class ResetpwdForm(Form):
    oldpwd = StringField(validators=[Length(6,20,message='请输入正确格式的旧密码')])
    newpwd = StringField(validators=[Length(6,20,message='请输入正确格式的新密码')])
    newpwd2 = StringField(validators=[EqualTo("newpwd",message='确认密码必须和新密码保持一致')])

    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message


class ResetEmailForm(Form):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱！')])
    captcha = StringField(validators=[Length(min=6,max=6,message='请输入正确长度的验证码！')])

    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_cache = cache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误！')

    def validate_email(self,field):
        email = field.data
        user = g.user
        if user.email == email:
            raise ValidationError('不能修改为相同的邮箱！')
    
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message


class AddCForm(Form):
    course_name = StringField(validators=[InputRequired(message='请输入课程名称')])

    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message

class ChangeCForm(AddCForm):
    course_id = StringField(validators=[InputRequired(message='请输入课程ID')])


class AddProbForm(Form):
    title = StringField(validators=[InputRequired(message='请输入标题！')])
    content = StringField(validators=[InputRequired(message='请输入内容！')])
    course_id = IntegerField(validators=[InputRequired(message='请输入课程id！')])
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message


class AddClassForm(Form):
    name = StringField(validators=[InputRequired(message='请输入班级名称！')])
    time = StringField(validators=[InputRequired(message='请输入课程时间！')])
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message

class UpdateClassForm(AddClassForm):
    class_id = IntegerField(validators=[InputRequired(message='请输入班级id！')])



class AddCommentForm(Form):
    content = StringField(validators=[InputRequired(message='请输入评论内容！')])
    prob_id = IntegerField(validators=[InputRequired(message='请输入题目id！')])
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message

class AddHWForm(Form):
    title = StringField(validators=[InputRequired(message='请输入标题！')])
    content = StringField(validators=[InputRequired(message='请输入内容！')])
    class_id = IntegerField(validators=[InputRequired(message='请输入课程id！')])
    ddl = StringField(validators=[InputRequired(message='请输入截至日期！')])
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message