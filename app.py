from flask import (
    Flask,
    render_template,
    request,
    g,
    redirect,
    url_for,
    session,
    views,
    abort,
    make_response,
    jsonify
)
from forms import (
    RegisterForm, 
    LoginForm, 
    ResetpwdForm, 
    ResetEmailForm, 
    AddCForm, 
    ChangeCForm, 
    AddProbForm,
    AddCommentForm,
    AddClassForm,
    UpdateClassForm,
    AddHWForm
)
from models import (
    User, 
    Course, 
    Problem, 
    Comment,
    Classes,
    CollectProb,
    HighlightProbModel,
    Homework,
    HWProb,
    BannerModel,
    Student
)
from flask_wtf import CSRFProtect
from flask_mail import Message
from flask_paginate import Pagination,get_page_parameter
from exts import db, mail
import utils
import config
from decorators import login_required
from ueditor import bp as ueditor_bp
from cms import bp as cms_bp
import restful
import string
import random
import cache
import os
from io import BytesIO
from captcha import Captcha
from sqlalchemy.sql import func

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
CSRFProtect(app)
app.register_blueprint(ueditor_bp)
app.register_blueprint(cms_bp)


#首页
@app.route('/', methods=['GET', 'POST'])
def index():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    context = {
        'banners': banners
    }
    return render_template('index.html',**context)



#教师首页操作
@app.route('/teacher_homepage/')
@login_required
def teacher_homepage():
    courses = Course.query.filter_by(user=g.user.id)
    context = {
        'courses': courses
    }
    return render_template('teacher_homepage.html', **context)

@app.route('/add_course/', methods=['POST'])
@login_required
def add_class():
    form = AddCForm(request.form)
    if form.validate():
        course_name = form.course_name.data
        course = Course(course_name=course_name, user=g.user.id)
        db.session.add(course)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(form.get_error())

@app.route('/change_course/', methods=['POST'])
@login_required
def change_class():
    form = ChangeCForm(request.form)
    if form.validate():
        course_id = form.course_id.data
        course_name = form.course_name.data
        course = Course.query.get(course_id)
        if course:
            course.course_name = course_name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这个课程')
    else:
        return restful.params_error(form.get_error())

@app.route('/delete_course/', methods=['POST'])
@login_required
def delete_class():
    course_id = request.form.get('course_id')
    if not course_id:
        return restful.params_error('请输入课程ID')
    course = Course.query.get(course_id)
    if not course:
        return restful.params_error('没有这个课程')
    db.session.delete(course)
    db.session.commit()
    return restful.success()



#注销
@app.route('/logout/')
@login_required
def logout():
    del session[config.TEACHER_USER_ID]
    return redirect(url_for('login'))



#个人信息
@app.route('/person_info/')
@login_required
def person_info():
    return render_template('person_info.html')


#作业
@app.route('/hw_list/')
@login_required
def hw_list():
    courses = Course.query.filter_by(user=g.user.id)
    probs = Problem.query.filter_by(user=g.user.id)
    context = {
        'courses': courses,
        'probs':probs
    }
    return render_template('hw_list.html', **context)

@app.route('/course_list/')
@login_required
def course_list():
    courses = Course.query.filter_by(user=g.user.id)
    context = {
        'courses': courses
    }
    return render_template('course_list.html', **context)

@app.route('/add_hw/',methods=['GET','POST'])
@login_required
def add_hw():
    if request.method == 'GET':
        course_id = request.args.get('sc',type=int,default=None)
        classes = Classes.query.filter_by(course_id=course_id)
        context = {
            'classes': classes,
            'course_id':course_id
        }
        return render_template('add_hw.html', **context)
    else:
        form = AddHWForm(request.form)
        # attach_file = request.files.get('file')
        # attach_file.save(os.path.join(config.UPLOAD_PATH,attach_file.filename))
        if form.validate():
            title = form.title.data
            content = form.content.data
            class_id = form.class_id.data
            ddl = form.ddl.data

            hw = Homework(name=title,content=content,ddl=ddl)
            hw.class_id = class_id
            
            db.session.add(hw)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())

@app.route('/add_hw_prob/',methods=['POST'])
@login_required
def add_hw_prob():
    prob_id = request.form.get('prob_id')
    hw_id = request.form.get('hw_id')
    if not hw_id:
        return restful.params_error('请输入作业ID')
    comment = HWProb(prob_id=prob_id,hw_id=hw_id)
    db.session.add(comment)
    db.session.commit()
    return restful.success()

@app.route('/dhwprob/', methods=['POST'])
@login_required
def dhwprob():
    hwprob_id = request.form.get('hwprob_id')
    if not hwprob_id:
        return restful.params_error('请输入作业题目ID')
    hwprob = HWProb.query.get(hwprob_id)
    if not hwprob:
        return restful.params_error('没有这个作业题目信息')
    db.session.delete(hwprob)
    db.session.commit()
    return restful.success()


@app.route('/delete_hw/', methods=['POST'])
@login_required
def delete_hw():
    hw_id = request.form.get('hw_id')
    if not hw_id:
        return restful.params_error('请输入作业ID')
    hw = Homework.query.get(hw_id)
    if not hw:
        return restful.params_error('没有这个作业')
    db.session.delete(hw)
    db.session.commit()
    return restful.success()

@app.route('/hw_detail/<hw_id>')
@login_required
def hw_detail(hw_id):
    hw = Homework.query.get(hw_id)
    probs = Problem.query.filter_by(user=g.user.id)
    if not hw:
        abort(404)
    hwprob = hw.hwprob
    context={
        'hw' : hw,
        'hwprob' : hwprob,
        'probs':probs
    }
    return render_template('hw_detail.html',**context)

@app.route('/homework/<hwprob_id>')
@login_required
def homework(hwprob_id):
    hwprob = HWProb.query.get(hwprob_id)
    return render_template('homework.html', hwprob=hwprob)

@app.route('/homework/getscore/<hwprob_id>',methods=['POST'])
@login_required
def homework_getscore(hwprob_id):
    hwprob = HWProb.query.get(hwprob_id)
    if not hwprob:
        abort(404)
    scores = hwprob.score
    s1,s2,s3,s4,s5 = 0,0,0,0,0
    sum1,sum2,sum3,sum4,sum5 = 0,0,0,0,0
    for i in scores:
        i=i.score
        if i<60 : s1+=1;sum1+=i
        elif i<70: s2+=1;sum2+=i
        elif i<80: s3+=1;sum3+=i
        elif i<90: s4+=1;sum4+=i
        else: s5+=1;sum5+=i
    count=[s1,s2,s3,s4,s5]
    sum_list=[sum1,sum2,sum3,sum4,sum5]
    avg=[]
    for i in range(5):
        if count[i] == 0:
            avg.append(0)
        else:
            avg.append(sum_list[i]/count[i])
    sb1,sb2,sb3,sb4,sb5 = 0,0,0,0,0
    for i in scores:
        i=i.submit
        if i<2 : sb1+=1
        elif 1<i<3: sb2+=1
        elif 2<i<6: sb3+=1
        elif 5<i<11: sb4+=1
        else: sb5+=1
    submit=[{'value':sb1,'name':"1次通过"},{'value':sb2,'name':"2次尝试后通过"},
            {'value':sb3,'name':"3-5次尝试后通过"},{'value':sb4,'name':"6-10次尝试后通过"},
            {'value':sb5,'name':"10次以上"}]
    return jsonify({"count" : count, 'avg':avg, 'submit':submit})



#班级
@app.route('/class_manage/<course_id>')
@login_required
def class_manage(course_id):
    classes = Classes.query.filter_by(course_id=course_id)
    context = {
        'classes': classes,
        'course_id': course_id
    }
    return render_template('class_manage.html', **context)

@app.route('/aclass/<course_id>',methods=['POST'])
@login_required
def aclass(course_id):
    form = AddClassForm(request.form)
    if form.validate():
        name = form.name.data
        time = form.time.data
        classes = Classes(name=name,time=time,course_id=course_id)
        db.session.add(classes)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@app.route('/eclass/',methods=['POST'])
@login_required
def eclass():
    form = UpdateClassForm(request.form)
    if form.validate():
        class_id = form.class_id.data
        name = form.name.data
        time = form.time.data
        classes = Classes.query.get(class_id)
        if classes:
            classes.name = name
            time = time
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个班级！')
    else:
        return restful.params_error(message=form.get_error())

@app.route('/dclass/',methods=['POST'])
@login_required
def dclass():
    class_id = request.form.get('class_id')
    if not class_id:
        return restful.params_error(message='请传入班级id！')

    classes = Classes.query.get(class_id)
    if not classes:
        return restful.params_error(message='没有这个班级！')

    db.session.delete(classes)
    db.session.commit()
    return restful.success()

@app.route('/students_check/<class_id>')
@login_required
def students_check(class_id):
    classes = Classes.query.get(class_id)
    student = classes.students
    context = {
        'student': student
    }
    return render_template('student_list.html', **context)

@app.route('/student_detail/<stu_id>')
@login_required
def student_detail(stu_id):
    student = Student.query.get(stu_id)
    context = {
        'student': student
    }
    return render_template('student_detail.html', **context)


#添加题目
@app.route('/add_prob/',methods=['GET','POST'])
@login_required
def add_prob():
    if request.method == 'GET':
        course = Course.query.filter_by(user=g.user.id)
        return render_template('add_prob.html',courses=course)
    else:
        form = AddProbForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            course_id = form.course_id.data
            course = Course.query.get(course_id)
            if not course:
                return restful.params_error(message='没有这个课程！')
            prob = Problem(title=title,content=content)
            prob.course_id = course_id
            prob.user = g.user.id
            db.session.add(prob)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())

#公共题目列表
@app.route('/problem_list/')
@login_required
def problem_list():
    page = request.args.get(get_page_parameter(),type=int,default=1)
    sort = request.args.get('st',type=int,default=0)

    query_obj = None
    if sort == 0:
        query_obj = Problem.query.filter_by(user=0)
        current_sort = 1
    elif sort == 1:
        query_obj = db.session.query(Problem).filter_by(user=0).outerjoin(HighlightProbModel).order_by(
            HighlightProbModel.create_time.desc(),Problem.prob_id
            )
        current_sort = 2
    elif sort == 2:
        query_obj = db.session.query(Problem).filter_by(user=0).outerjoin(CollectProb).group_by(Problem.prob_id).order_by(
            func.count(CollectProb.id).desc(),Problem.prob_id
            )
        current_sort = 3
    elif sort == 3:
        query_obj = db.session.query(Problem).filter_by(user=0).outerjoin(Comment).group_by(Problem.prob_id).order_by(
            func.count(Comment.com_id).desc(),Problem.prob_id
            )
        current_sort = 4

    start = (page-1)*config.PER_PAGE
    end = start+config.PER_PAGE
    probs = query_obj.slice(start,end)
    pagination = Pagination(bs_version=3,page=page,total=Problem.query.filter_by(user=0).count(),outer_window=0,inner_window=2)
    context={
        'problems' : probs,
        'pagination' : pagination,
        'current_sort' : current_sort
    }
    return render_template('problem_list.html', **context)

#个人题目列表
@app.route('/person_prob_list/')
@login_required
def person_prob_list():
    board_id = request.args.get('bd',type=int,default=None)
    page = request.args.get(get_page_parameter(),type=int,default=1)
    start = (page-1)*config.PER_PAGE
    end = start+config.PER_PAGE
    if board_id:
        q = CollectProb.query.filter_by(user_id=g.user.id)
        probs = q.order_by(
            CollectProb.create_time.desc()
        )
        st = 1
        total =  q.count()
    else:
        probs = Problem.query.filter_by(user=g.user.id).slice(start,end)
        st = 0
        total = Problem.query.filter_by(user=g.user.id).count()
    pagination = Pagination(bs_version=3,page=page,total=total,outer_window=0,inner_window=2)
    context={
        'problems' : probs,
        'pagination' : pagination,
        'st' : st
    }
    return render_template('person_prob_list.html', **context)

#题目详情
@app.route('/p/<prob_id>/')
def post_detail(prob_id):
    problem = Problem.query.get(prob_id)
    if not problem:
        abort(404)
    user_id = g.user.id
    if user_id == int(problem.user):
        is_creater = 0
    else:
        is_creater = 1
    count = CollectProb.query.filter_by(
        user_id = user_id,
        prob_id = prob_id
    ).count()
    context={
        'problem' : problem,
        'count' : count,
        'is_creater':is_creater
    }
    return render_template('pdetail.html',**context)

#收藏题目
@app.route('/collect_prob/')
def collect_prob():
    prob_id = request.args.get('prob_id','')
    user_id = g.user.id
    collect = CollectProb.query.filter_by(
        user_id = user_id,
        prob_id = prob_id
    ).count()
    if collect ==1 :
        return restful.params_error("已收藏！")
    else:
        collect = CollectProb(user_id=user_id,prob_id=prob_id)
        db.session.add(collect)
        db.session.commit()
        return restful.success()

@app.route('/dcollect_prob/')
def dcollect_prob():
    prob_id = request.args.get('prob_id','')
    user_id = g.user.id
    collect = CollectProb.query.filter_by(
        user_id = user_id,
        prob_id = prob_id
    ).first()
    
    db.session.delete(collect)
    db.session.commit()
    return restful.success()

#添加评论
@app.route('/acomment/',methods=['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        prob_id = form.prob_id.data
        author_id = g.user.id       
        comment = Comment(content=content,prob_id=prob_id,author_id=author_id)
        db.session.add(comment)
        db.session.commit()
        return restful.success()
        
    else:
        return restful.params_error(form.get_error())

@app.route('/comment/<prob_id>/')
@login_required
def comment(prob_id):
    comments = Comment.query.filter_by(prob_id=prob_id)
    context={
        'comments': comments,
        'prob_id': prob_id
    }
    return render_template('comment.html',**context)


#用户登录
class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('login.html', message=message)
    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.TEACHER_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('teacher_homepage'))
            else:
                return self.get(message='邮箱或密码错误')
        else:
            message = form.errors.popitem()[1][0]
            return self.get(message=message)
app.add_url_rule('/login/', view_func=LoginView.as_view('login'))


#用户注册
class RegistView(views.MethodView):
    def get(self, message=None):
        return render_template('register.html', message=message)

    def post(self):
        form = RegisterForm(request.form)
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            user = User(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            message = form.errors.popitem()[1][0]
            return self.get(message=message)
app.add_url_rule('/register/', view_func=RegistView.as_view('register'))


#修改密码
class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # {"code":200,message=""}
                # return jsonify({"code":200,"message":""})
                return restful.success()
            else:
                return restful.params_error("旧密码错误！")
        else:
            return restful.params_error(form.get_error())
app.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))


#修改邮箱
@app.route('/email_captcha/')
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


class ResetEmailView(views.MethodView):
    decorators = [login_required]
    def get(self):
        return render_template('resetemail.html')
    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())
app.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))


@app.route('/captcha/')
def graph_captcha():
    text,image = Captcha.gene_graph_captcha()
    cache.set(text.lower(),text.lower())
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


@app.before_request
def before_request():
    if config.TEACHER_USER_ID in session:
        user_id = session.get(config.TEACHER_USER_ID)
        user = User.query.get(user_id)
        if user:
            g.user = user

@app.errorhandler
def page_not_found():
    return render_template('404.html'),404


if __name__ == "__main__":
    app.run()

