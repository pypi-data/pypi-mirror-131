'''
python的数据库模块有统一的接口标准，所以数据库操作都有统一的模式，基本上都是下面几步（假设数据库模块名为db）：

1. 用db.connect创建数据库连接，假设连接对象为conn
2. 如果该数据库操作不需要返回结果，就直接用conn.execute查询，根据数据库事务隔离级别的不同，可能修改数据库需要conn.commit
3. 如果需要返回查询结果则用conn.cursor创建游标对象cur, 通过cur.execute查询数据库，用cur.fetchall/cur.fetchone/cur.fetchmany返回查询结果。根据数据库事 务隔离级别的不同，可能修改数据库需要conn.commit
4. 关闭cur, conn

参考文档：http://anony3721.blog.163.com/blog/static/5119742010716104442536/
         https://www.pythoncentral.io/introduction-to-sqlite-in-python/
'''

import sqlite3

class SQLite3Util:
    def __init__(self):
        pass

    @staticmethod
    def execute_sqlite3(sqllang, dbfile=None, execute_type="execute"):
        """ 在python中，使用sqlite3创建数据库的连接，当我们指定的数据库文件不存在的时候
            连接对象会自动创建数据库文件；如果数据库文件已经存在，则连接对象不会再创建
            数据库文件，而是直接打开该数据库文件。

            如果dbfile为空，那么会使用内存存储

            execute()           --执行一条sql语句

            executemany()       --执行多条sql语句

            参考文档：https://www.pythoncentral.io/introduction-to-sqlite-in-python/


            例子： 创建表
            sqllang = '''CREATE TABLE IF NOT EXISTS gitlab_user
                        (username       TEXT       PRIMARY KEY,
                            name           TEXT       NOT NULL,
                            password       TEXT       NOT NULL,
                            email          TEXT       NOT NULL,
                            createdate     TIMESTAMP  DEFAULT CURRENT_TIMESTAMP NOT NULL);
       """ 
        try:
            # We use the function sqlite3.connect to connect to the database.
            # We can use the argument ":memory:" to create a temporary DB in the RAM or pass the name of a file to open or create it.
            if dbfile is None:
                db = sqlite3.connect(':memory:')
            else:
                db = sqlite3.connect(dbfile)

            with db:
                if execute_type == "executemany":
                    # 如果你需要使用executemany插入多个用户， 那么数据需要为元组和列表：
                    # users = [(name1,phone1, email1, password1),
                    #          (name2,phone2, email2, password2),
                    #          (name3,phone3, email3, password3)]
                    # cursor.executemany('''INSERT INTO users(name, phone, email, password) VALUES(?,?,?,?)''', users)

                    if isinstance(sqllang, list):
                        db.executemany(sqllang)
                    else:
                        print('Error: If you need to insert several users use executemany and a list with the tuples!')
                else:
                    db.execute(sqllang)
        except (sqlite3.IntegrityError, sqlite3.DatabaseError) as sqlite3error:
            print('Error: %s' % (sqlite3error))
        finally:
            db.close()

        ## 方法二：
        # try:
        #     db = sqlite3.connect(dbfile)
        #     cursor = db.cursor()
        #     cursor.execute(sqllang)
        #     db.commit()
        # except (sqlite3.IntegrityError, sqlite3.DatabaseError) as sqlite3error:
        #     db.rollback()
        #     raise sqlite3error
        # finally:
        #     db.close()

    @staticmethod
    def fetch_sqlite3(sqllang, dbfile=None, fetch_type="fetchall"):
        """
            fetchone()          --从结果中取出一条记录

            fetchmany()         --从结果中取出多条记录

            fetchall()          --从结果中取出所有记录
        """
        try:
            if dbfile is None:
                db = sqlite3.connect(':memory:')
            else:
                db = sqlite3.connect(dbfile)

            cursor = db.cursor()
            cursor.execute(sqllang)
            if fetch_type == "fetchone":
                result = cursor.fetchone()
            elif fetch_type == "fetchmany":
                result = cursor.fetchmany()
            else:
                result = cursor.fetchall()
            return result
        except (sqlite3.IntegrityError, sqlite3.DatabaseError,
                sqlite3.OperationalError) as sqlite3error:
            result = None
            raise sqlite3error
        finally:
            db.close()

