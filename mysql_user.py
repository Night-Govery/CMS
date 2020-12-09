from cffi.cparser import lock


# 查询用户的角色
def database_getuserrole(connection, cursor, username):
    userrole_list = []
    lock.acquire()
    # 执行数据查询
    sql = "select role.name AS roleName from user,role,rights where rights.rol_id=role.id and rights.use_id=user.id " \
          "and user.name='" + username + "'"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    for a in result:
        userrole_list.append(a['roleName'])
    return userrole_list


# 查询用户的权限
def database_getuserpermission(connection, cursor, username):
    lock.acquire()
    # 初始化权限列表
    userpermission = {'起草合同': 0, '会签合同': 0, '定稿合同': 0, '审批合同': 0, '签订合同': 0,
                      '查询合同信息': 0, '查询合同流程': 0, '分配会签': 0, '分配审批': 0, '分配签订': 0,
                      '新增角色': 0, '编辑角色': 0, '查询角色': 0, '删除角色': 0, '新增用户': 0,
                      '编辑用户': 0, '查询用户': 0, '删除用户': 0, '查询日志': 0, '删除日志': 0,
                      '管理合同信息': 0, '新增客户': 0, '编辑客户': 0, '查询客户': 0, '删除客户': 0}
    # 获取用户的角色列表
    # 执行数据查询
    sql = "select role.name AS roleName from user,role,rights where rights.rol_id=role.id and rights.use_id=user.id " \
          "and user.name='" + username + "'"
    cursor.execute(sql)
    # 获取数据库单条数据
    result_role = cursor.fetchall()
    connection.commit()
    # 遍历该用户所有的角色
    for role in result_role:
        sql = "select functions.name AS functionsName from functions,role,role_functions where " \
              "role_functions.rol_id=role.id and role_functions.fun_id=functions.id and role.name='" + role[
                  'roleName'] + "'"
        cursor.execute(sql)
        # 获取该角色的所有权限
        result = cursor.fetchall()
        for permission in result:
            userpermission[permission['functionsName']] = 1
    connection.commit()
    lock.release()
    return userpermission
