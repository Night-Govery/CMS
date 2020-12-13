import datetime

from cffi.cparser import lock


# 查询待签订列表
def database_daiqianding(connection, cursor):
    lock.acquire()
    # 执行数据查询
    sql = "select contract.name AS contractName, contract_state.time AS contractTime from contract,contract_state where " \
          "contract_state.con_id=contract.id and contract_state.type=4 "
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


# 查询已签订列表
def database_yiqianding(connection, cursor):
    lock.acquire()
    # 执行数据查询
    sql = "select contract.name AS contractName, contract_state.time AS contractTime from contract,contract_state where " \
          "contract_state.con_id=contract.id and contract_state.type=5 "
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


# 签订合同
def database_huiqian(connection, cursor, name, userName, qianding):
    lock.acquire()
    timenum = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    # 更新数据
    sql = "UPDATE contract_process SET content='" + qianding + "',state='1',time='" + timenum + "' WHERE contract_process.con_id=(SELECT id FROM contract WHERE name='" + name + "') and contract_process.use_id=(SELECT id FROM user WHERE name='" + userName + "') and contract_process.type=3"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    lock.release()
    return True
