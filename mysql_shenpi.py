import datetime

from cffi.cparser import lock


# 查询待审批列表
def database_daishenpi(connection, cursor, userName):
    lock.acquire()
    # 执行数据查询
    sql = "select DISTINCT contract.name AS contractName, contract_state.time AS contractTime from contract,contract_state,contract_process " \
          "where contract_state.con_id=contract.id and contract_process.con_id=contract.id and contract_state.type>=3 and contract_process.use_id=(SELECT id FROM user WHERE name ='" + userName + "') and contract_process.type=2 and contract_process.state=0"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


# 查询已审批列表
def database_yishenpi(connection, cursor, userName):
    lock.acquire()
    # 执行数据查询
    sql = "select DISTINCT contract.name AS contractName, contract_state.time AS contractTime from contract,contract_state,contract_process" \
          " where contract_state.con_id=contract.id and contract_process.con_id=contract.id and contract_state.type>=4 and contract_process.use_id=(SELECT id FROM user WHERE name ='" + userName + "') and contract_process.type=2 and contract_process.state=1" \
          " UNION select DISTINCT contract.name AS contractName, contract_state.time AS contractTime from contract,contract_state,contract_process " \
          " where contract_state.con_id=contract.id and contract_process.con_id=contract.id and contract_state.type>=2 and contract_process.use_id=(SELECT id FROM user WHERE name ='" + userName + "') and contract_process.type=2 and contract_process.state=2"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchall()
    connection.commit()
    lock.release()
    return result


# 审批合同
def database_shenpi(connection, cursor, name, userName, state, yijian):
    lock.acquire()
    # 执行数据查询,查询是否有人否决
    sql = "SELECT use_id FROM contract_process WHERE contract_process.con_id=(SELECT id FROM contract WHERE name='" + name + "') and contract_process.type=2 and contract_process.state=2"
    cursor.execute(sql)
    # 获取数据库单条数据
    result = cursor.fetchone()
    if result:
        lock.release()
        return 0
    else:
        timenum = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        if state == '1':
            # 更新数据
            sql = "UPDATE contract_process SET content='" + yijian + "',state='" + state + "',time='" + timenum + "' WHERE contract_process.con_id=(SELECT id FROM contract WHERE name='" + name + "') and contract_process.use_id=(SELECT id FROM user WHERE name='" + userName + "') and contract_process.type=2"
            cursor.execute(sql)
            # 提交数据
            connection.commit()
            # 执行数据查询,查询是否全部审批
            sql = "SELECT use_id FROM contract_process WHERE contract_process.con_id=(SELECT id FROM contract WHERE name='" + name + "') and contract_process.type=2 and contract_process.state=0"
            cursor.execute(sql)
            # 获取数据库单条数据
            result = cursor.fetchone()
            # 全部会签完毕
            if not result:
                # 更新数据
                sql = "UPDATE contract_state SET type='4', time='" + timenum + "' WHERE contract_state.con_id=(SELECT id FROM contract WHERE name='" + name + "') and contract_state.type=3"
                cursor.execute(sql)
                # 提交数据
                connection.commit()
        elif state == '2':
            # 更新数据
            sql = "UPDATE contract_process SET content='" + yijian + "',state='" + state + "',time='" + timenum + "' WHERE contract_process.con_id=(SELECT id FROM contract WHERE name='" + name + "') and contract_process.use_id=(SELECT id FROM user WHERE name='" + userName + "') and contract_process.type=2"
            cursor.execute(sql)
            # 提交数据
            connection.commit()
            # 更新数据
            sql = "UPDATE contract_state SET type='2',time='" + timenum + "' WHERE contract_state.con_id=(SELECT id FROM contract WHERE name='" + name + "') "
            cursor.execute(sql)
            # 提交数据
            connection.commit()
        # 更新数据con_id,use_id,type,state
        sql = "UPDATE contract_process SET content=NULL,time=NULL,state='0' WHERE contract_process.con_id=(SELECT id FROM " \
              "contract WHERE name='" + name + "') and contract_process.type=3 "
        cursor.execute(sql)
        # 提交数据
        connection.commit()
        lock.release()
        return 1