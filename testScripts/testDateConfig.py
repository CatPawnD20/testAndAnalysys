# Description: This file contains the configuration for the test cases.
from datetime import datetime, timedelta
import config

# Test dates
start_date = config.start_date #test başlangıç tarihi
end_date = config.end_date #test bitiş tarihi

# Data dates
data_start_date = start_date #kullanılacak verinin başlangıç tarihi
data_end_date = end_date #kullanılacak verinin bitiş tarihi


# Decision dates
decision_start_date = start_date #işlenecek kararların başlangıç tarihi
date = datetime.strptime(end_date, '%Y-%m-%d')
decision_end_date = (date - timedelta(days=1)).strftime('%Y-%m-%d')
