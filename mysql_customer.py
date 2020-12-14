from cffi.cparser import lock


# 查询客户列表
def database_customerlist(connection, cursor, userName):
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


# 新增客户
def database_addcustomer(connection, cursor, customerName, customerAddr, customerTel):
    lock.acquire()
    # 执行数据查询,查询是否重名
    sql = "SELECT id FROM customer WHERE name='" + customerName + "' and tel ='" + customerTel + "'"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchone()
    # 用户名重复
    if result:
        lock.release()
        return 0
    # 添加成功
    else:
        sql = "INSERT INTO customer(name,address,tel)VALUES('" + customerName + "','" + customerAddr + "','" + customerTel + "');"
        cursor.execute(sql)
        connection.commit()
    lock.release()
    return 1
