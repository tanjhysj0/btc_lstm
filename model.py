# -*- coding:utf-8 -*-
import pymysql
import sys
from pymysql import IntegrityError
from imp import reload
from DBUtils.PooledDB import PooledDB
reload(sys)
lit = 0 #查询条数


HOST = "192.168.10.126"
USER = "root"
PASS = "root"
NAME= "fast"

pool = PooledDB(pymysql, 5, host=HOST, user=USER, passwd=PASS, db=NAME, port=3306)


def insert(table,data):

    db = pool.connection()
    cursor = db.cursor()
    sql = "insert into "+table+"("
    for key in data:
        sql += "`"+key+"`,"
    sql = sql.strip(",")
    sql += ") value("

    for key,value,in data.items():

        sql += "'"+str(value)+"',"
    sql = sql.strip(",")
    sql += ")"
    # try:
    line =  cursor.execute(sql)

    db.commit()
    db.close()
    return cursor.lastrowid
    return line

def select(table,where="",limit="",field="*",order="id asc"):
    global lit
    db = pool.connection()
    cursor = db.cursor()
    sql = "select "+str(field)+" from "+table

    if len(where) != 0:
        sql += " where "
        for key,value,in where.items():
            #如果是列表类形
            if isinstance(value,list):
                if value[0] == "gt":
                    sql +=str(key)+" > "+str(value[1]) + " and "
                elif value[0] =="lt":
                    sql +=str(key)+" < "+str(value[1])+ " and "
            else:
                sql += str(key) + "='"+str(value)+"' and "


    sql = sql.strip(" and ")
    sql = sql+" order by "+str(order)
    if limit != "":
        sql = sql+" limit "+str(limit)

    # try:
    print(sql)
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    db.close()

    return result

def find(table,where,order="id asc"):
    db = pool.connection()
    cursor = db.cursor()
    sql = "select * from "+table+" where "

    for key,value,in where.items():

        #如果是列表类形
        if isinstance(value,list):
            if value[0] == "gt":
                sql +=str(key)+" > "+str(value[1]) + " and "
            elif value[0] =="lt":
                sql +=str(key)+" < "+str(value[1])+ " and "
        else:
            sql += '`'+str(key)+'`' + "='"+str(value)+"' and "


    sql = sql.strip(" and ")

    sql += " order by " + order
    # try:

    cursor.execute(sql)
    db.commit()
    result = cursor.fetchone()
    db.close()
    return result


def update(table,where,data):
    db = pool.connection()
    cursor = db.cursor()

    sql = "update " + table + " set "

    for key in data:

        sql += str(key) + "="+str(data[key])+","

    sql = sql.strip(",")
    sql = sql + " where "

    for key, value, in where.items():
        sql += str(key) + "='"+str(value)+"' and "
    sql = sql.strip(" and ")

    line = cursor.execute(sql)
    db.commit()
    db.close()
    return line

def query(sql):
    db = pool.connection()
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    result = cursor.fetchall()
    db.close()
    return result