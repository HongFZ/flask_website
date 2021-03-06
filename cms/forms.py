#encoding: utf-8

from wtforms import Form,StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
import cache
from wtforms import ValidationError
from flask import g

class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message
    
    def validate(self):
        return super(BaseForm, self).validate()

class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,20,message='请输入正确格式的密码')])
    remember = IntegerField()


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message='请输入正确格式的旧密码')])
    newpwd = StringField(validators=[Length(6,20,message='请输入正确格式的新密码')])
    newpwd2 = StringField(validators=[EqualTo("newpwd",message='确认密码必须和新密码保持一致')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱！')])
    captcha = StringField(validators=[Length(min=6,max=6,message='请输入正确长度的验证码！')])

    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_cache = zlcache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误！')

    def validate_email(self,field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('不能修改为相同的邮箱！')

class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称！')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图图片链接！')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接！')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级！')])

class UpdateBannerForm(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message='请输入轮播图的id！')])

class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入板块名称！')])

class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message='请输入板块id！')])


class AddCForm(BaseForm):
    course_name = StringField(validators=[InputRequired(message='请输入课程名称')])
    user_id = IntegerField(validators=[InputRequired(message='请输入教师id！')])
    

class ChangeCForm(AddCForm):
    course_id = StringField(validators=[InputRequired(message='请输入课程ID')])


class AddProbForm(BaseForm):
    title = StringField(validators=[InputRequired(message='请输入标题！')])
    content = StringField(validators=[InputRequired(message='请输入内容！')])
    course_id = IntegerField(validators=[InputRequired()])


class AddClassForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入班级名称！')])
    time = StringField(validators=[InputRequired(message='请输入课程时间！')])
    

class UpdateClassForm(AddClassForm):
    class_id = IntegerField(validators=[InputRequired(message='请输入班级id！')])
    course_id = IntegerField(validators=[InputRequired(message='请输入课程id！')])


class ADDcmsUserForm(BaseForm):
    username = StringField(validators=[Length(2,20,message='请输入正确格式的用户名！')])
    email = StringField(validators=[Email(message='请输入正确的邮箱格式'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,25,message='请输入正确格式的密码！')])

class EditcmsUserForm(BaseForm):
    role_id = IntegerField(validators=[InputRequired()])
    user_id = IntegerField(validators=[InputRequired()])