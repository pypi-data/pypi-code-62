

class wrapsql():
  def connect(data, DBConfigName):
    import pymysql
    conn = pymysql.connect(
      host=data[DBConfigName]['host'],
      database=data[DBConfigName]['database'],
      user=data[DBConfigName]['user'],
      password=data[DBConfigName]['password'])
    return conn

  def get_data(con,TableName,Condition = '1'):
    import pandas as pd
    Condition = "where "+Condition
    query = "select * from "+TableName+" "+Condition
    df = pd.read_sql(query,con)
    return df
  
