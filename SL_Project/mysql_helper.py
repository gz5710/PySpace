import pymysql.cursors

class MysqlHelper(object):
    server = 'localhost'
    port = 3306
    user = 'root'
    pwd = ''
    db = 'test'
    charset = 'utf8mb4'
    cursorcls = pymysql.cursors.DictCursor

    @classmethod
    def InsertDictAnnonces(cls, annonces):
        connection = pymysql.connect(host= cls.server,
                             port = cls.port,
                             user= cls.user,
                             password= cls.pwd,
                             db= cls.db,
                             charset= cls.charset,
                             cursorclass= cls.cursorcls)

        # Construct a sql command by dict
        total_sql = ''
        for anno in annonces.values():
            fields = ','.join(anno.keys())
            values = ','.join(map(lambda x: type(x).__name__ == 'str' and f"'{x}'" or str(x), anno.values()))
            sql = f"INSERT INTO `Annonce` ({fields}) VALUES ({values});"
            total_sql += f"{sql}"
        
        try:
            with connection.cursor() as cursor:
                # Create a new record
                cursor.execute(total_sql)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

            # with connection.cursor() as cursor:
            #     # Read a single record
            #     sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            #     cursor.execute(sql, ('webmaster@python.org',))
            #     result = cursor.fetchone()
            #     print(result)
        finally:
            connection.close()


