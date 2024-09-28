# ilgili tarihler aşağıda belirtilmiştir.
# Test start date: TestDateConfig.start_date
# Test end date: TestDateConfig.end_date
# Data start date: TestDateConfig.data_start_date
# Data end date: TestDateConfig.data_end_date
# Decision start date: TestDateConfig.decision_start_date
# Decision end date: TestDateConfig.decision_end_date
from datetime import datetime, timedelta
from operator import itemgetter

import config
from databaseScripts.PostgreSQL import postgre_obj
from databaseScripts.classes.Processable.DailyDecisionV4ScoreDB import DailyDecisionV4ScoreDB
from databaseScripts.classes.Processable.FourHoursKlineDB import FourHoursKlineDB
from databaseScripts.classes.Processable.OneDayKlineDB import OneDayKlineDB
from databaseScripts.classes.Processable.OneHoursKlineDB import OneHoursKlineDB
from databaseScripts.classes.Processable.OneMinuteKlineDB import OneMinuteKlineDB
from testScripts import testDateConfig

# Description: Data sets for the test cases.
# 1 - ilgili tarihler arasında günük ve saatlik klineData'ları liste halinde hazırlar.
# 2 - ilgili tarihler arasında kararları liste halinde hazırlar.

start_date = testDateConfig.start_date
end_date = testDateConfig.end_date

#one day kline data
def calculate_start_id_oneDayKline(last_one_day_kline):
    # sonOneDayKline'in tarihini ve id'sini al
    last_one_day_kline_date = last_one_day_kline.opening_timestamp.replace(tzinfo=None)
    last_one_day_kline_id = last_one_day_kline.id
    # start_date'i,last_one_day_kline_date ve last_one_day_kline_id kullanarak start_id'yi hesapla
    if start_date == last_one_day_kline_date:
        start_id = last_one_day_kline_id
    else:
        # start_date'in tarihini ve last_one_day_kline_date'in tarihini datetime objesine çevir
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')

        # start_date_obj ve last_one_day_kline_date_obj arasındaki farkı hesapla
        difference = start_date_obj - last_one_day_kline_date
        # difference'ı gün cinsinden al
        difference_days = difference.days
        # start_id'yi hesapla
        start_id = last_one_day_kline_id + difference_days
    return start_id


def calculate_end_id_oneDayKline(last_one_day_kline):
    # sonOneDayKline'in tarihini ve id'sini al
    last_one_day_kline_date = last_one_day_kline.opening_timestamp.replace(tzinfo=None)
    last_one_day_kline_id = last_one_day_kline.id
    # end_date'i,last_one_day_kline_date ve last_one_day_kline_id kullanarak start_id'yi hesapla
    if end_date == last_one_day_kline_date:
        end_id = last_one_day_kline_id
    else:
        # end_date'in tarihini ve last_one_day_kline_date'in tarihini datetime objesine çevir
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        # end_date_obj ve last_one_day_kline_date_obj arasındaki farkı hesapla
        difference = end_date_obj - last_one_day_kline_date
        # difference'ı gün cinsinden al
        difference_days = difference.days
        # start_id'yi hesapla
        end_id = last_one_day_kline_id + difference_days
    return end_id


def find_OneDayKlineData_start_id():
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneDayKlineDB sınıfını oluştur
    one_day_kline_db = OneDayKlineDB(postgre_obj)

    # Veritabanından last id'yi getir
    last_id = one_day_kline_db.get_last_id()
    last_one_day_kline = one_day_kline_db.get_one_day_kline(last_id)
    start_id = calculate_start_id_oneDayKline(last_one_day_kline)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return start_id


def find_OneDayKlineData_end_id():
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneDayKlineDB sınıfını oluştur
    one_day_kline_db = OneDayKlineDB(postgre_obj)

    # Veritabanından last id'yi getir
    last_id = one_day_kline_db.get_last_id()
    last_one_day_kline = one_day_kline_db.get_one_day_kline(last_id)
    end_id = calculate_end_id_oneDayKline(last_one_day_kline)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return end_id


def find_OneDayKlineData(start_id, end_id):
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneDayKlineDB sınıfını oluştur
    one_day_kline_db = OneDayKlineDB(postgre_obj)

    listOfOneDayKlineDataId = list(range(start_id, end_id + 1))
    one_day_kline_data_list = []
    for id in listOfOneDayKlineDataId:
        one_day_kline = one_day_kline_db.get_one_day_kline(id)
        one_day_kline_data_list.append(one_day_kline)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return one_day_kline_data_list


def one_day_kline_data_list_RemoveFirstItem(one_day_kline_data_list):
    one_day_kline_data_list = one_day_kline_data_list[1:]
    return one_day_kline_data_list


def fetch_one_day_kline_data_list():
    start_id = find_OneDayKlineData_start_id()
    end_id = find_OneDayKlineData_end_id()
    one_day_kline_data_list = find_OneDayKlineData(start_id, end_id)
    one_day_kline_data_list = one_day_kline_data_list_RemoveFirstItem(one_day_kline_data_list)
    return one_day_kline_data_list

# one hour kline data
def calculate_start_id_oneHourKline(last_one_hour_kline):
    # sonOneHourKline'in tarihini ve id'sini al
    last_one_hour_kline_date = last_one_hour_kline.opening_timestamp.replace(tzinfo=None)
    last_one_hour_kline_id = last_one_hour_kline.id
    # start_date'i,last_one_hour_kline_date ve last_one_hour_kline_id kullanarak start_id'yi hesapla
    if start_date == last_one_hour_kline_date:
        start_id = last_one_hour_kline_id
    else:
        # start_date'in tarihini ve last_one_hour_kline_date'in tarihini datetime objesine çevir
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')

        # start_date_obj ve last_one_hour_kline_date_obj arasındaki farkı hesapla
        difference = start_date_obj - last_one_hour_kline_date
        # difference'ı saat cinsinden al
        difference_days = difference.days
        difference_hours = difference_days * 24
        # start_id'yi hesapla
        start_id = last_one_hour_kline_id + difference_hours + 1
    return start_id


def calculate_end_id_oneHourKline(last_one_hour_kline):
    # sonOneHourKline'in tarihini ve id'sini al
    last_one_hour_kline_date = last_one_hour_kline.opening_timestamp.replace(tzinfo=None)
    last_one_hour_kline_id = last_one_hour_kline.id
    # end_date'i,last_one_hour_kline_date ve last_one_hour_kline_id kullanarak start_id'yi hesapla
    if end_date == last_one_hour_kline_date:
        end_id = last_one_hour_kline_id
    else:
        # end_date'in tarihini ve last_one_hour_kline_date'in tarihini datetime objesine çevir
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        # end_date_obj ve last_one_hour_kline_date_obj arasındaki farkı hesapla
        difference = end_date_obj - last_one_hour_kline_date
        # difference'ı gün cinsinden al
        difference_days = difference.days
        difference_hours = difference_days * 24 + 24
        # start_id'yi hesapla
        end_id = last_one_hour_kline_id + difference_hours
    return end_id


def find_OneHourKlineData_start_id():
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneHoursKlineDB sınıfını oluştur
    one_hour_kline_db = OneHoursKlineDB(postgre_obj)

    # Veritabanından last id'yi getir
    last_id = one_hour_kline_db.get_last_id()
    last_one_hour_kline = one_hour_kline_db.get_one_hours_kline(last_id)
    start_id = calculate_start_id_oneHourKline(last_one_hour_kline)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return start_id


def find_OneHourKlineData_end_id():
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneHoursKlineDB sınıfını oluştur
    one_hour_kline_db = OneHoursKlineDB(postgre_obj)

    # Veritabanından last id'yi getir
    last_id = one_hour_kline_db.get_last_id()
    last_one_hour_kline = one_hour_kline_db.get_one_hours_kline(last_id)
    end_id = calculate_end_id_oneHourKline(last_one_hour_kline)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return end_id


def find_OneHourKlineData(start_id, end_id):
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneHoursKlineDB sınıfını oluştur
    one_hour_kline_db = OneHoursKlineDB(postgre_obj)

    listOfOneHourKlineDataId = list(range(start_id, end_id + 1))
    one_hour_kline_data_list = []
    for id in listOfOneHourKlineDataId:
        one_hour_kline = one_hour_kline_db.get_one_hours_kline(id)
        one_hour_kline_data_list.append(one_hour_kline)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return one_hour_kline_data_list


def one_hour_kline_data_list_RemoveFirst24Item(one_hour_kline_data_list):
    one_hour_kline_data_list = one_hour_kline_data_list[24:]
    return one_hour_kline_data_list


def fetch_one_hour_kline_data_list():
    start_id = find_OneHourKlineData_start_id()
    end_id = find_OneHourKlineData_end_id()
    one_hour_kline_data_list = find_OneHourKlineData(start_id, end_id)
    one_hour_kline_data_list = one_hour_kline_data_list_RemoveFirst24Item(one_hour_kline_data_list)
    return one_hour_kline_data_list
# four hour kline data
def find_FourHourKlineData(start_id, end_id):
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneHoursKlineDB sınıfını oluştur
    four_hour_kline_db = FourHoursKlineDB(postgre_obj)

    listOfFourHourKlineDataId = list(range(start_id, end_id + 1))
    four_hour_kline_data_list = []
    for id in listOfFourHourKlineDataId:
        four_hour_kline = four_hour_kline_db.get_four_hours_kline(id)
        four_hour_kline_data_list.append(four_hour_kline)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return four_hour_kline_data_list


def calculate_start_id_fourHourKline(last_four_hour_kline):
    # sonFourHourKline'in tarihini ve id'sini al
    last_four_hour_kline_date = last_four_hour_kline.opening_timestamp.replace(tzinfo=None)
    last_four_hour_kline_id = last_four_hour_kline.id
    # start_date'i,last_four_hour_kline_date ve last_four_hour_kline_id kullanarak start_id'yi hesapla
    if start_date == last_four_hour_kline_date:
        start_id = last_four_hour_kline_id
    else:
        # start_date'in tarihini ve last_four_hour_kline_date'in tarihini datetime objesine çevir
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')

        # start_date_obj ve last_four_hour_kline_date_obj arasındaki farkı hesapla
        difference = start_date_obj - last_four_hour_kline_date
        # difference'ı saat cinsinden al
        difference_days = difference.days + 1
        difference_four_hours = difference_days * 6
        # start_id'yi hesapla
        start_id = last_four_hour_kline_id + difference_four_hours + 1

    return start_id


def find_FourHourKlineData_start_id():
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneHoursKlineDB sınıfını oluştur
    four_hour_kline_db = FourHoursKlineDB(postgre_obj)

    # Veritabanından last id'yi getir
    last_id = four_hour_kline_db.get_last_id()
    last_four_hour_kline = four_hour_kline_db.get_four_hours_kline(last_id)
    start_id = calculate_start_id_fourHourKline(last_four_hour_kline)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return start_id


def calculate_end_id_fourHourKline(last_four_hour_kline):
    # sonOneHourKline'in tarihini ve id'sini al
    last_four_hour_kline_date = last_four_hour_kline.opening_timestamp.replace(tzinfo=None)
    last_four_hour_kline_id = last_four_hour_kline.id
    # end_date'i,last_four_hour_kline_date ve last_four_hour_kline_id kullanarak start_id'yi hesapla
    if end_date == last_four_hour_kline_date:
        end_id = last_four_hour_kline_id
    else:
        # end_date'in tarihini ve last_four_hour_kline_date'in tarihini datetime objesine çevir
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        # end_date_obj ve last_four_hour_kline_date_obj arasındaki farkı hesapla
        difference = end_date_obj - last_four_hour_kline_date
        # difference'ı gün cinsinden al
        difference_days = difference.days
        difference_hours = difference_days * 6
        # start_id'yi hesapla
        end_id = last_four_hour_kline_id + difference_hours + 6
    return end_id


def find_FourHourKlineData_end_id():
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneHoursKlineDB sınıfını oluştur
    four_hour_kline_db = FourHoursKlineDB(postgre_obj)

    # Veritabanından last id'yi getir
    last_id = four_hour_kline_db.get_last_id()
    last_four_hour_kline = four_hour_kline_db.get_four_hours_kline(last_id)
    end_id = calculate_end_id_fourHourKline(last_four_hour_kline)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return end_id


def four_hour_kline_data_list_RemoveFirst1Item(four_hour_kline_data_list):
    four_hour_kline_data_list = four_hour_kline_data_list[1:]
    return four_hour_kline_data_list


def fetch_four_hours_kline_data_list():
    start_id = find_FourHourKlineData_start_id()
    end_id = find_FourHourKlineData_end_id()
    four_hour_kline_data_list = find_FourHourKlineData(start_id, end_id)
    #four_hour_kline_data_list = four_hour_kline_data_list_RemoveFirst1Item(four_hour_kline_data_list)
    return four_hour_kline_data_list
#daily decision data
def calculate_start_id_dailyDecision(last_decision):
    # sonOneHourKline'in tarihini ve id'sini al
    last_decision_date = last_decision.date.replace(tzinfo=None)
    last_decision_id = last_decision.id
    # start_date'i,last_decision_date ve last_decision_id kullanarak start_id'yi hesapla
    if start_date == last_decision_date:
        start_id = last_decision_id
    else:
        # start_date'in tarihini ve last_decision_date'in tarihini datetime objesine çevir
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')

        # start_date_obj ve last_decision_date_obj arasındaki farkı hesapla
        difference = start_date_obj - last_decision_date
        # difference'ı gün cinsinden al
        difference_days = difference.days
        # start_id'yi hesapla
        start_id = last_decision_id + difference_days
    return start_id


def find_dailyDecision_start_id():
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneDayKlineDB sınıfını oluştur
    dailyDecision_db = DailyDecisionV4ScoreDB(postgre_obj)

    # Veritabanından last id'yi getir
    last_id = dailyDecision_db.get_last_id()
    last_decision = dailyDecision_db.get_decision(last_id)
    start_id = calculate_start_id_dailyDecision(last_decision)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return start_id -2


def calculate_end_id_dailyDecision(last_decision):
    # sonOneHourKline'in tarihini ve id'sini al
    last_decision_date = last_decision.date.replace(tzinfo=None)
    last_decision_id = last_decision.id
    # end_date'i,last_decision_date ve last_decision_id kullanarak start_id'yi hesapla
    if end_date == last_decision_date:
        end_id = last_decision_id
    else:
        # end_date'in tarihini ve last_decision_date'in tarihini datetime objesine çevir
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        # end_date_obj ve last_decision_date_obj arasındaki farkı hesapla
        difference = end_date_obj - last_decision_date
        # difference'ı gün cinsinden al
        difference_days = difference.days
        # start_id'yi hesapla
        end_id = last_decision_id + difference_days
    return end_id


def find_dailyDecision_end_id():
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneDayKlineDB sınıfını oluştur
    dailyDecision_db = DailyDecisionV4ScoreDB(postgre_obj)

    # Veritabanından last id'yi getir
    last_id = dailyDecision_db.get_last_id()
    last_decision = dailyDecision_db.get_decision(last_id)
    end_id = calculate_end_id_dailyDecision(last_decision)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return end_id


def find_dailyDecision(start_id, end_id):
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneHoursKlineDB sınıfını oluştur
    dailyDecision_db = DailyDecisionV4ScoreDB(postgre_obj)

    listOfDailyDecisionId = list(range(start_id, end_id + 1))
    dailyDecision_list = []
    for id in listOfDailyDecisionId:
        dailyDecision = dailyDecision_db.get_decision(id)
        dailyDecision_list.append(dailyDecision)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return dailyDecision_list


def dailyDecision_list_RemoveLastItem(dailyDecision_list):
    dailyDecision_list = dailyDecision_list[:-1]
    return dailyDecision_list


def fetch_dailyDecision_list():
    start_id = find_dailyDecision_start_id()
    end_id = find_dailyDecision_end_id()
    dailyDecision_list = find_dailyDecision(start_id, end_id)
    dailyDecision_list = dailyDecision_list_RemoveLastItem(dailyDecision_list)
    #foreach decision in dailyDecision_list
    #remove noneType decisions
    for decision in dailyDecision_list:
        if decision is None:
            dailyDecision_list.remove(decision)
    for decision in dailyDecision_list:
        if decision is None:
            dailyDecision_list.remove(decision)
    for decision in dailyDecision_list:
        if decision is None:
            dailyDecision_list.remove(decision)
    for decision in dailyDecision_list:
        if decision is None:
            dailyDecision_list.remove(decision)
    return dailyDecision_list


def prepare_four_hourly_tuple(hourlyDataList, dailyData, decision):
    # hourKline.openDate,dayKline.openPrice,decision.decision,decision.confidenceRate,hourKline.closePrice
    hourlyTuple = []
    for hourlyDataItem in hourlyDataList:
        hourlyTuple.append((hourlyDataItem.opening_timestamp, dailyData.opening_price, decision.decision,
                            decision.confidenceRate, hourlyDataItem.closing_price, hourlyDataItem.high_price,hourlyDataItem.low_price))
    return hourlyTuple


def removeNoneFromList(list):
    tempList = []
    for item in list:
        if item is not None:
            tempList.append(item)
    return tempList


def calculate_phase(opening_timestamp):
    if not hasattr(opening_timestamp, 'hour'):
        raise ValueError("opening_timestamp parametresi 'hour' (saat) özelliğine sahip olmalıdır.")
    hour = opening_timestamp.hour
    if not 0 <= hour <= 23:
        raise ValueError("Saat değeri 0 ile 23 arasında olmalıdır.")
    phase = (hour // 4) + 1
    return phase


def control_item_count_for_argument_lists(one_minute_kline_data_list, four_hours_decision_list,four_hours_kline_data_list):
    if len(one_minute_kline_data_list) == 0:
        raise ValueError("one_minute_kline_data_list is empty.")
    if len(four_hours_decision_list) == 0:
        raise ValueError("four_hours_decision_list is empty.")
    if len(four_hours_kline_data_list) == 0:
        raise ValueError("four_hours_kline_data_list is empty.")
    if len(four_hours_kline_data_list) != len(four_hours_decision_list):
        raise ValueError("four_hours_kline_data_list and four_hours_decision_list have different item count.")
    if len(one_minute_kline_data_list) / 240 != len(four_hours_kline_data_list):
        raise ValueError("one_minute_kline_data_list and four_hours_kline_data_list have different item count.")
    #write item counts for each list
    print("one_minute_kline_data_list item count: ", len(one_minute_kline_data_list))
    print("four_hours_decision_list item count: ", len(four_hours_decision_list))
    print("four_hours_kline_data_list item count: ", len(four_hours_kline_data_list))



def make_data_tuple_list(one_minute_kline_data_list, four_hours_decision_list, four_hours_kline_data_list):
    start_time = datetime.now()
    print("start_time: ", start_time)
    i = 0
    control_item_count_for_argument_lists(one_minute_kline_data_list, four_hours_decision_list, four_hours_kline_data_list)
    four_hours_tuple_list = []
    for decision in four_hours_decision_list:
        decision_date = decision.date.date()
        decision_phase = decision.phaseIndex
        phase_one_minute_control_data_list = []  # one minute kline data for the phase of decision
        for one_minute_control_data_item in one_minute_kline_data_list:
            one_minute_control_data_item_date = one_minute_control_data_item.opening_timestamp.date()
            one_minute_control_data_item_phase = calculate_phase(one_minute_control_data_item.opening_timestamp)
            if decision_date == one_minute_control_data_item_date:
                if decision_phase == one_minute_control_data_item_phase:
                    phase_one_minute_control_data_list.append(one_minute_control_data_item)
        four_hours_kline_data = None
        for four_hours_kline_data_item in four_hours_kline_data_list:
            four_hours_kline_data_item_date = four_hours_kline_data_item.opening_timestamp.date()
            four_hours_kline_data_item_phase = calculate_phase(four_hours_kline_data_item.opening_timestamp)
            if decision_date == four_hours_kline_data_item_date:
                if decision_phase == four_hours_kline_data_item_phase:
                    four_hours_kline_data = four_hours_kline_data_item  # dailyData for the day of decision
                    break
        if four_hours_kline_data is None:
            raise ValueError("four_hours_kline_data is None.")
        if phase_one_minute_control_data_list is None:
            raise ValueError("phase_one_minute_control_data_list is None.")
        if decision is None:
            raise ValueError("decision is None.")
        tuple_time = datetime.now()
        delta_tuple_time = tuple_time - start_time
        i += 1
        print(str(i) + '. Tuple tourmaline süresi: ', delta_tuple_time)
        hourlyTuple = prepare_four_hourly_tuple(phase_one_minute_control_data_list, four_hours_kline_data, decision)
        four_hours_tuple_list.append(hourlyTuple)
    end_time = datetime.now()
    delta_time = end_time - start_time
    print("Tamamlanma süresi: ", delta_time)
    return four_hours_tuple_list


def arrangeTestTuple(testTuple, confidence_rate):
    arrangedTestTuple = []
    for dailyTuple in testTuple:
        decision_confidence_rate = dailyTuple[4]
        if decision_confidence_rate >= confidence_rate:
            arrangedTestTuple.append(dailyTuple)
    return arrangedTestTuple


def includeConfidenceRate(testTupleList):
    is_confidence_rate_include = config.confidence_rate_include
    if is_confidence_rate_include:
        confidence_rate = config.confidence_rate
        if confidence_rate <= 0 or confidence_rate >= 1:
            raise ValueError("Confidence rate should be between 0 and 1")
        if confidence_rate == 0:
            is_confidence_rate_include = False
            raise ValueError(
                "Confidence = 0 its mean that there is no confidence rate. So, confidence rate is not included in the test data.")
        return arrangeTestTuple(testTupleList, confidence_rate)
    return testTupleList

# one minute kline data
def find_OneMinuteKlineData(start_id, end_id):
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneHoursKlineDB sınıfını oluştur
    one_minute_kline_db = OneMinuteKlineDB(postgre_obj)

    listOfOneMinuteKlineDataId = list(range(start_id, end_id + 1))
    one_minute_kline_data_list = []
    for id in listOfOneMinuteKlineDataId:
        one_minute_kline = one_minute_kline_db.get_one_minute_kline(id)
        one_minute_kline_data_list.append(one_minute_kline)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return one_minute_kline_data_list


def one_minute_kline_data_list_RemoveFirst240Item(one_minute_kline_data_list):
    one_minute_kline_data_list = one_minute_kline_data_list[240:]
    return one_minute_kline_data_list


def calculate_start_id_oneMinuteKline(last_four_hour_kline):
    # sonOneDayKline'in tarihini ve id'sini al
    last_one_minute_kline_date = last_four_hour_kline.opening_timestamp.replace(tzinfo=None)
    last_one_minute_kline_id = last_four_hour_kline.id
    # start_date'i,last_one_minute_kline_date ve last_one_minute_kline_id kullanarak start_id'yi hesapla
    if start_date == last_one_minute_kline_date:
        start_id = last_one_minute_kline_id
    else:
        # start_date'in tarihini ve last_one_minute_kline_date'in tarihini datetime objesine çevir
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')

        # start_date_obj ve last_one_minute_kline_date_obj arasındaki farkı hesapla
        difference = start_date_obj - last_one_minute_kline_date
        # difference'ı gün cinsinden al
        difference_days = difference.days + 1
        difference_one_minute = difference_days * 1440
        # start_id'yi hesapla
        start_id = last_one_minute_kline_id + difference_one_minute + 1
    return start_id


def find_OneMinuteKlineData_start_id():
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneHoursKlineDB sınıfını oluştur
    one_minute_kline_db = OneMinuteKlineDB(postgre_obj)

    # Veritabanından last id'yi getir
    last_id = one_minute_kline_db.get_last_id()
    last_four_hour_kline = one_minute_kline_db.get_one_minute_kline(last_id)
    start_id = calculate_start_id_oneMinuteKline(last_four_hour_kline)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return start_id


def calculate_end_id_oneMinuteKline(last_one_minute_kline):
    # sonOneHourKline'in tarihini ve id'sini al
    last_one_minute_kline_date = last_one_minute_kline.opening_timestamp.replace(tzinfo=None)
    last_one_minute_kline_id = last_one_minute_kline.id
    # end_date'i,last_one_hour_kline_date ve last_one_hour_kline_id kullanarak start_id'yi hesapla
    if end_date == last_one_minute_kline_date:
        end_id = last_one_minute_kline_id
    else:
        # end_date'in tarihini ve last_one_hour_kline_date'in tarihini datetime objesine çevir
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        # end_date_obj ve last_one_hour_kline_date_obj arasındaki farkı hesapla
        difference = end_date_obj - last_one_minute_kline_date
        # difference'ı gün cinsinden al
        difference_days = difference.days
        difference_one_minute = difference_days * 1440
        # start_id'yi hesapla
        end_id = last_one_minute_kline_id + difference_one_minute + 1440
    return end_id


def find_OneMinuteKlineData_end_id():
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneHoursKlineDB sınıfını oluştur
    one_minute_kline_db = OneMinuteKlineDB(postgre_obj)

    # Veritabanından last id'yi getir
    last_id = one_minute_kline_db.get_last_id()
    last_one_hour_kline = one_minute_kline_db.get_one_minute_kline(last_id)
    end_id = calculate_end_id_oneMinuteKline(last_one_hour_kline)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return end_id


def fetch_one_minute_kline_data_list():
    start_id = find_OneMinuteKlineData_start_id()
    end_id = find_OneMinuteKlineData_end_id()
    one_minute_kline_data_list = find_OneMinuteKlineData(start_id, end_id)
    #one_minute_kline_data_list = one_minute_kline_data_list_RemoveFirst240Item(one_minute_kline_data_list)
    return one_minute_kline_data_list

# four hour decision data
def calculate_start_id_four_hour_decision(last_decision):
    # sonOneHourKline'in tarihini ve id'sini al
    last_decision_date = last_decision.date.replace(tzinfo=None)
    last_decision_id = last_decision.id
    # start_date'i,last_decision_date ve last_decision_id kullanarak start_id'yi hesapla
    if start_date == last_decision_date:
        start_id = last_decision_id
    else:
        # start_date'in tarihini ve last_decision_date'in tarihini datetime objesine çevir
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')

        # start_date_obj ve last_decision_date_obj arasındaki farkı hesapla
        difference = start_date_obj - last_decision_date
        # difference'ı gün cinsinden al
        difference_days = difference.days
        difference_four_hours = difference_days * 6
        # start_id'yi hesapla
        start_id = last_decision_id + difference_four_hours + 2
    return start_id


def find_four_hour_decision_start_id():
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneDayKlineDB sınıfını oluştur
    four_hour_decision_db = DailyDecisionV4ScoreDB(postgre_obj)

    # Veritabanından last id'yi getir
    last_id = four_hour_decision_db.get_last_id()
    last_decision = four_hour_decision_db.get_decision(last_id)
    start_id = calculate_start_id_four_hour_decision(last_decision)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return start_id


def calculate_end_id_four_hour_decision(last_decision):
    # sonOneHourKline'in tarihini ve id'sini al
    last_decision_date = last_decision.date.replace(tzinfo=None)
    last_decision_id = last_decision.id
    # end_date'i,last_decision_date ve last_decision_id kullanarak start_id'yi hesapla
    if end_date == last_decision_date:
        end_id = last_decision_id
    else:
        # end_date'in tarihini ve last_decision_date'in tarihini datetime objesine çevir
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')

        # end_date_obj ve last_decision_date_obj arasındaki farkı hesapla
        difference = end_date_obj - last_decision_date
        # difference'ı gün cinsinden al
        difference_days = difference.days
        difference_four_hours = difference_days * 6
        # start_id'yi hesapla
        end_id = last_decision_id + difference_four_hours + 1
    return end_id


def find_four_hour_decision_end_id():
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneDayKlineDB sınıfını oluştur
    foru_hour_decision_db = DailyDecisionV4ScoreDB(postgre_obj)

    # Veritabanından last id'yi getir
    last_id = foru_hour_decision_db.get_last_id()
    last_decision = foru_hour_decision_db.get_decision(last_id)
    end_id = calculate_end_id_four_hour_decision(last_decision)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return end_id


def find_four_hour_decision(start_id, end_id):
    # Veritabanına bağlan
    postgre_obj.connect_db()

    # OneHoursKlineDB sınıfını oluştur
    four_hour_decision_db = DailyDecisionV4ScoreDB(postgre_obj)

    listOfFourHourDecisionId = list(range(start_id, end_id + 1))
    four_hour_decision_list = []
    for id in listOfFourHourDecisionId:
        four_hour_decision = four_hour_decision_db.get_decision(id)
        four_hour_decision_list.append(four_hour_decision)

    # Veritabanı bağlantısını kapat
    postgre_obj.disconnect_db()

    return four_hour_decision_list


def four_hour_decision_list_RemoveLast1Item(four_hour_decision_list):
    four_hour_decision_list = four_hour_decision_list[:-1]
    return four_hour_decision_list


def fetch_four_hour_decision_list():
    start_id = find_four_hour_decision_start_id()
    end_id = find_four_hour_decision_end_id()
    four_hour_decision_list = find_four_hour_decision(start_id, end_id)
    #four_hour_decision_list = four_hour_decision_list_RemoveLast1Item(four_hour_decision_list)
    return four_hour_decision_list

# Description: Test data preparation
def sortDecisionListByPhaseIndex(decision_data_list):
    # 'date' ve ardından 'phaseIndex' ile sıralama yap
    decision_data_list = sorted(decision_data_list, key=lambda obj: (obj.date, obj.phaseIndex))
    return decision_data_list


def generateBasicTestTupleList():
    testTupleList = []
    source_data_list = fetch_four_hours_kline_data_list() # eg. 1 day
    control_data_list = fetch_one_minute_kline_data_list() # eg. 1 hours
    decision_data_list = fetch_four_hour_decision_list()
    source_data_list = removeNoneFromList(source_data_list)
    control_data_list = removeNoneFromList(control_data_list)
    decision_data_list = removeNoneFromList(decision_data_list)
    decision_data_list = sortDecisionListByPhaseIndex(decision_data_list)


    # decision.id, decision.date, dayKline.openPrice, decision.decision, decision.confidenceRate,dayKline.closePrice,HourlyTuple
    data_tuple_list = make_data_tuple_list(control_data_list, decision_data_list, source_data_list)

    for i in range(len(decision_data_list)):
        decision = decision_data_list[i]
        dailyData = source_data_list[i]
        hourlyDataList = data_tuple_list[i]
        testTupleList.append((decision.id, dailyData.opening_timestamp, dailyData.opening_price, decision.decision,
                              decision.confidenceRate, dailyData.closing_price, hourlyDataList))
    return testTupleList


def findFirstBuyOrSell(testTupleList):
    for i in range(len(testTupleList)):
        decision = testTupleList[i][3]
        if decision == "UP" or decision == "DOWN":
            return i
    return -1


def stbDecisionConvertionHourly(testTupleList):
    for dailyTuple in testTupleList:
        dailyDecision = dailyTuple[3]
        hourlyTupleList = dailyTuple[6]
        # assign the daily decision to the hourlyTuple[2] for each hourlyTuple
        for i in range(len(hourlyTupleList)):
            hourlyTuple = hourlyTupleList[i]
            hourlyTupleList[i] = (hourlyTuple[0], hourlyTuple[1], dailyDecision, hourlyTuple[3],hourlyTuple[4])
    return testTupleList


def stbDecisionConversion(testTupleList):
    is_stb_decision_conversion = config.stb_decision_conversion
    if not is_stb_decision_conversion:
        return testTupleList
    indexOfFirstBuyOrSell = findFirstBuyOrSell(testTupleList)
    if indexOfFirstBuyOrSell == -1:
        raise ValueError("There is no buy or sell decision in the test data.")
    # delete the decisions before the first buy or sell decision
    testTupleList = testTupleList[indexOfFirstBuyOrSell:]

    # convert the STB decisions to UP/DOWN decisions
    for i in range(len(testTupleList)):
        decision = testTupleList[i][3]
        if decision == "STB":
            if i == 0:
                raise ValueError("The first decision is STB. It should be UP or DOWN.")
            previousDecision = testTupleList[i - 1][3]
            testTupleList[i] = (
            testTupleList[i][0], testTupleList[i][1], testTupleList[i][2], previousDecision, testTupleList[i][4],
            testTupleList[i][5], testTupleList[i][6])

    testTupleList = stbDecisionConvertionHourly(testTupleList)
    return testTupleList


def getTestTupleList():
    testTupleList = generateBasicTestTupleList()
    #testTupleList = stbDecisionConversion(testTupleList)
    #testTupleList = includeConfidenceRate(testTupleList)
    #return testTupleList


def writeTradeCount(testTupleList):
    # write the trade count to the screen
    tradeCount = 0
    yesterdayDecision = None
    for dailyTuple in testTupleList:
        dailyDecision = dailyTuple[3]
        if yesterdayDecision is not None:
            if yesterdayDecision != dailyDecision:
                tradeCount += 1
        yesterdayDecision = dailyDecision
    print("Trade count: " + str(tradeCount))


def writeTestDayCount(testTupleList):
    # write the test day count to the screen
    print("Test day count: " + str(len(testTupleList)))


def getTestInfo():
    testTupleList = getTestTupleList()
    writeTestDayCount(testTupleList)

