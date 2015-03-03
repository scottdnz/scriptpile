#!/usr/bin/env python
# -*- coding: utf-8 -*-


import MySQLdb as mdb
from Crypto.Cipher import AES


def encrypt_val(plain_val, ENCR_KEY, ENCR_IV):
    encoder_1 = AES.new(ENCR_KEY, AES.MODE_CFB, ENCR_IV)
    encrypted = encoder_1.encrypt(plain_val)
    return encrypted


def connect_to_db(username='', password='', database=''):
    res = {'db_conn': '', 'error': ''}
    #try:
    res['db_conn'] = mdb.connect('localhost', username, password, database);
    #except mdb.Error, e:
    #     res['error'] = 'Error {}: {}'.format(e.args[0], e.args[1])
    return res
        

def insert_vals(con, label, plain_val, ENCR_KEY, ENCR_IV):
    encrypted_val = encrypt_val(plain_val, ENCR_KEY, ENCR_IV)
    sql = 'insert into secret (label, encrypted_val) values ("{}", "{}");'.format(
    label, encrypted_val)
    #print(sql)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    return