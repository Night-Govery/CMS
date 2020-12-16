from cffi.cparser import lock


# 合同信息
def database_getcontractinfo(connection, cursor, name, userName):
    lock.acquire()
    sql = "SELECT contract.id AS contractid, customer.name AS customername, contract.name AS contractName, contract.beginTime AS beginTime, contract.endTime AS endTime, contract.content AS content, contract.use_id AS contractuseid  FROM contract,customer WHERE contract.name='" + name + "' AND contract.cus_id = customer.id"
    cursor.execute(sql)
    result = cursor.fetchone()
    connection.commit()
    # 查看所有会签意见
    sql = "SELECT DISTINCT contract_process.content AS huiqiancontent from contract,contract_process" \
          " where contract_process.con_id=contract.id and contract_process.type=1 and contract.id=(SELECT id FROM contract WHERE name ='" + name + "')"
    cursor.execute(sql)
    # 获取数据库多条数据
    result1 = cursor.fetchall()
    connection.commit()
    # 查看所有审批意见
    sql = "SELECT DISTINCT contract_process.content AS shenpicontent from contract,contract_process" \
          " where contract_process.con_id=contract.id and contract_process.type=2 and contract.id=(SELECT id FROM contract WHERE name ='" + name + "')"
    cursor.execute(sql)
    # 获取数据库多条数据
    result2 = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


# 合同信息
def database_contractlist(connection, cursor, userName):
    lock.acquire()
    # contractlist = []
    # contractinfo = {'con_id': -1, 'contractName': 'NULL', 'customerName': 'NULL', 'beginTime': 'NULL', 'endTime': 'NULL', 'content': 'NULL', 'contractuseid': 'NULL', 'state': 'NULL'}
    sql = "SELECT contract.id AS contractid, customer.name AS customerName, contract.name AS contractName, contract.beginTime AS beginTime, contract.endTime AS endTime, contract.content AS content, contract.use_id AS contractUserid, contract_state.type AS contractState FROM contract,customer,contract_state WHERE contract.id=contract_state.con_id AND contract.cus_id = customer.id"
    cursor.execute(sql)
    result = cursor.fetchall()
    # 提交数据
    connection.commit()
    lock.release()
    # flag = 0
    # contractlist.append(contractinfo)
    # for a in result:
    #     count = len(contractlist)
    #     for b in contractlist:
    #         if flag == 0:
    #             b['con_id'] = a['con_id']
    #             b['contractName'] = a['contractName']
    #             b['customerName'] = a['customerName']
    #             b['beginTime'] = a['beginTime']
    #             b['endTime'] = a['endTime']
    #             b['content'] = a['content']
    #             b['contractUserid'] = a['contractUserid']
    #             b['contractState'] = a['contractState']
    #             flag = 1
    #             break
    #         else:
    #             count = count - 1
    #     if count == 0:
    #         temp_contractinfo = {'fun_id': a['fun_id'], 'functionsName': a['functionsName'], 'funDescription': a['funDescription']}
    #         contractlist.append(temp_contractinfo)
    return result


# 合同信息
def database_deletecontract(connection, cursor, name, userName):
    lock.acquire()
    #删除合同状态
    sql = "DELETE FROM contract_state WHERE con_id=(SELECT id FROM contract WHERE name='" + name + "')"
    cursor.execute(sql)
    connection.commit()
    #删除合同流程
    sql = "DELETE FROM contract_process WHERE con_id=(SELECT id FROM contract WHERE name='" + name + "')"
    cursor.execute(sql)
    connection.commit()
    # 删除合同
    sql = "DELETE FROM contract WHERE name='" + name + "'"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    lock.release()
    return 1

