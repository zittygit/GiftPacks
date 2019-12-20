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

common_import = "from libs.GiftPacks import DB, TIME\n" \
                "from libs.logger import Logger\n\n" \
                "logger = Logger(__name__)"
common_page = " index=1, limit=1000"
bk = "    "


def select_generator(table_name, conf, section):
    method = "\n\n\n"
    db = DB(conf, section)
    result = db.select("desc %s" % table_name)
    db.close()
    col_type = ""
    col = ""
    for tmp in result:
        col += tmp[0] + ","
        if tmp[1].find("int") != -1:
            col_type += tmp[0] + "=0, "
        elif tmp[1].find("double") != -1:
            col_type += tmp[0] + "=0.0, "
        else:
            col_type += tmp[0] + "=None, "
    method += "def select(%s) -> dict:\n" % (col_type[:-1] + common_page)
    method += bk + 'sql = "select %s from %s where 1=1" \n' % (col[:-1], table_name)
    for tmp in result:
        method += bk + 'if %s:\n' % tmp[0]
        if tmp[1].find("int") != -1:
            method += bk + bk + 'sql += " and %s = %%s" %% %s\n' % (tmp[0], tmp[0])
        else:
            method += bk + bk + 'sql += " and %s = \'%%s\'" %% %s\n' % (tmp[0], tmp[0])
    method += bk + 'db = DB("%s", "%s")\n' % (conf, section)
    method += bk + "result = db.select(sql, index, limit)\n"
    method += bk + "db.close()\n"
    method += bk + 'if result is not None:\n'
    method += bk + bk + 'if type(result) is dict:\n'
    method += bk + bk + bk + 'data = result.get("data")\n'
    method += bk + bk + 'else:\n'
    method += bk + bk + bk + 'data = result\n'
    method += bk + bk + 'r_data = list()\n'
    method += bk + bk + 'for tmp in data:\n'
    result_dict = ""
    for index, tmp in enumerate(result):
        result_dict += "%s=tmp[%d], " % (tmp[0], index)
    method += bk + bk + bk + 'r_data.append(dict(%s))\n' % result_dict[:-2]
    method += bk + bk + 'if type(result) is dict:\n'
    method += bk + bk + bk + 'return dict(data=r_data, total_count=result.get("total_count"))\n'
    method += bk + bk + 'else:\n'
    method += bk + bk + bk + 'return dict(data=r_data)\n'
    method += bk + 'logger.info("result is None: %s, index:%s, limit:%s" % (sql, index, limit))\n'
    method += bk + 'return dict()'
    return method


def select_by_pri_generator(table_name, conf, section):
    method = "\n\n\n"
    db = DB(conf, section)
    result = db.select("desc %s" % table_name)
    db.close()
    col = ""
    pri_name = ""
    pri = ""
    pri_name_type = ""
    for tmp in result:
        col += tmp[0] + ","
        if tmp[1].find("int") != -1:
            if tmp[3] == 'PRI':
                pri += "%s: int, " % tmp[0]
                pri_name += tmp[0]+"=%s and "
                pri_name_type += "%s, " % tmp[0]

        elif tmp[1].find("double") != -1:
            if tmp[3] == 'PRI':
                pri += "%s: double, " % tmp[0]
                pri_name += tmp[0] + "=%s and "
                pri_name_type += "%s, " % tmp[0]
        else:
            if tmp[3] == 'PRI':
                pri += "%s: str, " % tmp[0]
                pri_name += tmp[0]+"='%s' and "
                pri_name_type += "%s, " % tmp[0]
    if not pri:
        return ""
    method += "def select_by_primary(%s) -> dict:\n" % (pri[:-2])
    method += bk + 'sql = "select %s from %s where %s" %% (%s)\n' % (col[:-1], table_name, pri_name[:-5], pri_name_type[:-2])
    method += bk + 'db = DB("%s", "%s")\n' % (conf, section)
    method += bk + "result = db.select(sql)\n"
    method += bk + "db.close()\n"
    method += bk + 'if result:\n'
    result_dict = ""
    for index, tmp in enumerate(result):
        result_dict += '%s=result[0][%d], ' % (tmp[0], index)
    method += bk + bk + 'return dict(%s)\n' % result_dict[:-2]
    method += bk + 'logger.info("result is None: %s" % sql)\n'
    method += bk + "return dict()"
    return method


def insert_generator(table_name, conf, section):
    method = "\n\n\n"
    db = DB(conf, section)
    result = db.select("desc %s" % table_name)
    db.close()
    col_type = ""
    col = ""
    value = ""
    for tmp in result:
        if tmp[5] == 'auto_increment':
            continue

        if tmp[1].find("int") != -1:
            value += "%s,"
            if tmp[4] is not None:
                col_type += tmp[0] + "=%s, " % tmp[4]
            else:
                col_type += tmp[0] + "=0, "
            col += "%s, " % tmp[0]

        elif tmp[1].find("double") != -1:
            value += "%s,"
            if tmp[4] is not None:
                col_type += tmp[0] + "=%s, " % tmp[4]
            else:
                col_type += tmp[0] + "=0.0, "
            col += "%s, " % tmp[0]
        elif tmp[1].find("timestamp") != -1:
            col += tmp[0] + ", "
            value += "'%s',"
            col_type += tmp[0] + '=TIME.now(), '
        else:
            col += tmp[0] + ", "
            value += "'%s',"
            if tmp[4] is not None:
                col_type += tmp[0] + '="%s",' % tmp[4]
            else:
                col_type += tmp[0] + '="NULL", '

    method += "def insert(%s) -> bool:\n" % (col_type[:-2])
    method += bk + 'sql = "insert into %s(%s) values(%s)" %% (%s)\n' % (table_name, col[:-2], value[:-1], col[:-2])
    method += bk + 'db = DB("%s", "%s")\n' % (conf, section)
    method += bk + "result = db.insert(sql)\n"
    method += bk + "db.close()\n"
    method += bk + "return result"
    return method


def insert_list_generator(table_name, conf, section):
    method = "\n\n\n"
    db = DB(conf, section)
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
            value += "%s,"
            col_value += 'value.get("%s",0), ' % tmp[0]

        elif tmp[1].find("double") != -1:
            value += "%s,"
            col_value += 'value.get("%s",0.0), ' % tmp[0]

        elif tmp[1].find("timestamp") != -1:
            value += "'%s',"
            col_value += 'value.get("%s",TIME.now()), ' % tmp[0]

        else:
            value += "'%s',"
            col_value += 'value.get("%s","NULL"), ' % tmp[0]
    method += "def insert_list(values: list) -> bool:\n"
    method += bk + 'if not values:\n'
    method += bk + bk + 'return False\n'
    method += bk + 'sql = "insert into %s(%s) value"\n' % (table_name, col[:-1])
    method += bk + "for value in values:\n"
    method += bk + bk + 'sql += "(%s)," %% (%s)\n' % (value[:-1], col_value[:-2])
    method += bk + "sql = sql[:-1]\n"
    method += bk + 'db = DB("%s", "%s")\n' % (conf, section)
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
    pri_name = ""
    pri = ""
    pri_name_type = ""
    for tmp in result:
        if tmp[1].find("int") != -1:
            if tmp[3] == 'PRI':
                pri += "%s: int, " % tmp[0]
                pri_name += tmp[0] + "=%s and "
                pri_name_type += "%s, " % tmp[0]
                col += tmp[0] + ", "

        elif tmp[1].find("double") != -1:
            if tmp[3] == 'PRI':
                pri += "%s: double, " % tmp[0]
                pri_name += tmp[0] + "=%s and "
                pri_name_type += "%s, " % tmp[0]
                col += tmp[0] + ", "
        else:
            if tmp[3] == 'PRI':
                pri += "%s: str," % tmp[0]
                pri_name += tmp[0] + "='%s' and "
                pri_name_type += "%s, " % tmp[0]
                col += tmp[0] + ", "

    for tmp in result:
        if tmp[1].find("int") != -1:
            if tmp[3] != 'PRI':
                col += tmp[0] + "=0, "
        else:
            if tmp[3] != 'PRI':
                col += tmp[0] + "=None, "
    if not pri:
        return ""
    method += "def update_by_primary(%s) -> bool:\n" % col[:-2]
    for tmp in result:
        if tmp[3] == 'PRI':
            method += bk + 'if not %s:\n' % tmp[0]
            method += bk + bk + 'return False\n'

    method += bk + 'sql = "update %s set " \n' % table_name

    for tmp in result:
        if tmp[3] != 'PRI':
            method += bk + 'if %s:\n' % tmp[0]
            if tmp[1].find("int") != -1 or tmp[1].find("double") != -1:
                method += bk + bk + 'sql += "%s = %%s," %% %s\n' % (tmp[0], tmp[0])
            else:
                method += bk + bk + 'sql += "%s = \'%%s\'," %% %s\n' % (tmp[0], tmp[0])
    method += bk + 'sql = sql[:-1] + " where %s" %% (%s)\n' % (pri_name[:-5], pri_name_type[:-2])
    method += bk + 'db = DB("%s", "%s")\n' % (conf, section)
    method += bk + "result = db.update(sql)\n"
    method += bk + "db.close()\n"
    method += bk + "return result"
    return method


def delete_by_pri_generator(table_name, conf, section):
    method = "\n\n\n"
    db = DB(conf, section)
    result = db.select("desc %s" % table_name)
    db.close()
    col = ""
    pri_name = ""
    pri = ""
    pri_name_type = ""
    for tmp in result:
        col += tmp[0] + ","
        if tmp[1].find("int") != -1:
            if tmp[3] == 'PRI':
                pri += "%s: int, " % tmp[0]
                pri_name += tmp[0] + "=%s and "
                pri_name_type += "%s, " % tmp[0]
        elif tmp[1].find("double") != -1:
            if tmp[3] == 'PRI':
                pri += "%s: double, " % tmp[0]
                pri_name += tmp[0] + "=%s and "
                pri_name_type += "%s, " % tmp[0]
        else:
            if tmp[3] == 'PRI':
                pri += "%s: str, " % tmp[0]
                pri_name += tmp[0] + "='%s' and "
                pri_name_type += "%s, " % tmp[0]
    if not pri:
        return ""
    method += "def delete_by_primary(%s) -> bool:\n" % pri[:-2]

    for tmp in result:
        if tmp[3] == 'PRI':
            method += bk + 'if not %s:\n' % tmp[0]
            method += bk + bk + 'return False\n'

    method += bk + 'sql = "delete from %s where %s" %% (%s)\n' % (table_name, pri_name[:-5], pri_name_type[:-2])
    method += bk + 'db = DB("%s", "%s")\n' % (conf, section)
    method += bk + "result = db.delete(sql)\n"
    method += bk + "db.close()\n"
    method += bk + "return result"
    return method


def generate_python_file(path, table_list, conf, section):
    if not path:
        print("生成文件路径为空！")
        return
    if not table_list:
        print("表为空！")
        return
    if not conf and not section:
        print("mysql 配置为空")
    for table in table_list:
        f = open("%s/%s.py" % (path, table), 'w')
        f.write(common_comment + common_import +
                select_generator(table, conf, section) +
                select_by_pri_generator(table, conf, section) +
                insert_generator(table, conf, section) +
                insert_list_generator(table, conf, section) +
                update_by_pri_generator(table, conf, section) +
                delete_by_pri_generator(table, conf, section))
        f.flush()
        f.close()
        print("%s.py generated success!" % table)


if __name__ == '__main__':
    tables = ['tb_depots', 'tb_vols', 'tb_devices', 'tb_box', 'tb_user', 'tb_api_record']
    conf = "CBS"
    #section = "test"
    section = "CBS_DB"
    path = "modules/CBS/dao"
    generate_python_file(path, tables, conf, section)

