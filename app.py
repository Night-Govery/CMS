import pymysql
from flask import Flask, render_template, request, redirect, url_for, session, make_response

import configs

# !/usr/bin/python
# -*- coding: UTF-8 -*-
import mysql_contract
import mysql_customer
import mysql_dinggao
import mysql_fenpei
import mysql_huiqian
import mysql_log
import mysql_login
import mysql_member
import mysql_qianding
import mysql_qicao
import mysql_role
import mysql_shenpi
import mysql_user

app = Flask(__name__)
# 加密通话
app.secret_key = '234sdqwe324234'

# 连接MySQL数据库
connection = pymysql.connect(host=configs.HOST, port=configs.PORT, user=configs.USERNAME, password=configs.PASSWORD,
                             db=configs.DATABASE,
                             charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
# 通过cursor创建游标
cursor = connection.cursor()


# 欢迎(已完成)
@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        return render_template('welcome.html')


# # 报错(已完成)
# @app.route('/error', methods=['GET', 'POST'])
# def error():
#     # 如果没有登录，就返回登录页
#     if "username" not in session:
#         return redirect(url_for('index'))
#     # 如果登录，就前往页面
#     else:
#         return render_template('error.html')


# 无权限页(已完成)
@app.route('/nopermission', methods=['GET', 'POST'])
def nopermission():
    return render_template('nopermission.html')


# 设置session(已完成)
@app.route('/set_session/<username>')
def set_session(username):
    response = make_response(redirect(url_for("index")))
    result_permission = mysql_user.database_getuserpermission(connection, cursor, username)
    session["username"] = username
    session["起草合同"] = result_permission['起草合同']
    session["会签合同"] = result_permission['会签合同']
    session["定稿合同"] = result_permission['定稿合同']
    session["审批合同"] = result_permission['审批合同']
    session["签订合同"] = result_permission['签订合同']
    session["查询合同信息"] = result_permission['查询合同信息']
    session["查询合同流程"] = result_permission['起草合同']
    session["分配会签"] = result_permission['分配会签']
    session["分配审批"] = result_permission['分配审批']
    session["分配签订"] = result_permission['分配签订']
    session["新增角色"] = result_permission['新增角色']
    session["编辑角色"] = result_permission['编辑角色']
    session["查询角色"] = result_permission['查询角色']
    session["删除角色"] = result_permission['删除角色']
    session["新增用户"] = result_permission['新增用户']
    session["编辑用户"] = result_permission['编辑用户']
    session["查询用户"] = result_permission['查询用户']
    session["删除用户"] = result_permission['删除用户']
    session["查询日志"] = result_permission['查询日志']
    session["删除日志"] = result_permission['删除日志']
    session["管理合同信息"] = result_permission['管理合同信息']
    session["新增客户"] = result_permission['新增客户']
    session["编辑客户"] = result_permission['编辑客户']
    session["查询客户"] = result_permission['查询客户']
    session["删除客户"] = result_permission['删除客户']
    return response


# 登出页(已完成)
@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("index")))
    # 如果是登录状态，就删除session和session
    if "username" in session:
        # 删除session
        session.pop("username")
    return response


# 用户设置(已完成)
@app.route('/one_set/<username>', methods=['GET', 'POST'])
def oneset(username):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        message = -1
        if request.method == 'POST':
            username = session.get('username')
            newpass = request.form.get('password')
            message = mysql_member.database_changememberpassword(connection, cursor, username, newpass, username)
        return render_template('one_set.html', message=message, username=username)


# 主页(已完成)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 登录信息
        iuser = request.form.get('iuser')
        psw = request.form.get('psw')
        # 注册信息
        ruser = request.form.get('ruser')
        psw1 = request.form.get('psw1')
        psw2 = request.form.get('psw2')
        username = session.get('username')
        # 登陆界面
        if iuser and psw:
            message = mysql_login.database_login(connection, cursor, iuser, psw, username)
            if message == 4:
                return redirect(url_for('set_session', username=iuser))
            else:
                return render_template('index.html', message=message)
        # 注册界面
        if ruser and psw1 and psw2:
            message = mysql_login.database_register(connection, cursor, ruser, psw1, username)
            return render_template('index.html', message=message)
    # 检测session是否存在“username”项
    if "username" not in session:
        # 如果没有username，则进入登录页
        return render_template('index.html')
    else:
        # 如果有，则证明已经登录，进入主页
        return redirect(url_for('main'))


# 主页框架(已完成)
@app.route('/main', methods=['GET', 'POST'])
def main():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        username = session.get('username')
        return render_template('main.html', username=username, permission_list=session)


# 起草合同(已完成)
@app.route('/qicao', methods=['GET', 'POST'])
def qicao():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('起草合同'):
            # 获取请求
            message = -1
            username = session.get('username')
            if request.method == 'POST':
                name = request.form.get('name')
                client = request.form.get('client')
                start = request.form.get('start')
                end = request.form.get('end')
                info = request.form.get('info')
                message = mysql_qicao.database_qicao(connection, cursor, name, client, start, end, info, username)
            customer_list = mysql_customer.database_customerlist(connection, cursor, username)
            return render_template('qicao.html', message=message, customer_list=customer_list)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 待会签(已完成)
@app.route('/daihuiqian', methods=['GET', 'POST'])
def daihuiqian():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('会签合同'):
            username = session.get('username')
            daihuiqian_list = mysql_huiqian.database_daihuiqian(connection, cursor, username)
            return render_template('daihuiqian.html', daihuiqian_list=daihuiqian_list)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 已会签(已完成)
@app.route('/yihuiqian', methods=['GET', 'POST'])
def yihuiqian():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('会签合同'):
            username = session.get('username')
            yihuiqian_list = mysql_huiqian.database_yihuiqian(connection, cursor, username)
            return render_template('yihuiqian.html', yihuiqian_list=yihuiqian_list)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 会签合同(已完成)
@app.route('/huiqian/<contractName>', methods=['GET', 'POST'])
def huiqian(contractName):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('会签合同'):
            message = -1
            if request.method == 'POST':
                info = request.form.get('info')
                userName = session.get('username')
                message = mysql_huiqian.database_huiqian(connection, cursor, contractName, userName, info)
            return render_template('huiqian.html', contractName=contractName, message=message)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 待定稿(已完成)
@app.route('/daidinggao', methods=['GET', 'POST'])
def daidinggao():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('定稿合同'):
            username = session.get('username')
            daidinggao_list = mysql_dinggao.database_daidinggao(connection, cursor, username)
            return render_template('daidinggao.html', daidinggao_list=daidinggao_list)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 已定稿
@app.route('/yidinggao', methods=['GET', 'POST'])
def yidinggao():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('定稿合同'):
            username = session.get('username')
            yidinggao_list = mysql_dinggao.database_yidinggao(connection, cursor, username)
            return render_template('yidinggao.html', yidinggao_list=yidinggao_list)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 定稿(已完成)
@app.route('/dinggao/<contractName>', methods=['GET', 'POST'])
def dinggao(contractName):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('定稿合同'):
            message = -1
            username = session.get('username')
            if request.method == 'POST':
                info = request.form.get('info')
                message = mysql_dinggao.database_dinggao(connection, cursor, contractName, username, info)
            contract = mysql_contract.database_getcontractinfo(connection, cursor, contractName, username)
            return render_template('dinggao.html', contractName=contractName, message=message, contract=contract)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 待审批
@app.route('/daishenpi', methods=['GET', 'POST'])
def daishenpi():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('审批合同'):
            username = session.get('username')
            daishenpi_list = mysql_shenpi.database_daishenpi(connection, cursor, username)
            return render_template('daishenpi.html', daishenpi_list=daishenpi_list)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 已审批
@app.route('/yishenpi', methods=['GET', 'POST'])
def yishenpi():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('审批合同'):
            username = session.get('username')
            yishenpi_list = mysql_shenpi.database_yishenpi(connection, cursor, username)
            return render_template('yishenpi.html', yishenpi_list=yishenpi_list)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 审批
@app.route('/shenpi/<contractName>', methods=['GET', 'POST'])
def shenpi(contractName):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('审批合同'):
            message = -1
            if request.method == 'POST':
                state = request.form.get('state')
                info = request.form.get('info')
                userName = session.get('username')
                message = mysql_shenpi.database_shenpi(connection, cursor, contractName, userName, state, info)
            return render_template('shenpi.html', contractName=contractName, message=message)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 待签定
@app.route('/daiqianding', methods=['GET', 'POST'])
def daiqianding():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('签订合同'):
            username = session.get('username')
            daiqianding_list = mysql_qianding.database_daiqianding(connection, cursor, username)
            return render_template('daiqianding.html', daiqianding_list=daiqianding_list)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 已签订
@app.route('/yiqianding', methods=['GET', 'POST'])
def yiqianding():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('签订合同'):
            username = session.get('username')
            yiqianding_list = mysql_qianding.database_yiqianding(connection, cursor, username)
            return render_template('yiqianding.html', yiqianding_list=yiqianding_list)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 签订
@app.route('/qianding/<contractName>', methods=['GET', 'POST'])
def qianding(contractName):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('签订合同'):
            message = -1
            username = session.get('username')
            if request.method == 'POST':
                info = request.form.get('info')
                message = mysql_qianding.database_qianding(connection, cursor, contractName, username, info)
            contract = mysql_contract.database_getcontractinfo(connection, cursor, contractName, username)
            return render_template('qianding.html', contractName=contractName, message=message, contract=contract)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 待分配(已完成)
@app.route('/daifenpei', methods=['GET', 'POST'])
def daifenpei():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('分配会签') or session.get('分配审批') or session.get('分配签订'):
            username = session.get('username')
            constract_list = mysql_fenpei.database_daifenpei(connection, cursor, username)
            return render_template('daifenpei.html', constract_list=constract_list)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 分配会签(已完成)
@app.route('/fenpeihuiqian/<constractName>', methods=['GET', 'POST'])
def fenpeihuiqian(constractName):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('分配会签'):
            message = -1
            username = session.get('username')
            user_list = mysql_member.database_memberlist(connection, cursor, username)
            if request.method == 'POST':
                huiqian_list = request.form.getlist('huiqian')
                message = mysql_fenpei.database_fenpeihuiqian(connection, cursor, constractName, huiqian_list, username)
            return render_template('fenpeihuiqian.html', user_list=user_list, message=message,
                                   constractName=constractName)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 分配审批(已完成)
@app.route('/fenpeishenpi/<constractName>', methods=['GET', 'POST'])
def fenpeishenpi(constractName):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('分配审批'):
            message = -1
            userName = session.get('username')
            user_list = mysql_member.database_memberlist(connection, cursor, userName)
            if request.method == 'POST':
                huiqian_list = request.form.getlist('shenpi')
                message = mysql_fenpei.database_fenpeishenpi(connection, cursor, constractName, huiqian_list, userName)
            return render_template('fenpeishenpi.html', user_list=user_list, message=message,
                                   constractName=constractName)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 分配签订(已完成)
@app.route('/fenpeiqianding/<constractName>', methods=['GET', 'POST'])
def fenpeiqianding(constractName):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('分配签订'):
            message = -1
            userName = session.get('username')
            user_list = mysql_member.database_memberlist(connection, cursor, userName)
            if request.method == 'POST':
                huiqian_list = request.form.getlist('qianding')
                message = mysql_fenpei.database_fenpeiqianding(connection, cursor, constractName, huiqian_list,
                                                               userName)
            return render_template('fenpeiqianding.html', user_list=user_list, message=message,
                                   constractName=constractName)
        # 无权限
        else:
            return redirect(url_for('fenpeiqianding'))


# 新增角色
@app.route('/role-add', methods=['GET', 'POST'])
def roleadd():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('新增角色'):
            return render_template('role-add.html')
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 编辑角色
@app.route('/role-edit/<roleName>', methods=['GET', 'POST'])
def roleedit(roleName):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('编辑角色'):

            return render_template('role-edit.html', roleName=roleName)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 查询角色(已完成)
@app.route('/role', methods=['GET', 'POST'])
def role():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        if session.get('查询角色'):
            userName = session.get('username')
            role_list = mysql_role.database_rolelist(connection, cursor, userName)
            return render_template('role.html', role_list=role_list)
        else:
            return redirect(url_for('nopermission'))


# 删除角色
@app.route('/role-delete/<roleName>', methods=['GET', 'POST'])
def roledelete(roleName):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('删除角色'):
            userName = session.get('username')
            message = mysql_role.database_deleterole(connection, cursor, roleName, userName)
            role_list = mysql_role.database_rolelist(connection, cursor, userName)
            return render_template('role.html', role_list=role_list, message=message)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 新增用户(已完成)
@app.route('/member-add', methods=['GET', 'POST'])
def memberadd():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('新增用户'):
            message = -1
            if request.method == 'POST':
                userName = request.form.get('username')
                password = request.form.get('password')
                message = mysql_member.database_addmember(connection, cursor, userName, password)
            return render_template('member-add.html', message=message)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 编辑用户(已完成)
@app.route('/member-edit/<change_member>', methods=['GET', 'POST'])
def memberedit(change_member):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('编辑用户'):
            message = -1
            userName = session.get('username')
            if request.method == 'POST':
                uname = request.form.get('name')
                urole = request.form.getlist('status')
                message = mysql_member.database_editmember(connection, cursor, uname, urole, userName)
            role_list = mysql_role.database_rolelist(connection, cursor, userName)
            return render_template('member-edit.html', role_list=role_list, change_member=change_member,
                                   message=message)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 更改用户密码(已完成)
@app.route('/member-password/<membername>', methods=['GET', 'POST'])
def memberpassword(membername):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 有权限
        if session.get('编辑用户'):
            message = -1
            userName = session.get('username')
            if request.method == 'POST':
                # 登录信息
                newpass = request.form.get('newpass')
                message = mysql_member.database_changememberpassword(connection, cursor, membername, newpass, userName)
            return render_template('member-password.html', message=message, membername=membername)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 查询用户(已完成)
@app.route('/member-list', methods=['GET', 'POST'])
def memberlist():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        if session.get('查询用户'):
            message = -1
            userName = session.get('username')
            member_list = mysql_member.database_memberlist(connection, cursor, userName)
            return render_template('member-list.html', member_list=member_list, message=message)
        else:
            return redirect(url_for('nopermission'))


# 删除用户
@app.route('/member-delete/<delete_member>', methods=['GET', 'POST'])
def memberdelete(delete_member):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('删除用户'):
            userName = session.get('username')
            message = mysql_member.database_deletemember(connection, cursor, delete_member, userName)
            member_list = mysql_member.database_memberlist(connection, cursor, userName)
            return render_template('member-list.html', member_list=member_list, message=message)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 查询日志
@app.route('/log', methods=['GET', 'POST'])
def log():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('查询日志'):
            message = -1
            userName = session.get('username')
            log_list = mysql_log.database_loglist(connection, cursor, userName)
            return render_template('log.html', log_list=log_list, message=message)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 删除日志
@app.route('/log/<log_id>', methods=['GET', 'POST'])
def logdelete(log_id):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('删除日志'):
            userName = session.get('username')
            message = mysql_log.database_deletelog(connection, cursor, userName, log_id)
            log_list = mysql_log.database_loglist(connection, cursor, userName)
            return render_template('log.html', log_list=log_list, message=message)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 查询客户
@app.route('/customer-list', methods=['GET', 'POST'])
def customerlist():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('查询客户'):
            userName = session.get('username')
            customer_list = mysql_customer.database_customerlist(connection, cursor, userName)
            return render_template('customer-list.html', customer_list=customer_list)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 新增客户
@app.route('/customer-add', methods=['GET', 'POST'])
def customeradd():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('新增客户'):
            message = -1
            if request.method == 'POST':
                name = request.form.get('name')
                phone = request.form.get('phone')
                address = request.form.get('address')
                fax = request.form.get('fax')
                code = request.form.get('code')
                bankname = request.form.get('bankname')
                bankaccount = request.form.get('bankaccount')
                message = mysql_customer.database_addcustomer(connection, cursor, name, address, phone, fax, code,
                                                              bankname, bankaccount)
            return render_template('customer-add.html', message=message)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 编辑客户
@app.route('/customer-edit/<customerName>,<phone>,<address>,<fax>,<code>,<bankname>,<bankaccount>',
           methods=['GET', 'POST'])
def customeredit(customerName, phone, address, fax, code, bankname, bankaccount):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('编辑客户'):
            message = -1
            if request.method == 'POST':
                phone = request.form.get('phone')
                address = request.form.get('address')
                fax = request.form.get('fax')
                code = request.form.get('code')
                bankname = request.form.get('bankname')
                bankaccount = request.form.get('bankaccount')
                message = mysql_customer.database_editcustomer(connection, cursor, customerName, address, phone, fax,
                                                               code, bankname,
                                                               bankaccount)
            return render_template('customer-edit.html', customerName=customerName, message=message, phone=phone,
                                   address=address, fax=fax, code=code, bankname=bankname, bankaccount=bankaccount)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 删除客户
@app.route('/customer-delete/<customerName>', methods=['GET', 'POST'])
def customerdelete(customerName):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('删除客户'):
            userName = session.get('username')
            message = mysql_customer.database_deletecustomer(connection, cursor, customerName, userName)
            customer_list = mysql_customer.database_customerlist(connection, cursor, userName)
            return render_template('customer-list.html', customer_list=customer_list, message=message)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 查询合同
@app.route('/contract-list', methods=['GET', 'POST'])
def contractlist():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('查询客户'):
            userName = session.get('username')
            customer_list = mysql_customer.database_customerlist(connection, cursor, userName)
            return render_template('contract-list.html', customer_list=customer_list)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 新增合同
@app.route('/contract-add', methods=['GET', 'POST'])
def contractadd():
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('新增客户'):
            # 获取请求
            message = -1
            username = session.get('username')
            if request.method == 'POST':
                name = request.form.get('name')
                client = request.form.get('client')
                start = request.form.get('start')
                end = request.form.get('end')
                info = request.form.get('info')
                message = mysql_qicao.database_qicao(connection, cursor, name, client, start, end, info, username)
            customer_list = mysql_customer.database_customerlist(connection, cursor, username)
            return render_template('contract-add.html', message=message, customer_list=customer_list)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 编辑合同
@app.route('/contract-edit/<customerName>,<phone>,<address>,<fax>,<code>,<bankname>,<bankaccount>',
           methods=['GET', 'POST'])
def contractedit(customerName, phone, address, fax, code, bankname, bankaccount):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('编辑客户'):
            message = -1
            if request.method == 'POST':
                phone = request.form.get('phone')
                address = request.form.get('address')
                fax = request.form.get('fax')
                code = request.form.get('code')
                bankname = request.form.get('bankname')
                bankaccount = request.form.get('bankaccount')
                message = mysql_customer.database_editcustomer(connection, cursor, customerName, address, phone, fax,
                                                               code, bankname,
                                                               bankaccount)
            return render_template('contract-edit.html', customerName=customerName, message=message, phone=phone,
                                   address=address, fax=fax, code=code, bankname=bankname, bankaccount=bankaccount)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 删除合同
@app.route('/contract-delete/<customerName>', methods=['GET', 'POST'])
def contractdelete(customerName):
    # 如果没有登录，就返回登录页
    if "username" not in session:
        return redirect(url_for('index'))
    # 如果登录，就前往页面
    else:
        # 校验权限
        # 有权限
        if session.get('删除客户'):
            userName = session.get('username')
            message = mysql_customer.database_deletecustomer(connection, cursor, customerName, userName)
            customer_list = mysql_customer.database_customerlist(connection, cursor, userName)
            return render_template('contract-list.html', customer_list=customer_list, message=message)
        # 无权限
        else:
            return redirect(url_for('nopermission'))


# 启动服务器
if __name__ == '__main__':
    app.run(debug=True)
