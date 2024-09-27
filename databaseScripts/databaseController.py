# This file includes functions to control database
from databaseScripts.PostgreSQL import PostgreSQL
from databaseScripts.classes.Processable.DailyDecisionV4ScoreDB import DailyDecisionV4ScoreDB
from databaseScripts.classes.Processable.FourHoursKlineDB import FourHoursKlineDB
from databaseScripts.classes.Processable.OneDayKlineDB import OneDayKlineDB
from databaseScripts.classes.Processable.OneHoursKlineDB import OneHoursKlineDB
from databaseScripts.classes.Processable.OneMinuteKlineDB import OneMinuteKlineDB


def get_last_id_from_one_day_kline():

    # PostgreSQL sınıfını oluştur
    postgre_obj = PostgreSQL()

    try:

        # Veritabanına bağlan
        postgre_obj.connect_db()

        # OneDayKlineDB sınıfını oluştur
        one_day_kline_db = OneDayKlineDB(postgre_obj)

        # Son ID'yi getir
        last_id = one_day_kline_db.get_last_id()

        return last_id

    finally:

        # Veritabanı bağlantısını kapat
        postgre_obj.disconnect_db()

def get_one_day_kline(id):

    # PostgreSQL sınıfını oluştur
    postgre_obj = PostgreSQL()

    try:

        # Veritabanına bağlan
        postgre_obj.connect_db()

        # OneDayKlineDB sınıfını oluştur
        one_day_kline_db = OneDayKlineDB(postgre_obj)

        # Son ID'yi getir
        one_day_kline = one_day_kline_db.get_one_day_kline(id)

        return one_day_kline

    finally:

        # Veritabanı bağlantısını kapat
        postgre_obj.disconnect_db()


def get_last_id_from_one_hours_kline():
    # PostgreSQL sınıfını oluştur
    postgre_obj = PostgreSQL()

    try:
        # Veritabanına bağlan
        postgre_obj.connect_db()

        # OneHoursKlineDB sınıfını oluştur
        one_hours_kline_db = OneHoursKlineDB(postgre_obj)

        # Son ID'yi getir
        last_id = one_hours_kline_db.get_last_id()

        return last_id

    finally:
        # Veritabanı bağlantısını kapat
        postgre_obj.disconnect_db()

def get_one_hours_kline(id):
    # PostgreSQL sınıfını oluştur
    postgre_obj = PostgreSQL()

    try:
        # Veritabanına bağlan
        postgre_obj.connect_db()

        # OneDayKlineDB sınıfını oluştur
        one_hours_kline_db = OneHoursKlineDB(postgre_obj)

        # Son ID'yi getir
        one_hours_kline = one_hours_kline_db.get_one_hours_kline(id)

        return one_hours_kline

    finally:
        # Veritabanı bağlantısını kapat
        postgre_obj.disconnect_db()



def get_last_id_from_daily_decision():
    postgre_obj = PostgreSQL()
    try:
        postgre_obj.connect_db()
        daily_decision_db = DailyDecisionV4ScoreDB(postgre_obj)
        last_id = daily_decision_db.get_last_id()
        return last_id
    finally:
        postgre_obj.disconnect_db()

def get_daily_decision(id):
    postgre_obj = PostgreSQL()
    try:
        postgre_obj.connect_db()
        daily_decision_db = DailyDecisionV4ScoreDB(postgre_obj)
        daily_decision = daily_decision_db.get_daily_decision(id)
        return daily_decision
    finally:
        postgre_obj.disconnect_db()


def get_last_id_from_four_hours_kline():
    postgre_obj = PostgreSQL()
    try:
        postgre_obj.connect_db()
        four_hours_kline_db = FourHoursKlineDB(postgre_obj)
        last_id = four_hours_kline_db.get_last_id()
        return last_id
    finally:
        postgre_obj.disconnect_db()

def get_four_hours_kline(id):
    postgre_obj = PostgreSQL()
    try:
        postgre_obj.connect_db()
        four_hours_kline_db = FourHoursKlineDB(postgre_obj)
        four_hours_kline = four_hours_kline_db.get_four_hours_kline(id)
        return four_hours_kline
    finally:
        postgre_obj.disconnect_db()


def get_last_id_from_one_minute_kline():
    postgre_obj = PostgreSQL()
    try:
        postgre_obj.connect_db()
        one_minute_kline_db = OneMinuteKlineDB(postgre_obj)
        last_id = one_minute_kline_db.get_last_id()
        return last_id
    finally:
        postgre_obj.disconnect_db()

def get_one_minute_kline(id):
    postgre_obj = PostgreSQL()
    try:
        postgre_obj.connect_db()
        one_minute_kline_db = OneMinuteKlineDB(postgre_obj)
        one_minute_kline = one_minute_kline_db.get_one_minute_kline(id)
        return one_minute_kline
    finally:
        postgre_obj.disconnect_db()