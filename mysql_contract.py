from cffi.cparser import lock


# 合同信息
def database_getcontractinfo(connection, cursor, name, userName):
    lock.acquire()
    sql = "SELECT contract.id AS contractid, customer.name AS customername, contract.name AS contractName, contract.beginTime AS beginTime, contract.endTime AS endTime, contract.content AS content, contract.use_id AS contractuseid  FROM contract,customer WHERE contract.name='" + name + "' AND contract.cus_id = customer.id"
    cursor.execute(sql)
    result = cursor.fetchone()
    # 提交数据
    connection.commit()
    lock.release()
    return result


# 合同信息
def database_getcontractstate(connection, cursor, name, userName):
    lock.acquire()
    sql = "SELECT contract.id AS contractid, customer.name AS customername, contract.name AS contractName, contract.beginTime AS beginTime, contract.endTime AS endTime, contract.content AS content, contract.use_id AS contractuseid  FROM contract,customer WHERE contract.name='" + name + "' AND contract.cus_id = customer.id"
    cursor.execute(sql)
    result = cursor.fetchone()
    # 提交数据
    connection.commit()
    lock.release()
    return result


# 合同信息
def database_deletecontract(connection, cursor, name, userName):
    lock.acquire()
    #删除合同状态
    sql = "DELETE FROM contract_state WHERE id=(SELECT id FROM contract WHERE name='" + name + "')"
    cursor.execute(sql)
    connection.commit()
    #删除合同流程
    sql = "DELETE FROM contract_process WHERE id=(SELECT id FROM contract WHERE name='" + name + "')"
    cursor.execute(sql)
    connection.commit()
    # 删除合同
    sql = "DELETE FROM contract WHERE id=(SELECT id FROM contract WHERE name='" + name + "')"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    lock.release()
    return 1

