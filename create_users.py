import json
import os
from exception import RequestException
from rds_helper import RdsHelper
from rds_helper import RdsConnect

def create(environment, region):
  try:
    environment = os.environ['bucket']
    region = os.environ['region']
    rds = RdsHelper(environment, region)
    db_connect = RdsConnect(rds.read_conn_info())
    users = rds.read_user_info()

    for user in users['USERS']:
      user_name = user['username']
      user_password = user['password']
      user_privileges = user['privileges']
      database_name = user['database_name']

      user_exists = "SELECT user FROM mysql.user WHERE user = '" + user_name + "'"
      exists = db_connect.execute_get_query(user_exists)

      if exists:
        drop_user = "DROP USER IF EXISTS'" + user_name + "'"
        db_connect.execute_create_query(drop_user)

      create_db = "CREATE DATABASE IF NOT EXISTS " + database_name
      grant_usage = "CREATE USER '" + user_name + "'@'%' IDENTIFIED BY '" + user_password + "'"
      grant_privileges = "GRANT " + user_privileges + " ON " + database_name + ".* TO '" + user_name + "'@'%' REQUIRE SSL"
      set_pwd = "SET PASSWORD FOR '" + user_name + "'@'%'='" + user_password + "'"

      db_connect.execute_create_query(create_db)
      db_connect.execute_create_query(grant_usage)
      db_connect.execute_create_query(grant_privileges)
      db_connect.execute_create_query(set_pwd)

  except Exception as exception:
    raise Exception(exception)
