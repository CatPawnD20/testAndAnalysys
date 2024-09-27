from databaseScripts.classes.klineBased.OneMinuteKline import OneMinuteKline
import psycopg2

class OneMinuteKlineDB:
    def __init__(self, postgresql):
        self.postgresql = postgresql

    def get_last_id(self):

        try:

            connection = self.postgresql.connection

            cursor = connection.cursor()

            cursor.execute("SELECT MAX(id) FROM oneminutekline")

            last_id = cursor.fetchone()[0]
            return last_id

        except psycopg2.Error as e:

            print(e)
            print("Son ID çekilirken bir hata oluştu.")
            return None

        finally:

            cursor.close()

    #make a get function with ID parameter
    def get_one_minute_kline(self, id):
        try:
            connection = self.postgresql.connection
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM oneminutekline WHERE id = %s", (id,))
            result = cursor.fetchone()

            if result is None:
                return None

            one_minute_kline = OneMinuteKline(result[1], result[2], result[3], result[4], result[5], result[6], result[7],
                                        result[8], result[9], result[10], result[11], result[12])
            one_minute_kline.id = result[0]

            return one_minute_kline

        except psycopg2.Error as e:
            print(e)
            print("OneMinuteKline çekilirken bir hata oluştu.")
            return None

        finally:
            cursor.close()