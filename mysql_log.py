from cffi.cparser import lock


# 查询日志列表
def database_loglist(connection, cursor, userName):
    lock.acquire()
    # 执行数据查询
    sql = "select log.id AS use_id,user.name AS userName,log.content AS logContent, log.time AS logTime from user,log"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


def database_deletelog(connection, cursor, userName, log_id):
    lock.acquire()
    # 删除
    sql = "DELETE FROM log WHERE id='" + log_id + "'"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    lock.release()
    return None