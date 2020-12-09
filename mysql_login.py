from cffi.cparser import lock


def database_register(connection, cursor, ruser, psw1):
    lock.acquire()
    # 执行数据查询,查询是否重名
    sql = "SELECT password " + "FROM user" + " WHERE name='" + ruser + "'"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchone()
    # 用户名重复
    if result:
        lock.release()
        return 2
    # 注册成功
    else:
        # 插入数据
        sql = "INSERT INTO user (name, password)VALUES('" + ruser + "', '" + psw1 + "');"
        cursor.execute(sql)
        # 提交数据
        connection.commit()
        # 插入数据
        sql = "INSERT INTO rights (use_id,rol_id)VALUES((SELECT id FROM user WHERE name='" + ruser + "), '6');"
        cursor.execute(sql)
        # 提交数据
        connection.commit()
        lock.release()
        return 3


# 登录
def database_login(connection, cursor, iuser, psw):
    lock.acquire()
    # 执行数据查询
    sql = "SELECT * FROM user" + " WHERE name='" + iuser + "' AND password='" + psw + "'"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    # 登陆成功
    if result:
        lock.release()
        return 4
    # 登陆失败
    else:
        lock.release()
        return 1
