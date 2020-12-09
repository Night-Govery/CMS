import datetime

from cffi.cparser import lock


# 查询待会签列表
def database_daihuiqian(connection, cursor, userName):
    lock.acquire()
    # 执行数据查询
    sql = "select DISTINCT contract.name AS contractName, contract_state.time AS contractTime from contract,contract_state,contract_process " \
          "where contract_state.con_id=contract.id and contract_state.type=1 and contract_process.use_id=(SELECT id FROM user WHERE name ='" + userName + "') and contract_process.type=1 and contract_process.state=0"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


# 查询已会签列表
def database_yihuiqian(connection, cursor, userName):
    lock.acquire()
    # 执行数据查询
    sql = "select DISTINCT contract.name AS contractName, contract_state.time AS contractTime from contract,contract_state,contract_process" \
          " where contract_state.con_id=contract.id and contract_state.type=2 and contract_process.use_id=(SELECT id FROM user WHERE name ='" + userName + "') and contract_process.type=1 and contract_process.state=1"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


# 会签合同
def database_huiqian(connection, cursor, name, userName, yijian):
    lock.acquire()
    timenum = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    # 更新数据
    sql = "UPDATE contract_process SET content='" + yijian + "',state='1',time='" + timenum + "' WHERE contract_process.con_id=(SELECT id FROM contract WHERE name='" + name + "') and contract_process.use_id=(SELECT id FROM user WHERE name='" + userName + "') and contract_process.type=1"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    # 执行数据查询,查询是否全部会签
    sql = "SELECT use_id FROM contract_process WHERE contract_process.con_id=(SELECT id FROM contract WHERE name='" + name + "') and contract_process.type=1 and contract_process.state=0"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchone()
    # 全部会签完毕
    if result:
        lock.release()
        return True
    else:
        sql = "UPDATE contract_state SET type='2', time='" + timenum + "' WHERE contract_state.con_id=(SELECT id FROM contract WHERE name='" + name + "') and contract_state.type=1"
        cursor.execute(sql)
        # 提交数据
        connection.commit()
    lock.release()
    return True
