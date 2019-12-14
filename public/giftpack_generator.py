#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-12-13 21:09
# @Author  : ziyezhang

# 代码生成器
# 自动生成数据表增删改查python文件
from public.GiftPacks import DB
import time


common_comment = "#!/usr/bin/env python3\n"\
                 "# -*- coding: utf-8 -*-\n"\
                 "# @Time    : %s\n"\
                 "# @Tool    : GiftPack Generator\n"\
                 "# @Author  : ziyezhang\n\n" % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

common_import = "from libs.GiftPacks import DB\n" \
                "from libs.logger import Logger\n\n" \
                "logger = Logger(__name__)"
common_page = " index=1, limit=1000"
bk = "    "


def select_generator(table_name, section):
    method = "\n\n\n"
    db = DB(section)
    result = db.select("desc %s" % table_name)
    db.close()
    col_type = ""
    col = ""
    for tmp in result:
        col += tmp[0] + ","
        if tmp[1].find("int") != -1:
            col_type += tmp[0] + ": int, "
        else:
            col_type += tmp[0] + ": str, "
    method += "def select(%s) -> dict:\n" % (col_type[:-1] + common_page)
    method += bk + 'sql = "select %s from %s where 1=1" \n' % (col[:-1], table_name)
    for tmp in result:
        method += bk + 'if %s:\n' % tmp[0]
        if tmp[1].find("int") != -1:
            method += bk + bk + 'sql += "and %s = %%d " %% int(%s)\n' % (tmp[0], tmp[0])
        else:
            method += bk + bk + 'sql += "and %s = \'%%s\' " %% %s\n' % (tmp[0], tmp[0])
    method += bk + 'db = DB("%s")\n' % (section)
    method += bk + "result = db.select(sql, index, limit)\n"
    method += bk + "db.close()\n"
    method += bk + 'if result and result.get("data"):\n'
    method += bk + bk + 'data = result.get("data")\n'
    method += bk + bk + 'r_data = list()\n'
    method += bk + bk + 'for tmp in data:\n'
    result_dict = ""
    for index, tmp in enumerate(result):
        result_dict += "%s=tmp[%d], " % (tmp[0], index)
    method += bk + bk + bk + 'r_data.append(dict(%s))\n' % result_dict[:-2]
    method += bk + bk + 'return dict(data=r_data, total_count=result.get("total_count"))\n'
    method += bk + 'logger.info("result is None: %s, index:%d, limit:%d" % (sql, index, limit))\n'
    method += bk + 'return None'
    return method


def select_by_pri_generator(table_name, section):
    method = "\n\n\n"
    db = DB(section)
    result = db.select("desc %s" % table_name)
    db.close()
    col = ""
    pri = None
    for tmp in result:
        col += tmp[0] + ","
        if tmp[1].find("int") != -1:
            if tmp[5] == 'auto_increment':
                pri = "%s: int," % tmp[0]
                pri_name = tmp[0]
                pri_type = "%d"
                pri_name_type = "int(%s)" % tmp[0]
        else:
            if tmp[5] == 'auto_increment':
                pri = "%s: str," % tmp[0]
                pri_name = tmp[0]
                pri_type = "'%s'"
                pri_name_type = tmp[0]
    if not pri:
        return ""
    method += "def select_by_primary(%s) -> dict:\n" % (pri + common_page)
    method += bk + 'sql = "select %s from %s where %s=%s" %% %s\n' % (col[:-1], table_name, pri_name, pri_type, pri_name_type)
    method += bk + 'db = DB("%s")\n' % (section)
    method += bk + "result = db.select(sql, index, limit)\n"
    method += bk + "db.close()\n"
    method += bk + 'if result and result.get("data"):\n'
    method += bk + bk + 'data = result.get("data")\n'
    result_dict = ""
    for index, tmp in enumerate(result):
        result_dict += '%s=data[0][%d], ' % (tmp[0], index)
    method += bk + bk + 'return dict(data=dict(%s), total_count=result.get("total_count"))\n' % result_dict[:-2]
    method += bk + 'logger.info("result is None: %s, index:%d, limit:%d" % (sql, index, limit))\n'
    method += bk + "return None"
    return method


def insert_generator(table_name, section):
    method = "\n\n\n"
    db = DB(section)
    result = db.select("desc %s" % table_name)
    db.close()
    col_type = ""
    col = ""
    value = ""
    for tmp in result:
        if tmp[5] == 'auto_increment':
            continue

        if tmp[1].find("int") != -1:
            value += "%d,"
            col_type += tmp[0] + "=0, "
            col += "int(%s), " % tmp[0]
        else:
            col += tmp[0] + ", "
            value += "'%s',"
            col_type += tmp[0] + '="NULL", '

    method += "def insert(%s) -> bool:\n" % (col_type[:-1])
    method += bk + 'sql = "insert into %s(%s) values(%s)" %% (%s)\n' % (table_name, col[:-1], value[:-1], col[:-2])
    method += bk + 'db = DB("%s")\n' % (section)
    method += bk + "result = db.insert(sql)\n"
    method += bk + "db.close()\n"
    method += bk + "return result"
    return method


def insert_list_generator(table_name, section):
    method = "\n\n\n"
    db = DB(section)
    result = db.select("desc %s" % table_name)
    db.close()
    col_value = ""
    col = ""
    value = ""
    for tmp in result:
        if tmp[5] == 'auto_increment':
            continue
        col += tmp[0] + ","
        if tmp[1].find("int") != -1:
            value += "%d,"
            col_value += 'int(value.get("%s")), ' % tmp[0]
        else:
            value += "'%s',"
            col_value += 'value.get("%s"), ' % tmp[0]
    method += "def insert_list(values: list) -> bool:\n"
    method += bk + 'sql = "insert into %s(%s) value"\n' % (table_name, col[:-1])
    method += bk + "for value in values:\n"
    method += bk + bk + 'sql += "(%s)," %% (%s)\n' % (value[:-1], col_value[:-2])
    method += bk + "sql = sql[:-1]\n"
    method += bk + 'db = DB("%s")\n' % (section)
    method += bk + "result = db.insert(sql)\n"
    method += bk + "db.close()\n"
    method += bk + "return result"
    return method


def update_by_pri_generator(table_name, conf, section):
    method = "\n\n\n"
    db = DB(conf, section)
    result = db.select("desc %s" % table_name)
    db.close()
    col = ""
    pri = None
    for tmp in result:
        if tmp[1].find("int") != -1:
            col += tmp[0] + ": int, "
            if tmp[5] == 'auto_increment':
                pri_name = tmp[0]
                pri_type = "%d"
                pri_name_type = "int(%s)" % tmp[0]
        else:
            col += tmp[0] + ": str, "
            if tmp[5] == 'auto_increment':
                pri_name = tmp[0]
                pri_type = "'%s'"
                pri_name_type = tmp[0]
    if not pri:
        return ""
    method += "def update_by_primary(%s) -> bool:\n" % col[:-2]
    method += bk + 'if not %s:\n' % pri_name
    method += bk + bk + 'return False\n'
    method += bk + 'sql = "update %s set " \n' % table_name
    for tmp in result:
        method += bk + 'if %s:\n' % tmp[0]
        if tmp[1].find("int") != -1:
            method += bk + bk + 'sql += "%s = %%d," %% %s\n' % (tmp[0], tmp[0])
        else:
            method += bk + bk + 'sql += "%s = \'%%s\'," %% %s\n' % (tmp[0], tmp[0])
    method += bk + 'sql += "where %s=%s" %% %s\n' % (pri_name, pri_type, pri_name_type)
    method += bk + 'db = DB("%s")\n' % (section)
    method += bk + "result = db.update(sql)\n"
    method += bk + "db.close()\n"
    method += bk + "return result"
    return method


def delete_by_pri_generator(table_name, section):
    method = "\n\n\n"
    db = DB(conf)
    result = db.select("desc %s" % table_name)
    db.close()
    col = ""
    pri = None
    for tmp in result:
        col += tmp[0] + ","
        if tmp[1].find("int") != -1:
            if tmp[5] == 'auto_increment':
                pri = "%s: int," % tmp[0]
                pri_name = tmp[0]
                pri_type = "%d"
                pri_name_type = "int(%s)" % tmp[0]
        else:
            if tmp[5] == 'auto_increment':
                pri = "%s: str," % tmp[0]
                pri_name = tmp[0]
                pri_type = "'%s'"
                pri_name_type = tmp[0]
    if not pri:
        return ""
    method += "def delete_by_primary(%s) -> bool:\n" % pri
    method += bk + 'if not %s:\n' % pri_name
    method += bk + bk + 'return False\n'
    method += bk + 'sql = "delete from %s where %s=%s" %% %s\n' % (table_name, pri_name, pri_type, pri_name_type)
    method += bk + 'db = DB("%s")\n' % (section)
    method += bk + "result = db.delete(sql)\n"
    method += bk + "db.close()\n"
    method += bk + "return result"
    return method


def generate_python_file(path, table_list, section):
    if not path:
        print("生成文件路径为空！")
        return
    if not table_list:
        print("表为空！")
        return
    for table in table_list:
        f = open("%s/%s.py" % (path, table), 'w')
        f.write(common_comment + common_import +
                select_generator(table, section) +
                select_by_pri_generator(table, section) +
                insert_generator(table, section) +
                insert_list_generator(table, section) +
                update_by_pri_generator(table, section) +
                delete_by_pri_generator(table, section))
        f.flush()
        f.close()
        print("%s.py generated success!" % table)


if __name__ == '__main__':
    tables = ['tb_api_record', 'tb_api', 'tb_user', 'tb_box']
    section = "test"
    path = "giftpacks_dao"
    generate_python_file(path, tables, section)

