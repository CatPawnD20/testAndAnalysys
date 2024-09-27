import psycopg2

class PostgreSQL:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect_db(self):
        try:
            self.connection = psycopg2.connect(
                host="127.0.0.1",
                user="postgres",
                password="112233",
                database="postgres"
            )
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print(e)
            print("Veritabanına bağlanılamadı!!!")

    def disconnect_db(self):
        try:
            if self.connection:
                self.connection.close()
        except psycopg2.Error as e:
            print(e)
            print("Veritabanı bağlantısı kapatılamadı!!!")



# Kullanım örneği
postgre_obj = PostgreSQL()
postgre_obj.connect_db()

# Veritabanı işlemleri burada yapılır

postgre_obj.disconnect_db()
