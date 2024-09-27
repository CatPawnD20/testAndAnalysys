import psycopg2

import config
from databaseScripts.classes.decisionBased.DailyDecisionV4Score import DailyDecisionV4Score


class DailyDecisionV4ScoreDB:
    def __init__(self,postgresql):
        self.postgresql = postgresql

    def get_last_id(self):
        try:
            connection = self.postgresql.connection
            cursor = connection.cursor()

            cursor.execute("SELECT MAX(id) FROM "+config.decisionType)
            last_id = cursor.fetchone()[0]

            return last_id

        except psycopg2.Error as e:
            print(e)
            print("Son ID çekilirken bir hata oluştu.")
            return None

        finally:
            cursor.close()

    def get_decision(self, id):
        try:
            connection = self.postgresql.connection
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM "+config.decisionType+" WHERE id = %s", (id,))
            result = cursor.fetchone()

            if result is None:
                return None
            daily_decision = DailyDecisionV4Score(result[1], result[2], result[3], result[4])
            daily_decision.id = result[0]

            return daily_decision

        except psycopg2.Error as e:
            print(e)
            print(config.decisionType+ "tablosundan çekilirken bir hata oluştu.")
            return None

        finally:
            cursor.close()