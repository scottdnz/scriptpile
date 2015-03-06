#!/usr/bin/env python
# -*- coding: utf-8 -*-


import MySQLdb as mdb
from Crypto.Cipher import AES

#from django.utils.encoding import smart_unicode


def encrypt_val(plain_val, ENCR_KEY, ENCR_IV):
    encoder_1 = AES.new(ENCR_KEY, AES.MODE_CFB, ENCR_IV)
    encrypted = encoder_1.encrypt(plain_val)
    # Encode to hex to avoid annoying utf coding errors
    return encrypted.encode('hex')
    
    
def decrypt_val(encrypted_val, ENCR_KEY, ENCR_IV):
    encoder_1 = AES.new(ENCR_KEY, AES.MODE_CFB, ENCR_IV)
    decrypted = encoder_1.decrypt(encrypted_val.decode('hex'))
    return decrypted


def connect_to_db(username='', password='', database=''):
    res = {'db_conn': '', 'error': ''}
    try:
        res['db_conn'] = mdb.connect('localhost', username, password, database);
    except mdb.Error, e:
        res['error'] = 'Error {}: {}'.format(e.args[0], e.args[1])
    return res
        

def insert_secret_vals(con, label, plain_val, ENCR_KEY, ENCR_IV, logger):
    encrypted_val = encrypt_val(plain_val, ENCR_KEY, ENCR_IV)
    sql = 'insert into secret (label, encrypted_val) values ("{}", "{}");'.format(
    label, encrypted_val)
    
    cur = con.cursor()
    try:
        cur.execute(sql)
        con.commit()
    except Exception as exc:
        #print(sql)
        logger.debug("Error inserting secret val: {}".format(exc))
    return