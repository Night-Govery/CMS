from cffi.cparser import lock


# 合同信息
def database_getcontractinfo(connection, cursor, name, userName):
    lock.acquire()
    sql = "SELECT contract.id AS contractid, customer.name AS contractcusname, contract.name AS contractName, contract.beginTime AS beginTime, contract.endTime AS endTime, contract.content AS content, contract.use_id AS contractuseid  FROM contract,customer WHERE contract.name='" + name + "' AND contract.cus_id = customer.id"
    cursor.execute(sql)
    result = cursor.fetchone()
    # 提交数据
    connection.commit()
    lock.release()
    return result
