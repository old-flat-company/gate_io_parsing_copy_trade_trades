import os
import pathlib
import time
from datetime import datetime
from selenium import webdriver

parse_urls = ['https://www.gate.io/strategybot/detail?id=389182&&type=futures-boll&&name=Oscar-Darcy-Lyla']

check_time = 5  # in min
sleep_time = 10  # in sec

driver_file_name = 'geckodriver_v0.31.0'
curr_dir_path = pathlib.Path(__file__).parent.resolve()
driver_path = os.path.join(curr_dir_path, driver_file_name)

def click_by_element(driver=None, curr_url='', id_name=''):
    while True:
        try:
            driver.get(curr_url)
            elem = driver.find_element("id", id_name)
            elem.click()
            return
        except:
            print('error in click_by_element ')
            print('sleep', 120, 'secs')
            time.sleep(120)
            continue


def parse_first_line_trades_tab(curr_url='', id_name=''):
    driver = None
    while True:
        try:
            if not driver:
                driver = webdriver.Firefox(executable_path=driver_path)
            click_by_element(driver=driver, curr_url=curr_url, id_name=id_name)  # switch to the "Trades" tab
            data_date, data_time, data_side, data_price, data_currency, data_number_contracts, data_contract = driver.find_element_by_class_name(
                'ant-table-row-level-0').text.split()
            driver.close()
            return data_date, data_time, data_side
        except:
            print('error in parse_first_line_trades_tab ')
            print('sleep', 120, 'secs')
            time.sleep(120)
            driver.close()
            driver = None
            continue


def check_time_new_data(data_date='', data_time=''):
    '''
    checking a new data (in the first line of table in "Trades" tab)
    '''
    date_time = '{0} {1}'.format(data_date, data_time)
    new_data_unix_date_time = int(datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").timestamp())
    curr_unix_time = int(time.mktime(datetime.now().timetuple()))
    return True if curr_unix_time - check_time * 60 <= new_data_unix_date_time else False


# try:

while True:
    for curr_url in parse_urls:
        # click_by_element(curr_url=curr_url, id_name='rc-tabs-0-tab-2')  # switch to the "Trades" tab
        data_date, data_time, data_side = parse_first_line_trades_tab(curr_url=curr_url, id_name='rc-tabs-0-tab-2')
        print('True') if check_time_new_data(data_date=data_date, data_time=data_time) else print('False')
        print('sleep', sleep_time, 'secs')
        time.sleep(sleep_time)

# except Exception as e:
#     print(e)
#     driver.close()
