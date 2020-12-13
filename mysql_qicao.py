import datetime

from cffi.cparser import lock


# 起草合同
def database_qicao(connection, cursor, name, client, start, end, info, userName):
    lock.acquire()
    timenum = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    # 校验是否有重名合同
    sql = "SELECT id FROM contract WHERE name='" + name + "'"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchone()
    # 合同名重复
    if result:
        lock.release()
        return 0
    # 无重复
    else:
        # 插入数据
        sql = "INSERT INTO contract (name,cus_id,use_id,beginTime,endTime,content)VALUES('" + name + "',(SELECT id FROM customer WHERE name='" + client + "'),(SELECT id FROM user WHERE name='" + userName + "'),'" + start + "','" + end + "','" + info + "');"
        cursor.execute(sql)
        connection.commit()
        sql = "INSERT INTO contract_state (con_id,type,time)VALUES((SELECT id FROM contract WHERE name='" + name + "'),'1','" + timenum + "')"
        cursor.execute(sql)
        # 提交数据
        connection.commit()
        lock.release()
        return 1
