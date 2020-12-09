from cffi.cparser import lock


# 查询客户列表
def database_customerlist(connection, cursor):
    lock.acquire()
    # 执行数据查询
    sql = "select id AS customerId, name AS customerName, address AS customerAddress, tel AS customerTel, " \
          "fax AS customerFax, code AS customerCode, bank AS customerBank, account AS customerAccount from customer "
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result
