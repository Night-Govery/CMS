from cffi.cparser import lock


# 查询待审批列表
def database_daishenpi(connection, cursor):
    lock.acquire()
    # 执行数据查询
    sql = "select contract.name AS contractName, contract_state.time AS contractTime from contract,contract_state where " \
          "contract_state.con_id=contract.id and contract_state.type=3 "
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


# 查询已审批列表
def database_yishenpi(connection, cursor):
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
