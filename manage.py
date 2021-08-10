from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import app
from exts import db
from models import User,Problem,Classes,Course,Student
from cms import models
import os

CMSUser = models.CMSUser
CMSRole = models.CMSRole
CMSPermission = models.CMSPersmission

manager = Manager(app)

Migrate(app,db)
manager.add_command('db',MigrateCommand)


@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功！')

@manager.command
def create_role():
    visitor = CMSRole(name='访问者',desc='只能访问相关数据，不能修改。')
    visitor.permissions = CMSPermission.VISITOR

    operator = CMSRole(name='运营者',desc='管理课程，题目，评论，轮播图与前台用户。')
    operator.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.CMSUSER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER

    admin = CMSRole(name='管理员',desc='拥有本系统所有权限。')
    admin.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.CMSUSER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER|CMSPermission.BOARDER

    developer = CMSRole(name='开发者',desc='开发人员专用角色。')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()



@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户添加到角色成功！')
        else:
            print('没有这个角色：%s'%role)
    else:
        print('%s邮箱没有这个用户!'%email)



@manager.command
def test_permission():
    user = CMSUser.query.first()
    if user.is_developer:
        print('这个用户有访问者的权限！')
    else:
        print('这个用户没有访问者权限！')


@manager.option('-t','--telephone',dest='telephone')
@manager.option('-r','--realname',dest='realname')
@manager.option('-p','--password',dest='password')
def create_student(telephone,realname,password):
    user = Student(telephone=telephone,realname=realname,password=password)
    db.session.add(user)
    db.session.commit()


@manager.option('-e','--email',dest='email')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(email,username,password):
    user = User(email=email,username=username,password=password)
    db.session.add(user)
    db.session.commit()

@manager.command
def import_probs():
    folder_Path1=r'D:\ZHF\Gra-Paper\Minor\SJTU\Q_content'
    file_list1=os.listdir(folder_Path1)
    for i in file_list1:
        with open(folder_Path1+'\\'+i,'r',encoding='UTF-8') as f:
            text=''
            flag = True
            for j in f.readlines():
                if flag:
                    title = j
                    flag = False
                else:
                    text += j
            prob = Problem(title=title,content=text)
            prob.course_id = 0
            prob.user = 0
            try:
                db.session.add(prob)
                db.session.commit()
            except:
                pass
    print('success')

if __name__ == '__main__':
    manager.run()