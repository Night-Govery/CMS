# 所有用户的信息， 用于用户列表网页
test_userlist = [{'use_id': 1, 'userName': 'test1', 'roleName': ['管理员','老板']},
                 {'use_id': 2, 'userName': 'test2', 'roleName': ['部门经理']},
                 {'use_id': 3, 'userName': 'test3', 'roleName': ['员工']}]

test_userrole = ['管理员', '用户', '部门经理']

# 当前登录用户的权限列表，用于校验用户权限
test_userpermission = {'起草合同': 1, '会签合同': 1, '定稿合同': 1, '审批合同': 1, '签订合同': 1,
                       '查询合同信息': 1, '查询合同流程': 1, '分配会签': 1, '分配审批': 1, '分配签订': 1,
                       '新增角色': 1, '编辑角色': 1, '查询角色': 1, '删除角色': 1, '新增用户': 1,
                       '编辑用户': 1, '查询用户': 1, '删除用户': 1, '查询日志': 1, '删除日志': 1,
                       '管理合同信息': 1, '新增客户': 1, '编辑客户': 1, '查询客户': 1, '删除客户': 1}

# 所有角色的信息，用于角色列表网页
test_rolelist = [
    {'rol_id': 1, 'roleName': '管理员', 'description': '拥有最高权力，系统维护者',
     '起草合同': 1, '会签合同': 1, '定稿合同': 1, '审批合同': 1, '签订合同': 1,
     '查询合同信息': 1, '查询合同流程': 1, '分配会签': 1, '分配审批': 1, '分配签订': 1,
     '新增角色': 1, '编辑角色': 1, '查询角色': 1, '删除角色': 1, '新增用户': 1,
     '编辑用户': 1, '查询用户': 1, '删除用户': 1, '查询日志': 1, '删除日志': 1,
     '管理合同信息': 1, '新增客户': 1, '编辑客户': 1, '查询客户': 1, '删除客户': 1},

    {'rol_id': 2, 'roleName': '部门经理', 'description': '用户管理部门经理',
     '起草合同': 1, '会签合同': 1, '定稿合同': 1, '审批合同': 1, '签订合同': 1,
     '查询合同信息': 1, '查询合同流程': 1, '分配会签': 1, '分配审批': 1, '分配签订': 1,
     '新增角色': 1, '编辑角色': 1, '查询角色': 1, '删除角色': 1, '新增用户': 1,
     '编辑用户': 1, '查询用户': 1, '删除用户': 1, '查询日志': 1, '删除日志': 1,
     '管理合同信息': 1, '新增客户': 1, '编辑客户': 1, '查询客户': 1, '删除客户': 1},

    {'rol_id': 3, 'roleName': '员工', 'description': '打工人是人上人',
     '起草合同': 1, '会签合同': 1, '定稿合同': 1, '审批合同': 1, '签订合同': 1,
     '查询合同信息': 1, '查询合同流程': 1, '分配会签': 1, '分配审批': 1, '分配签订': 1,
     '新增角色': 1, '编辑角色': 1, '查询角色': 1, '删除角色': 1, '新增用户': 1,
     '编辑用户': 1, '查询用户': 1, '删除用户': 1, '查询日志': 1, '删除日志': 1,
     '管理合同信息': 1, '新增客户': 1, '编辑客户': 1, '查询客户': 1, '删除客户': 1}]


# 所有角色的信息，用于角色列表网页
test_rolelist00000 = [
    {'rol_id': 1, 'roleName': '管理员', 'description': '拥有最高权力，系统维护者',
     '起草合同': 1, '会签合同': 0, '定稿合同': 1, '审批合同': 1, '签订合同': 1,
     '查询合同信息': 1, '查询合同流程': 1, '分配会签': 1, '分配审批': 1, '分配签订': 1,
     '新增角色': 1, '编辑角色': 1, '查询角色': 1, '删除角色': 1, '新增用户': 1,
     '编辑用户': 1, '查询用户': 1, '删除用户': 1, '查询日志': 1, '删除日志': 1,
     '管理合同信息': 1, '新增客户': 1, '编辑客户': 1, '查询客户': 1, '删除客户': 1},

    {'rol_id': 2, 'roleName': '部门经理', 'description': '用户管理部门经理',
     '起草合同': 1, '会签合同': 1, '定稿合同': 1, '审批合同': 1, '签订合同': 1,
     '查询合同信息': 1, '查询合同流程': 1, '分配会签': 1, '分配审批': 1, '分配签订': 1,
     '新增角色': 1, '编辑角色': 1, '查询角色': 1, '删除角色': 1, '新增用户': 1,
     '编辑用户': 1, '查询用户': 1, '删除用户': 0, '查询日志': 1, '删除日志': 1,
     '管理合同信息': 1, '新增客户': 1, '编辑客户': 1, '查询客户': 1, '删除客户': 1},

    {'rol_id': 3, 'roleName': '员工', 'description': '打工人是人上人',
     '起草合同': 1, '会签合同': 1, '定稿合同': 1, '审批合同': 1, '签订合同': 1,
     '查询合同信息': 1, '查询合同流程': 1, '分配会签': 1, '分配审批': 1, '分配签订': 1,
     '新增角色': 1, '编辑角色': 1, '查询角色': 1, '删除角色': 1, '新增用户': 1,
     '编辑用户': 1, '查询用户': 1, '删除用户': 1, '查询日志': 1, '删除日志': 1,
     '管理合同信息': 1, '新增客户': 1, '编辑客户': 1, '查询客户': 1, '删除客户': 1}]
