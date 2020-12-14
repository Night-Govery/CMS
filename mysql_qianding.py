import datetime

from cffi.cparser import lock


# 查询待签订列表
def database_daiqianding(connection, cursor, userName):
    lock.acquire()
    # 执行数据查询
    sql = "select DISTINCT contract.name AS contractName, contract_state.time AS contractTime from contract,contract_state,contract_process " \
          "where contract_state.con_id=contract.id and contract_process.con_id=contract.id and contract_state.type=4 and contract_process.use_id=(SELECT id FROM user WHERE name ='" + userName + "') and contract_process.type=3 and contract_process.state=0"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


# 查询已签订列表
def database_yiqianding(connection, cursor, userName):
    lock.acquire()
    # 执行数据查询
    sql = "select DISTINCT contract.name AS contractName, contract_state.time AS contractTime from contract,contract_state,contract_process " \
          "where contract_state.con_id=contract.id and contract_process.con_id=contract.id and contract_state.type=5 and contract_process.use_id=(SELECT id FROM user WHERE name ='" + userName + "') and contract_process.type=3 and contract_process.state=1"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


# 签订合同
def database_qianding(connection, cursor, name, userName, qianding):
    lock.acquire()
    timenum = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    # 更新数据
    sql = "UPDATE contract_process SET content='" + qianding + "',state='1',time='" + timenum + "' WHERE contract_process.con_id=(SELECT id FROM contract WHERE name='" + name + "') and contract_process.use_id=(SELECT id FROM user WHERE name='" + userName + "') and contract_process.type=3"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    # 更新数据
    sql = "UPDATE contract_state SET type='5',time='" + timenum + "' WHERE contract_state.con_id=(SELECT id FROM contract WHERE name='" + name + "') "
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    lock.release()
    return True
