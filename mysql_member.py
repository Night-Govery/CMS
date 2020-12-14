from cffi.cparser import lock


# 查询用户列表
def database_memberlist(connection, cursor):
    lock.acquire()
    userlist = []
    userinfo = {'use_id': -1, 'userName': 'NULL', 'roleName': []}
    # 执行数据查询
    sql = "select user.id AS use_id,user.name AS userName,role.name AS roleName from user,role,rights where " \
          "user.id=use_id and " \
          "role.id=rol_id "
    cursor.execute(sql)
    # 获取数据库多条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    flag = 0
    userlist.append(userinfo)
    for a in result:
        count = len(userlist)
        for b in userlist:
            if flag == 0:
                b['use_id'] = a['use_id']
                b['userName'] = a['userName']
                b['roleName'].append(a['roleName'])
                flag = 1
                break
            if a['use_id'] == b['use_id']:
                b['userName'] = a['userName']
                b['roleName'].append(a['roleName'])
            else:
                count = count - 1
        if count == 0:
            temp_userinfo = {'use_id': a['use_id'], 'userName': a['userName'], 'roleName': [a['roleName']]}
            userlist.append(temp_userinfo)
    return userlist


# 更改用户数据
def database_editmember(connection, cursor, uname, urole):
    lock.acquire()
    # 删除用户数据
    sql = "DELETE FROM rights WHERE rights.use_id=(SELECT id FROM user WHERE name ='" + uname + "')"
    cursor.execute(sql)
    # 插入用户数据
    for role in urole:
        sql = "INSERT INTO rights (use_id,rol_id)VALUE((SELECT id FROM user WHERE name ='" + uname + "'),(SELECT id FROM role WHERE name ='" + role + "'))"
        cursor.execute(sql)
    # 提交数据
    connection.commit()
    lock.release()
    return 1


# 更改用户密码
def database_changememberpassword(connection, cursor, userName, password):
    lock.acquire()
    # 更改相关用户密码
    sql = "UPDATE user SET password='" + password + "'WHERE name='" + userName + "'"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    lock.release()
    return 1


# 删除用户
def database_deletemember(connection, cursor, userName):
    lock.acquire()
    # 清楚用户未会签以及未审批操作
    # 删除用户及相关内容
    sql = "DELETE FROM rights WHERE rights.use_id=(SELECT id FROM user WHERE name ='" + userName + "')"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    sql = "DELETE FROM contract_process WHERE contract_process.use_id=(SELECT id FROM user WHERE name ='" + userName + "')"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    sql = "DELETE FROM contract WHERE contract.use_id=(SELECT id FROM user WHERE name ='" + userName + "')"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    sql = "DELETE FROM user WHERE name ='" + userName + "'"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    lock.release()
    return 1


# 添加新用户
def addmember(connection, cursor, userName, password):
    lock.acquire()
    # 执行数据查询,查询是否重名
    sql = "SELECT password " + "FROM user" + " WHERE name='" + userName + "'"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchone()
    # 用户名重复
    if result:
        lock.release()
        return 0
    # 注册成功
    else:
        # 插入数据
        sql = "INSERT INTO user (name, password)VALUES('" + userName + "', '" + password + "');"
        cursor.execute(sql)
        # 提交数据
        connection.commit()
        # 插入数据
        sql = "INSERT INTO rights (use_id,rol_id)VALUES((SELECT id FROM user WHERE name='" + userName + "'),'6');"
        print(sql)
        cursor.execute(sql)
        # 提交数据
        connection.commit()
        lock.release()
        return 1
