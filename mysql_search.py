from cffi.cparser import lock


def database_contractinfosearch(connection, cursor, userName):
    lock.acquire()
    sql = "SELECT contract.name AS contractName, customer.name AS customerName, contract.beginTime AS beginTime, contract.endTime AS endTime, contract.content AS content FROM contract,customer WHERE contract.cus_id=customer.id"
    cursor.execute(sql)
    result = cursor.fetchall()
    # 提交数据
    connection.commit()
    lock.release()
    return result


def database_contractprocesssearch(connection, cursor, userName):
    lock.acquire()
    sql = "SELECT contract.name AS contractName, contract_state.type AS contractState FROM contract,contract_state WHERE contract.id=contract_state.con_id"
    cursor.execute(sql)
    result = cursor.fetchall()
    # 提交数据
    connection.commit()
    lock.release()
    return result