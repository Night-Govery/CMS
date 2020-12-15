from cffi.cparser import lock


# 查询角色列表
def database_rolelist(connection, cursor, userName):
    lock.acquire()
    rolelist = []
    roleinfo = {'rol_id': -1, 'roleName': 'NULL', 'description': 'NULL',
                '起草合同': 0, '会签合同': 0, '定稿合同': 0, '审批合同': 0, '签订合同': 0,
                '查询合同信息': 0, '查询合同流程': 0, '分配会签': 0, '分配审批': 0, '分配签订': 0,
                '新增角色': 0, '编辑角色': 0, '查询角色': 0, '删除角色': 0, '新增用户': 0,
                '编辑用户': 0, '查询用户': 0, '删除用户': 0, '查询日志': 0, '删除日志': 0,
                '管理合同信息': 0, '新增客户': 0, '编辑客户': 0, '查询客户': 0, '删除客户': 0}
    # 执行数据查询
    sql = "select role.id AS rol_id ,role.name AS roleName, functions.name AS funcName, role.description from functions,role," \
          "role_functions where functions.id=fun_id and role.id=rol_id "
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    rolelist.append(roleinfo)
    flag = 0
    for a in result:
        # 计算已有的角色数量
        count = len(rolelist)
        # 遍历已有角色
        for b in rolelist:
            # 第一次插入
            if flag == 0:
                b['rol_id'] = a['rol_id']
                b['roleName'] = a['roleName']
                b['description'] = a['description']
                b[a['funcName']] = 1
                flag = 1
                break
            if a['rol_id'] == b['rol_id']:
                b['roleName'] = a['roleName']
                b['description'] = a['description']
                b[a['funcName']] = 1
            else:
                count = count - 1
                # 当前列表没有该id
        if count == 0:
            temp_roleinfo = {'rol_id': a['rol_id'], 'roleName': b['roleName'], 'description': 'NULL', '起草合同': 0,
                             '会签合同': 0, '定稿合同': 0, '审批合同': 0, '签订合同': 0, '查询合同信息': 0, '查询合同流程': 0, '分配会签': 0, '分配审批': 0,
                             '分配签订': 0, '新增角色': 0, '编辑角色': 0, '查询角色': 0, '删除角色': 0, '新增用户': 0, '编辑用户': 0, '查询用户': 0,
                             '删除用户': 0, '查询日志': 0, '删除日志': 0, '管理合同信息': 0, '新增客户': 0, '编辑客户': 0, '查询客户': 0, '删除客户': 0,
                             a['funcName']: 1}
            rolelist.append(temp_roleinfo)
    lock.release()
    return rolelist


# # 更改角色数据
# def database_editrole(connection, cursor, roleName, functionName, description, userName):
#     lock.acquire()
#     # 删除角色数据
#     sql = "DELETE FROM role_functions WHERE role_functions.rol_id=(SELECT id FROM role WHERE name ='" + roleName + "')"
#     cursor.execute(sql)
#     # 插入角色数据
#     sql = "INSERT INTO role_functions (rol_id,fun_id)VALUE((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM function WHERE name ='" + functionName + "'))"
#     cursor.execute(sql)
#     # 提交数据
#     connection.commit()
#     lock.release()
#     return 1
# 更改角色数据
def database_editrole(connection, cursor, roleName, functionName, description, userName):
    lock.acquire()
    # 删除角色数据
    sql = "DELETE FROM role_functions WHERE role_functions.rol_id=(SELECT id FROM role WHERE name ='" + roleName + "')"
    cursor.execute(sql)
    connection.commit()
    sql = "UPDATE role SET description='" + description + "' WHERE name='" + roleName + ""
    cursor.execute(sql)
    connection.commit()
    # 插入角色数据
    if '起草合同' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='起草合同'); "
        cursor.execute(sql)
        connection.commit()
    if '定稿合同' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='定稿合同'); "
        cursor.execute(sql)
        connection.commit()
    if '会签合同' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='会签合同'); "
        cursor.execute(sql)
        connection.commit()
    if '审批合同' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='审批合同'); "
        cursor.execute(sql)
        connection.commit()
    if '签订合同' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='签订合同'); "
        cursor.execute(sql)
        connection.commit()
    if '查询合同信息' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='查询合同信息'); "
        cursor.execute(sql)
        connection.commit()
    if '查询合同流程' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='查询合同流程'); "
        cursor.execute(sql)
        connection.commit()
    if '分配会签' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='分配会签'); "
        cursor.execute(sql)
        connection.commit()
    if '分配审批' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='分配审批'); "
        cursor.execute(sql)
        connection.commit()
    if '分配签订' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='分配签订'); "
        cursor.execute(sql)
        connection.commit()
    if '新增用户' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='新增用户'); "
        cursor.execute(sql)
        connection.commit()
    if '编辑用户' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='编辑用户'); "
        cursor.execute(sql)
        connection.commit()
    if '查询用户' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='查询用户'); "
        cursor.execute(sql)
        connection.commit()
    if '删除用户' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='删除用户'); "
        cursor.execute(sql)
        connection.commit()
    if '新增角色' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='新增角色'); "
        cursor.execute(sql)
        connection.commit()
    if '编辑角色' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='编辑角色'); "
        cursor.execute(sql)
        connection.commit()
    if '查询角色' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='查询角色'); "
        cursor.execute(sql)
        connection.commit()
    if '删除角色' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='删除角色'); "
        cursor.execute(sql)
        connection.commit()
    if '新增客户' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='新增客户'); "
        cursor.execute(sql)
        connection.commit()
    if '编辑客户' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='编辑客户'); "
        cursor.execute(sql)
        connection.commit()
    if '查询客户' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='查询客户'); "
        cursor.execute(sql)
        connection.commit()
    if '删除客户' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='删除客户'); "
        cursor.execute(sql)
        connection.commit()
    if '管理合同信息' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='管理合同信息'); "
        cursor.execute(sql)
        connection.commit()
    if '查询日志' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='查询日志'); "
        cursor.execute(sql)
        connection.commit()
    if '删除日志' in functionName:
        sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='删除日志'); "
        cursor.execute(sql)
        connection.commit()
    lock.release()
    return 1


# 删除角色
def database_deleterole(connection, cursor, roleName, userName):
    lock.acquire()
    # 删除角色及相关内容
    sql = "DELETE FROM role_functions WHERE role_functions.rol_id=(SELECT id FROM role WHERE name ='" + roleName + "')"
    cursor.execute(sql)
    sql = "DELETE FROM rights WHERE rights.rol_id=(SELECT id FROM role WHERE name ='" + roleName + "')"
    cursor.execute(sql)
    sql = "DELETE FROM role WHERE name ='" + roleName + "'"
    cursor.execute(sql)
    # 提交数据
    connection.commit()
    lock.release()
    return 1


# 新增角色数据
def database_addrole(connection, cursor, roleName, functionName, description, userName):
    lock.acquire()
    # 分两步，先查询是否有重名，有返回0，没有就根据传入的权限列表创建新的角色
    # 校验是否有重名角色
    sql = "SELECT id FROM role WHERE name='" + roleName + "'"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchone()
    # 角色名重复
    if result:
        lock.release()
        return 0
    # 无重复
    else:
        sql = "INSERT INTO role (name,description)VALUES('" + roleName + "','" + description + "');"
        cursor.execute(sql)
        # 提交数据
        connection.commit()
        if '起草合同' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='起草合同'); "
            cursor.execute(sql)
            connection.commit()
        if '定稿合同' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='定稿合同'); "
            cursor.execute(sql)
            connection.commit()
        if '会签合同' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='会签合同'); "
            cursor.execute(sql)
            connection.commit()
        if '审批合同' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='审批合同'); "
            cursor.execute(sql)
            connection.commit()
        if '签订合同' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='签订合同'); "
            cursor.execute(sql)
            connection.commit()
        if '查询合同信息' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='查询合同信息'); "
            cursor.execute(sql)
            connection.commit()
        if '查询合同流程' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='查询合同流程'); "
            cursor.execute(sql)
            connection.commit()
        if '分配会签' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='分配会签'); "
            cursor.execute(sql)
            connection.commit()
        if '分配审批' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='分配审批'); "
            cursor.execute(sql)
            connection.commit()
        if '分配签订' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='分配签订'); "
            cursor.execute(sql)
            connection.commit()
        if '新增用户' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='新增用户'); "
            cursor.execute(sql)
            connection.commit()
        if '编辑用户' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='编辑用户'); "
            cursor.execute(sql)
            connection.commit()
        if '查询用户' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='查询用户'); "
            cursor.execute(sql)
            connection.commit()
        if '删除用户' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='删除用户'); "
            cursor.execute(sql)
            connection.commit()
        if '新增角色' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='新增角色'); "
            cursor.execute(sql)
            connection.commit()
        if '编辑角色' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='编辑角色'); "
            cursor.execute(sql)
            connection.commit()
        if '查询角色' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='查询角色'); "
            cursor.execute(sql)
            connection.commit()
        if '删除角色' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='删除角色'); "
            cursor.execute(sql)
            connection.commit()
        if '新增客户' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='新增客户'); "
            cursor.execute(sql)
            connection.commit()
        if '编辑客户' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='编辑客户'); "
            cursor.execute(sql)
            connection.commit()
        if '查询客户' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='查询客户'); "
            cursor.execute(sql)
            connection.commit()
        if '删除客户' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='删除客户'); "
            cursor.execute(sql)
            connection.commit()
        if '管理合同信息' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='管理合同信息'); "
            cursor.execute(sql)
            connection.commit()
        if '查询日志' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='查询日志'); "
            cursor.execute(sql)
            connection.commit()
        if '删除日志' in functionName:
            sql = "INSERT INTO role_functions(rol_id,fun_id)VALUES((SELECT id FROM role WHERE name ='" + roleName + "'),(SELECT id FROM functions WHERE name ='删除日志'); "
            cursor.execute(sql)
            connection.commit()
    lock.release()
    return 1


# 查看权限列表
def database_getpermissionlist(connection, cursor, userName):
    lock.acquire()
    permissionlist = []
    permissioninfo = {'fun_id': -1, 'functionsName': 'NULL', 'roleName': 'NULL'}
    # 执行数据查询
    sql = "select functions.id AS fun_id,functions.name AS functionsName,functions.description AS funDescription from functions"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    flag = 0
    permissionlist.append(permissioninfo)
    for a in result:
        count = len(permissionlist)
        for b in permissionlist:
            if flag == 0:
                b['fun_id'] = a['fun_id']
                b['functionsName'] = a['functionsName']
                b['funDescription'].a['funDescription']
                flag = 1
                break
            if a['fun_id'] == b['fun_id']:
                b['functionsName'] = a['functionsName']
                b['funDescription'].a['funDescription']
            else:
                count = count - 1
        if count == 0:
            temp_userinfo = {'fun_id': a['fun_id'], 'functionsName': a['functionsName'],
                             'funDescription': a['funDescription']}
            permissionlist.append(temp_userinfo)
    return permissionlist
