from databaseScripts.classes.klineBased.OneMinuteKline import OneMinuteKline


class OneMinuteKlineBulkDB:
    def __init__(self, postgre_obj):
        self.postgre_obj = postgre_obj
        self.cursor = self.postgre_obj.cursor

    def get_one_minute_kline_bulk(self, id_list):
        # ID listesini tuple formatına dönüştür
        id_tuple = tuple(id_list)

        # Sorguyu hazırlayın
        query = "SELECT * FROM oneminutekline WHERE id IN %s"

        # Sorguyu çalıştırın
        self.cursor.execute(query, (id_tuple,))

        # Sonuçları alın
        results = self.cursor.fetchall()

        # Sonuçları işlemden geçirin
        one_minute_kline_data_list = []
        for row in results:
            one_minute_kline = self._row_to_kline_data(row)
            one_minute_kline_data_list.append(one_minute_kline)

        return one_minute_kline_data_list

    def _row_to_kline_data(self, row):
        # Satırı OneMinuteKline nesnesine dönüştür
        one_minute_kline = OneMinuteKline(row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                          row[8], row[9], row[10], row[11], row[12])
        one_minute_kline.id = row[0]

        return one_minute_kline
