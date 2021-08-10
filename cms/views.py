#encoding: utf-8

from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    redirect,
    url_for,
    g,
    jsonify
)
from .forms import (
    LoginForm,
    ResetpwdForm,
    ResetEmailForm,
    AddBannerForm,
    UpdateBannerForm,
    AddBoardForm,
    UpdateBoardForm,
    AddCForm,
    ChangeCForm,
    AddClassForm,
    UpdateClassForm,
    AddProbForm,
    ADDcmsUserForm,
    EditcmsUserForm
)
from flask_paginate import Pagination,get_page_parameter
from .models import CMSUser,CMSPersmission, CMSRole, CMSOper
from  models import BannerModel,Course,Problem,HighlightProbModel,Classes,Comment,User,Student,ForbinComment,ReportComment
from .decorators import login_required,permission_required
import config
from exts import db,mail
from flask_mail import Message
import restful
import cache
import string
import random


bp = Blueprint("cms",__name__,url_prefix='/cms')

def addOpLog(desc):
    oplog = CMSOper(adm_id=g.cms_user.id, desc=desc)
    db.session.add(oplog)
    db.session.commit()

@bp.route('/')
@login_required
def index():
    # g.cms_user
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]
    addOpLog('注销')
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/operation_log/')
@login_required
def operation_log():
    logs = CMSOper.query.filter_by(adm_id=g.cms_user.id)
    context = {
        'logs': logs
    }
    return render_template('cms/cms_oper_log.html',**context)


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请传递邮箱参数！')
    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(0, 10)))
    captcha = "".join(random.sample(source, 6))
    message = Message('SUFE OJ邮箱验证码', recipients=[
                      email], body='您的验证码是：%s' % captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    cache.set(email, captcha)
    return restful.success()


@bp.route('/posts/')
@login_required
@permission_required(CMSPersmission.POSTER)
def posts():
    page = request.args.get(get_page_parameter(),type=int,default=1)
    start = (page-1)*10
    end = start+10
    probs = Problem.query.slice(start,end)
    pagination = Pagination(bs_version=3,page=page,total=Problem.query.filter_by(user=0).count(),outer_window=0,inner_window=2)
    context={
        'posts' : probs,
        'pagination' : pagination
    }
    return render_template('cms/cms_posts.html',**context)


@bp.route('/aposts/',methods=['GET','POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def aposts():
    if request.method == 'GET':
        return render_template('cms/cms_add_prob.html')
    else:
        form = AddProbForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            course_id = form.course_id.data
            prob = Problem(title=title,content=content)
            prob.course_id = course_id
            prob.user = 0
            db.session.add(prob)
            db.session.commit()
            addOpLog('添加题目'+str(title))
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())

@bp.route('/dposts/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def dposts():
    prob_id = request.form.get("prob_id")
    if not prob_id:
        return restful.params_error('请传入题目id！')
    prob = Problem.query.get(prob_id)
    if not prob:
        return restful.params_error(message='没有这个题目！')
    db.session.delete(prob)
    db.session.commit()
    addOpLog('删除题目'+str(prob_id))
    return restful.success()


@bp.route('/hpost/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def hpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入题目id！')
    post = Problem.query.get(post_id)
    if not post:
        return restful.params_error("没有这个题目！")

    highlight = HighlightProbModel()
    highlight.prob = post
    db.session.add(highlight)
    db.session.commit()
    addOpLog('标记热门题目'+str(post_id))
    return restful.success()


@bp.route('/uhpost/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def uhpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入题目id！')
    post = Problem.query.get(post_id)
    if not post:
        return restful.params_error("没有这个题目！")

    highlight = HighlightProbModel.query.filter_by(prob_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    addOpLog('取消标记热门题目'+str(post_id))
    return restful.success()


@bp.route('/detail_comment/<comment_id>')
@login_required
@permission_required(CMSPersmission.COMMENTER)
def detail_comment(comment_id):
    comment = Comment.query.get(comment_id)
    return render_template('cms/cms_comment_info.html',comment=comment)

@bp.route('/comments/')
@login_required
@permission_required(CMSPersmission.COMMENTER)
def comments():
    page = request.args.get(get_page_parameter(),type=int,default=1)
    board = request.args.get('st',type=int,default=None)
    start = (page-1)*10
    end = start+10

    if board == None:
        comments = Comment.query.slice(start,end)
        total=Comment.query.count()
        current_sort = 1
    elif board == 1:
        query_obj = db.session.query(Comment).filter_by(com_id=21)
        comments = query_obj.slice(start,end)
        total=1
        current_sort = 2
    elif board == 2:
        comments = db.session.query(Comment).join(ReportComment, Comment.com_id==ReportComment.com_id).slice(start,end)
        total=db.session.query(Comment).join(ReportComment, Comment.com_id==ReportComment.com_id).count()
        current_sort = 3
    
    pagination = Pagination(bs_version=3,page=page,total=total,outer_window=0,inner_window=2)
    context={
        'comments' : comments,
        'current_sort': current_sort,
        'pagination' : pagination
    }
    return render_template('cms/cms_comments.html',**context)


@bp.route('/dcomments/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.COMMENTER)
def dcomments():
    com_id = request.form.get("com_id")
    if not com_id:
        return restful.params_error('请传入评论id！')
    comment = Comment.query.get(com_id)
    if not comment:
        return restful.params_error(message='没有这个评论！')
    db.session.delete(comment)
    db.session.commit()
    addOpLog('删除评论'+str(com_id))
    return restful.success()


@bp.route('/comment_report/<com_id>')
@login_required
@permission_required(CMSPersmission.COMMENTER)
def comment_report(com_id):
    reports = ReportComment.query.filter_by(com_id=com_id)
    return render_template('cms/cms_comment_report.html',reports=reports)


@bp.route('/dcomment_report/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.COMMENTER)
def dcomment_report():
    report_id = request.form.get("report_id")
    if not report_id:
        return restful.params_error('请传入举报id！')
    report = ReportComment.query.get(report_id)
    if not report:
        return restful.params_error(message='举报已被删除！')
    db.session.delete(report)
    db.session.commit()
    addOpLog('删除举报'+str(report_id))
    return restful.success()


@bp.route('/boards/')
@login_required
@permission_required(CMSPersmission.BOARDER)
def boards():
    courses = Course.query.all()
    context = {
        'courses': courses
    }
    return render_template('cms/cms_boards.html',**context)

@bp.route('/aboard/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def aboard():
    form = AddCForm(request.form)
    if form.validate():
        course_name = form.course_name.data
        user_id = form.user_id.data
        course = Course(course_name=course_name, user=user_id)
        db.session.add(course)
        db.session.commit()
        addOpLog('添加课程'+str(course_name))
        return restful.success()
    else:
        return restful.params_error(form.get_error())


@bp.route('/uboard/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def uboard():
    form = ChangeCForm(request.form)
    if form.validate():
        course_id = form.course_id.data
        course_name = form.course_name.data
        user_id = form.user_id.data
        course = Course.query.get(course_id)
        if course:
            course.course_name = course_name
            course.user = user_id
            db.session.commit()
            addOpLog('修改课程信息,课程ID'+str(course_id))
            return restful.success()
        else:
            return restful.params_error('没有这个课程')
    else:
        return restful.params_error(form.get_error())


@bp.route('/dboard/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def dboard():
    board_id = request.form.get("course_id")
    if not board_id:
        return restful.params_error('请传入课程id！')
    board = Course.query.get(board_id)
    if not board:
        return restful.params_error(message='没有这个课程！')
    db.session.delete(board)
    db.session.commit()
    addOpLog('删除课程'+str(board_id))
    return restful.success()

@bp.route('/class_manage/')
@login_required
@permission_required(CMSPersmission.BOARDER)
def class_manage():
    classes = Classes.query.all()
    context = {
        'classes': classes
    }
    return render_template('cms/cms_class.html',**context)

@bp.route('/eclass/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def eclass():
    form = UpdateClassForm(request.form)
    if form.validate():
        class_id = form.class_id.data
        course_id = form.course_id.data
        name = form.name.data
        time = form.time.data
        classes = Classes.query.get(class_id)
        course = Course.query.get(course_id)
        if course:
            if classes:
                classes.name = name
                classes.time = time
                classes.course = course
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error(message='没有这个班级！')
        else:
            return restful.params_error(message='没有这个课程！')
    else:
        return restful.params_error(message=form.get_error())




@bp.route('/fusers/')
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def fusers():
    users = Student.query.all()
    context = {
        'users': users
    }
    return render_template('cms/cms_fusers.html',**context)


@bp.route('/silence_users/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def silence_users():
    user_id = request.form.get('user_id')
    if not user_id:
        return restful.params_error('请传入用户id！')
    user = Student.query.get(user_id)
    if not user:
        return restful.params_error("没有这个用户！")

    silence = ForbinComment()
    silence.student = user
    db.session.add(silence)
    db.session.commit()
    addOpLog('禁言用户'+str(user.realname))
    return restful.success()

@bp.route('/usilence_users/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def usilence_users():
    user_id = request.form.get("user_id")
    if not user_id:
        return restful.params_error('请传入用户id！')
    user = Student.query.get(user_id)
    if not user:
        return restful.params_error("没有这个用户！")

    silence = ForbinComment.query.filter_by(user_id=user_id).first()
    db.session.delete(silence)
    db.session.commit()
    addOpLog('取消禁言用户'+str(user.realname))
    return restful.success()

@bp.route('/delete_users/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def delete_users():
    user_id = request.form.get("user_id")
    if not user_id:
        return restful.params_error('请传入学生id！')
    student = Student.query.get(user_id)
    if not student:
        return restful.params_error(message='没有这个学生！')
    db.session.delete(student)
    db.session.commit()
    addOpLog('删除用户'+str(user_id))
    return restful.success()

@bp.route('/detail_users/<user_id>')
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def detail_users(user_id):
    student = Student.query.get(user_id)
    return render_template('cms/cms_student_info.html',student=student)




@bp.route('/cusers/')
@login_required
@permission_required(CMSPersmission.CMSUSER)
def cusers():
    users = CMSUser.query.all()
    permissions = CMSRole.query.all()
    context = {
        'users': users,
        'permissions': permissions
    }
    return render_template('cms/cms_cusers.html',**context)

@bp.route('/add_cusers/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.CMSUSER)
def add_cusers():
    form = ADDcmsUserForm(request.form)
    if form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = CMSUser(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        addOpLog('添加管理员'+str(user.username))
        return restful.success()
    else:
        return restful.params_error(form.get_error())

@bp.route('/edit_cusers/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.CMSUSER)
def edit_cusers():
    form = EditcmsUserForm(request.form)
    if form.validate():
        role_id = form.role_id.data
        user_id = form.user_id.data
        role = CMSRole.query.filter_by(id=role_id).first()
        user = CMSUser.query.filter_by(id=user_id).first()
        role.users.append(user)
        db.session.commit()
        addOpLog('更改管理员权限，管理员'+str(user.username))
        return restful.success()
    else:
        return restful.params_error(form.get_error())

@bp.route('/delete_cusers/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.CMSUSER)
def delete_cusers():
    user_id = request.form.get('user_id')
    if not user_id:
        return restful.params_error(message='请传入管理员id！')

    user = CMSUser.query.get(user_id)
    if not user:
        return restful.params_error(message='没有这个管理员！')
    addOpLog('删除管理员'+str(user.username))
    db.session.delete(user)
    db.session.commit()
    return restful.success()

@bp.route('/cuser_operation/<user_id>')
@login_required
@permission_required(CMSPersmission.CMSUSER)
def cuser_operation(user_id):
    logs = CMSOper.query.filter_by(adm_id=user_id)
    context = {
        'logs': logs
    }
    return render_template('cms/cms_oper_log.html',**context)

@bp.route('/croles/')
@login_required
@permission_required(CMSPersmission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')





@bp.route('/banners/')
@login_required
@permission_required(CMSPersmission.POSTER)
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html',banners=banners)


@bp.route('/abanner/',methods=['POST'])
@permission_required(CMSPersmission.POSTER)
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/ubanner/',methods=['POST'])
@permission_required(CMSPersmission.POSTER)
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图！')
    else:
        return restful.params_error(message=form.get_error())

@bp.route('/dbanner/',methods=['POST'])
@permission_required(CMSPersmission.POSTER)
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图id！')

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图！')

    db.session.delete(banner)
    db.session.commit()
    addOpLog('删除轮播图')
    return restful.success()


class LoginView(views.MethodView):

    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                g.cms_user = user
                if remember:
                    session.permanent = True
                addOpLog('登录')
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或密码错误')
        else:
            message = form.get_error()
            return self.get(message=message)

class ResetPwdView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                addOpLog('修改密码')
                return restful.success()
            else:
                return restful.params_error("旧密码错误！")
        else:
            return restful.params_error(form.get_error())


class ResetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')
    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            addOpLog('修改邮箱')
            return restful.success()
        else:
            return restful.params_error(form.get_error())

bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))

