from cffi.cparser import lock


# 查询日志列表
def database_loglist(connection, cursor, userName):
    lock.acquire()
    # 执行数据查询
    sql = "select user.id AS use_id,user.name AS userName,log.content AS logContent, log.time AS logTime from user,log"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result