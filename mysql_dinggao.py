import datetime

from cffi.cparser import lock


# 查询待定稿列表
def database_daidinggao(connection, cursor, userName):
    lock.acquire()
    # 执行数据查询
    sql = "select DISTINCT contract.name AS contractName, contract_state.time AS contractTime from contract,contract_state,user,contract_process" \
          " where contract_state.con_id=contract.id and contract_process.con_id=contract.id and contract_state.type=2 and contract.use_id=(SELECT id FROM user WHERE name ='" + userName + "')"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


# 查询已定稿列表
def database_yidinggao(connection, cursor, userName):
    lock.acquire()
    # 执行数据查询
    sql = "select DISTINCT contract.name AS contractName, contract_state.time AS contractTime from contract,contract_state " \
          "where contract_state.id=contract.id and contract_state.type>=3 and contract.use_id=(SELECT id FROM user " \
          "WHERE name ='" + userName + "') "
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


# 定稿合同
def database_dinggao(connection, cursor, name, userName, dinggao):
    lock.acquire()
    timenum = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    # 执行数据查询,查询是否全部会签
    sql = "SELECT use_id FROM contract_process WHERE contract_process.con_id=(SELECT id FROM contract WHERE name='" + name + "') and contract_process.type=1 and contract_process.state=0"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchone()
    # 存在未会签用户
    if result:
        lock.release()
        return 0
    else:
        # 更新数据
        sql = "UPDATE contract_state SET type='3',time='" + timenum + "' WHERE contract_state.con_id=(SELECT id FROM contract WHERE name='" + name + "') "
        cursor.execute(sql)
        # 提交数据
        connection.commit()
        # 更新数据
        sql = "UPDATE contract SET content='" + dinggao + "' WHERE contract.name='" + name + "' and contract.use_id=(SELECT id FROM user WHERE name='" + userName + "')"
        cursor.execute(sql)
        # 提交数据
        connection.commit()
        # 更新数据con_id,use_id,type,state
        sql = "UPDATE contract_process SET content=NULL,time=NULL,state='0' WHERE contract_process.con_id=(SELECT id FROM " \
              "contract WHERE name='" + name + "') and contract_process.type=2 "
        cursor.execute(sql)
        # 提交数据
        connection.commit()
        lock.release()
        return 1


# 查看所有会签意见
def database_huiqianyijian(connection, cursor, name, userName):
    lock.acquire()
    # 执行数据查询
    sql = "SELECT DISTINCT contract_process.content AS huiqiancontent from contract,contract_process" \
          " where contract_process.con_id=contract.id and contract_process.type=1 and contract.id=(SELECT id FROM contract WHERE name ='" + name + "')"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


# 查看所有审批意见
def database_shenpiyijian(connection, cursor, name, userName):
    lock.acquire()
    # 执行数据查询
    sql = "SELECT DISTINCT contract_process.content AS shenpicontent from contract,contract_process" \
          " where contract_process.con_id=contract.id and contract_process.type=2 and contract.id=(SELECT id FROM contract WHERE name ='" + name + "')"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result