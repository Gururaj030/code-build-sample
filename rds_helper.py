import boto3
import json
import os
import pymysql
import yaml
from exception import RequestException

class RdsHelper:
  def __init__(self, bucket, region):
    self.rds_client = boto3.client('rds', region)
    self.s3_client = boto3.resource('s3')
    self.bucket = self.s3_client.Bucket('%s' %(bucket.replace('_', '-')))

  def read_conn_info(self):
    local = '/tmp/database.yaml'
    self.bucket.download_file('system_data/credentials/database.yaml', local)
    file = open(local)
    read_conn_info = yaml.load(file)
    file.close()
    os.remove(local)
    return read_conn_info

  def read_user_info(self):
    local = '/tmp/database_users.yaml'
    self.bucket.download_file('system_data/users/database_users.yaml', local)
    file = open(local)
    user_info = yaml.load(file)
    file.close()
    os.remove(local)
    return user_info

class RdsConnect:
  def __init__(self, read_conn_info):
    self.db_details = read_conn_info['rds']
    self.user = read_conn_info['rds']['masteruser']
    self.password = read_conn_info['rds']['password']
    self.host = read_conn_info['rds']['host']

  def connect(self):
    arg = self.db_details
    self.conn = pymysql.connect(
      user        = arg['masteruser'],
      password    = arg['password'],
      host        = arg['host']
    )
    self.cur = self.conn.cursor()

  def execute_get_query(self, sql):
    self.connect()
    self.cur.execute(sql)
    result = self.cur.fetchall()
    self.conn.commit()
    self.conn.close()
    return result

  def execute_create_query(self, sql):
    self.connect()
    self.cur.execute(sql)
    self.conn.commit()
    self.conn.close()
    return json.dumps({"status": "Created"})
