import datetime

from cffi.cparser import lock


# 查询待分配列表
def database_daifenpei(connection, cursor, userName):
    lock.acquire()
    # 执行数据查询
    sql = "select contract.name AS contractName, contract_state.time AS contractTime from contract,contract_state where " \
          "contract_state.con_id=contract.id and contract_state.type>=1 and contract_state.type<5"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


# 分配会签
def database_fenpeihuiqian(connection, cursor, contractName, fenpeiuser_list, userName):
    lock.acquire()
    timenum = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    sql = "DELETE FROM contract_process WHERE contract_process.con_id=(SELECT id FROM contract WHERE name='" + contractName + "') and contract_process.type=1"
    cursor.execute(sql)
    connection.commit()
    for fenpeiuser in fenpeiuser_list:
        # 检查是否存在重复分配
        sql = "SELECT state FROM contract_process WHERE contract_process.use_id=(SELECT id FROM user WHERE name='" + fenpeiuser + "') and contract_process.con_id=(SELECT id FROM contract WHERE name='" + contractName + "') "
        cursor.execute(sql)
        # 获取数据库单条数据
        result = cursor.fetchone()
        # 重复分配
        if result:
            lock.release()
            return 0
        else:
            sql = "INSERT INTO contract_process(con_id,use_id,type,state)VALUE((SELECT id FROM contract WHERE name='" + contractName + "'),(SELECT id FROM user WHERE name='" + fenpeiuser + "'),'1','0') "
            cursor.execute(sql)
    # 提交数据
    connection.commit()
    # 变更合同状态
    sql = "UPDATE contract_state SET type='1',time='"+ timenum +"' WHERE contract_state.con_id=(SELECT id FROM contract WHERE name='" + contractName + "') and contract_state.type>=1"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    lock.release()
    return 1


# 分配审批
def database_fenpeishenpi(connection, cursor, contractName, fenpeiuser_list, userName):
    lock.acquire()
    timenum = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    sql = "DELETE FROM contract_process WHERE contract_process.con_id=(SELECT id FROM contract WHERE name='" + contractName + "') and contract_process.type=2"
    cursor.execute(sql)
    connection.commit()
    for fenpeiuser in fenpeiuser_list:
        # 检查是否存在重复分配
        sql = "SELECT state FROM contract_process WHERE contract_process.use_id=(SELECT id FROM user WHERE name='" + fenpeiuser + "') and contract_process.con_id=(SELECT id FROM contract WHERE name='" + contractName + "') "
        cursor.execute(sql)
        # 获取数据库单条数据
        result = cursor.fetchone()
        # 重复分配
        if result:
            lock.release()
            return 0
        else:
            sql = "INSERT INTO contract_process(con_id,use_id,type,state)VALUE((SELECT id FROM contract WHERE name='" + contractName + "'),(SELECT id FROM user WHERE name='" + fenpeiuser + "'),'2','0') "
            cursor.execute(sql)
    # 提交数据
    connection.commit()
    # 变更合同状态
    sql = "UPDATE contract_state SET type='3',time='"+ timenum +"' WHERE contract_state.con_id=(SELECT id FROM contract WHERE name='" + contractName + "') and contract_state.type>=3"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    lock.release()
    return 1


# 分配签订
def database_fenpeiqianding(connection, cursor, contractName, fenpeiuser_list, userName):
    lock.acquire()
    timenum = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    sql = "DELETE FROM contract_process WHERE contract_process.con_id=(SELECT id FROM contract WHERE name='" + contractName + "') and contract_process.type=3"
    cursor.execute(sql)
    connection.commit()
    for fenpeiuser in fenpeiuser_list:
        # 检查是否存在重复分配
        sql = "SELECT state FROM contract_process WHERE contract_process.use_id=(SELECT id FROM user WHERE name='" + fenpeiuser + "') and contract_process.con_id=(SELECT id FROM contract WHERE name='" + contractName + "') "
        cursor.execute(sql)
        # 获取数据库单条数据
        result = cursor.fetchone()
        # 重复分配
        if result:
            lock.release()
            return 0
        else:
            sql = "INSERT INTO contract_process(con_id,use_id,type,state)VALUE((SELECT id FROM contract WHERE name='" + contractName + "'),(SELECT id FROM user WHERE name='" + fenpeiuser + "'),'3','0') "
            cursor.execute(sql)
    # 提交数据
    connection.commit()
    # 变更合同状态
    sql = "UPDATE contract_state SET type='4',time='"+ timenum +"' WHERE contract_state.con_id=(SELECT id FROM contract WHERE name='" + contractName + "') and contract_state.type>=4"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    lock.release()
    return 1
