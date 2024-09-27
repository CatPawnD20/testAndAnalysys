from databaseScripts.classes.klineBased.OneHoursKline import OneHoursKline
import psycopg2

class OneHoursKlineDB:
    def __init__(self, postgresql):
        self.postgresql = postgresql

    def get_last_id(self):
        try:
            connection = self.postgresql.connection
            cursor = connection.cursor()

            cursor.execute("SELECT MAX(id) FROM onehourskline")
            last_id = cursor.fetchone()[0]

            return last_id

        except psycopg2.Error as e:
            print(e)
            print("Son ID çekilirken bir hata oluştu.")
            return None

        finally:
            cursor.close()


    def get_one_hours_kline(self, id):
        try:
            connection = self.postgresql.connection
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM onehourskline WHERE id = %s", (id,))
            result = cursor.fetchone()

            if result is None:
                return None

            one_hours_kline = OneHoursKline(result[1], result[2], result[3], result[4], result[5], result[6],
                                            result[7], result[8], result[9], result[10], result[11], result[12])
            one_hours_kline.id = result[0]

            return one_hours_kline

        except psycopg2.Error as e:
            print(e)
            print("OneHoursKline çekilirken bir hata oluştu.")
            return None

        finally:
            cursor.close()



