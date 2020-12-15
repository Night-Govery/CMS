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
def database_addcustomer(connection, cursor, customerName, customerAddress, customerTel, customerFax, customerCose, customerBank, customerAccount, userName):
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
        sql = "INSERT INTO customer(name,address,tel,fax,code,bank,account)VALUES('" + customerName + "','" + customerAddress + "','" + customerTel + "','" + customerFax + "','" + customerCose + "','" + customerBank + "','" + customerAccount + "');"
        cursor.execute(sql)
        connection.commit()
    lock.release()
    return 1


def database_deletecustomer(connection, cursor, customerName, userName):
    lock.acquire()
    # 查询是否有合同
    sql = "SELECT id FROM contract WHERE cus_id=(SELECT id from customer WHERE name='" + customerName + "')"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchone()
    if result:
        lock.release()
        return 0
    else:
        # 删除客户
        sql = "DELETE FROM customer WHERE name='" + customerName + "'"
        cursor.execute(sql)
        # 提交数据
        connection.commit()
    lock.release()
    return 1


def database_editcustomer(connection, cursor, customerName, address, phone, fax, code, bankname, bankaccount, userName):
    lock.acquire()
    #修改信息
    sql = "SELECT id FROM customer WHERE name ='" + customerName + "'"
    cursor.execute(sql)
    connection.commit()
    result =  cursor.fetchone()
    sql = "UPDATE customer SET name='" + customerName + "',address='" + address + "',tel='" + phone + "',fax='" + fax + "',code='" + code + "',bank='" + bankname + "',account='" + bankaccount + "' WHERE id='" + str(result['id']) + "'"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    lock.release()
    return None



# 查询单个客户
def database_customerinfo(connection, cursor, customerName, userName):
    lock.acquire()
    # 执行数据查询
    sql = "select id AS customerId, name AS customerName, address AS customerAddress, tel AS customerTel, " \
          "fax AS customerFax, code AS customerCode, bank AS customerBank, account AS customerAccount from customer where name = '" + customerName + "'"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchone()
    connection.commit()
    lock.release()
    return result