import gc
import os
import time
import requests
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from py.xml import html
from selenium.webdriver.support.wait import WebDriverWait
from b_c_components.get_b_version.get_version import auto_get_browser_driver
from b_c_components.get_config.get_config import Setting


def pytest_html_results_table_header_private(cells):
    """
    a
    """
    while cells:
        cells.pop(0)
    cells.insert(0, html.th('通过/失败', class_="sortable result initial-sort", col="result"))
    cells.insert(1, html.th('测试用例', class_="sortable", col="name"))
    cells.insert(2, html.th('用例描述', col="name"))
    cells.insert(3, html.th("执行耗时/S", class_="sortable", col="duration"))
    cells.insert(4, html.th("校验内容", col="name"))
    cells.insert(5, html.link(rel_="stylesheet", href_='http://8.141.50.128:5000/static/report/css/animate.min.css'))
    cells.insert(6,
                 html.link(rel_='stylesheet', href_='http://8.141.50.128:5000/static/report/syalert/syalert.min.css'))
    cells.insert(7, html.script(src_='http://8.141.50.128:5000/static/report/js/jquery.min.js'))
    cells.insert(8, html.script(src_='http://8.141.50.128:5000/static/report/syalert/syalert.min.js'))


def pytest_html_results_table_row_private(report, cells):
    """
    a
    """
    cells.insert(2, html.td(report.description))
    report_name = report.head_line.split('.')[-1]
    str1 = str()
    if pytest.assess_msg.get(report_name) is None:
        str1 = f'html.div("当前用例被手动跳过·没有校验信息"),  '
    elif len(pytest.assess_msg.get(report_name)[::-1]) != 0:
        for i in pytest.assess_msg.get(report_name)[::-1]:
            str1 += f'html.div("{i}"), '
    else:
        str1 = f'html.div("没有校验信息"),  '
    cells.insert(4,
                 html.td(html.div('点击查看详情', onClick_=f"syalert.syopen('{report_name}')", style_='color:blue'),
                         html.div(html.div('校验信息', class_='sy-title'),
                                  html.div(*eval(str1), class_='sy-content'),
                                  html.div(html.button('确定', onClick_=f'ok("{report_name}")'), class_='sy-btn'),
                                  class_='sy-alert sy-alert-alert animated', sy_enter_='zoomIn', sy_leave_='zoomOut',
                                  sy_type_='alert', sy_mask_='true', id_=f'{report_name}'
                                  )
                         )
                 )
    del str1
    cells.pop()


def pytest_runtest_makereport_private(driver, item, outcome):
    """
    Extends the PyTest Plugin to take and embed screenshot in html_str report, whenever test fails.
    :param outcome:
    :param driver:
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":

        if report.outcome == 'failed':
            xfail = hasattr(report, 'wasxfail')
            if (report.skipped and xfail) or (report.failed and not xfail):
                try:
                    if hasattr(driver, 'img_dict'):
                        for def_name in driver.img_dict.keys():
                            if report.head_line[len(report.head_line) - len(def_name):] == def_name:
                                img_list = driver.img_dict.get(def_name)
                                for i in img_list:
                                    html_str = f'<a href = "{i}" target=blank ><img target=_blank src="{i}" alt="screenshot" style="width:304px;height:228px;" οnclick="window.open(this.src)" align="right"/></a>'
                                    extra.append(pytest_html.extras.html(html_str))
                                    report.extra = extra
                            else:
                                continue
                except Exception as e:
                    print(e)
    if report.when == 'call':
        case_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
        # driver.global_cases_instance.update(case_name=case_name)
        if not hasattr(pytest, 'assess_msg'):
            pytest.assess_msg = {}
        pytest.assess_msg[case_name] = []
        a = []
        while driver.global_instance.get('assess_msg'):
            if list(driver.global_instance.get('assess_msg')[0].keys())[0] == report.head_line.split('.')[-1]:
                pytest.assess_msg.get(report.head_line.split('.')[-1]).append(
                    driver.global_instance.get('assess_msg').pop(0).get(report.head_line.split('.')[-1]))
            else:
                a.append(driver.global_instance.get('assess_msg').pop(0))


def pytest_html_report_title_private(report):
    """
    a
    """
    if hasattr(pytest, 'report_title'):
        if hasattr(pytest, 'browser_language'):
            if pytest.browser_language == 'en,en_US':
                # pytest.browser_language = 'en,en_US'
                report.title = "测试报告·英文浏览器环境"
    else:
        report.title = "测试报告·中文浏览器环境"


def web_driver_initialize_private():
    """

    :return:
    """
    config_framework_path = os.environ.get('config_path')
    config = Setting(config_framework_path)
    chrome = config.get_setting('chrome_option', 'chrome')
    chrome_options = Options()
    if chrome == 'M':
        argument_list = [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--ignore-certificate-errors',
            '--window-size=500,900'
        ]
        chrome_options._arguments = argument_list

        simulator_name = config.get_setting('chrome_option', 'simulator_name')
        chrome_options.experimental_options.update(mobileEmulation={'deviceName': simulator_name})

    elif chrome == 'PC':
        argument_list = [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--ignore-certificate-errors',
        ]
        chrome_options._arguments = argument_list

    elif chrome == 'custom':
        chrome_custom_list = eval(config.get_setting('chrome_option', 'chrome_custom_list'))
        chrome_options._arguments = chrome_custom_list
        experimental_options_list = eval(config.get_setting('chrome_option', 'experimental_options'))
        while experimental_options_list:
            chrome_options.experimental_options.update(experimental_options_list.pop(0))
    chrome_options.experimental_options.update(w3c=False)
    caps = {
        'browserName': 'chrome',
        'loggingPrefs': {
            'browser': 'ALL',
            'driver': 'ALL',
            'performance': 'ALL',
        },
        'goog:chromeOptions': {
            'perfLoggingPrefs': {
                'enableNetwork': True,
            },
            'w3c': False,
        },
    }
    browser_language = config.get_setting('chrome_option', 'browser_language')
    if browser_language:
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': browser_language})
        pytest.browser_language = browser_language
    else:
        chrome_options.experimental_options.update(prefs={'intl.accept_languages': 'en,en_US'})
        pytest.browser_language = browser_language

    if hasattr(pytest, 'browser_language'):
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': pytest.browser_language})

    driver = webdriver.Chrome(
        auto_get_browser_driver(config_framework_path),
        desired_capabilities=caps,
        options=chrome_options)
    driver.implicitly_wait(config.get_int('explicit_waiting', 'implicitly_wait'))
    os.environ.setdefault('environment', config.get_setting('environment_data', 'environment'))
    driver.global_instance = {}
    driver.global_instance.update(config=config)
    driver.global_instance.update(assess_msg=[])

    return driver


def cases_setup_private(driver):
    """

    :param driver:
    :return:
    """
    if hasattr(driver, 'global_cases_instance'):
        del driver.global_cases_instance
        gc.collect()
    driver.global_cases_instance = {}
    driver.global_cases_instance.update(network_data=[])
    return driver


def pytest_assume(driver, expected_results, actual_results, msg):
    """
    断言
    :param driver:
    :param expected_results: 预期结果
    :param actual_results: 实际结果
    :param msg
    """
    case_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]

    screenshots = pytest.assume(
        expected_results == actual_results,
        f"预期结果与实际结果不一致：预期结果:{expected_results}   实际结果:{actual_results}")
    results_msg = f" : [不通过]" if not screenshots else ' : [通过]'
    driver.global_instance.get('assess_msg').append(
        {case_name: msg + results_msg})
    return screenshots


def pytest_assume_contain(driver, expected_results, actual_results, msg):
    """
    断言
    :param driver:
    :param expected_results: 预期结果
    :param actual_results: 实际结果
    :param msg
    """
    case_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
    screenshots = pytest.assume(
        expected_results in actual_results,
        f"预期结果与实际结果不一致：预期结果:{expected_results}   实际结果:{actual_results}")
    results_msg = f" : [不通过]" if not screenshots else ' : [通过]'
    driver.global_instance.get('assess_msg').append(
        {case_name: msg + results_msg})
    return screenshots


def set_screenshots(driver):
    """
    调用此方法进行截图
    driver:
    """
    case_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
    if not hasattr(driver, 'img_dict'):
        driver.img_dict = dict()
    if driver.img_dict.get(case_name) is None:
        driver.img_dict[case_name] = list()
    file_name = case_name + '_' + 'No.' + str(int(time.time() * 1000)) + ".png"
    headers = {
        'Cookie': 'put_img_key=test'
    }
    data = {
        'img_base64_data': driver.get_screenshot_as_base64(),
        'img_name': file_name
    }
    r = requests.post('http://8.141.50.128:80/put_img_base64', json=data, headers=headers)
    file_name = 'http://8.141.50.128:80' + r.json().get('url')

    driver.img_dict[case_name].append(file_name)


def explicit_waiting(driver, element_str, wait_time=None, poll_frequency=None):
    """
    :param driver:
    :param element_str:
    :param wait_time: 默认值20，即配置文件不传、调用不传
    :param poll_frequency: 默认值0.5，即配置文件不传、调用不传
    :return:
    """
    if wait_time is None:
        wait_time = driver.global_instance.get('config').get_int('explicit_waiting', 'timeout')
    if poll_frequency is None:
        poll_frequency = driver.global_instance.get('config').get_int('explicit_waiting', 'poll_frequency')
    wait = WebDriverWait(
        driver,
        timeout=20 if wait_time is None else wait_time,
        poll_frequency=0.5 if poll_frequency is None else poll_frequency)
    wait.until(lambda x: x.find_element_by_xpath(element_str))


def isElementExist(driver, element_str):
    """

    :param driver:
    :param element_str:
    :return:
    """

    implicitly_wait_int = Setting(driver.global_instance.get('config_path')).get_int(
        'explicit_waiting',
        'implicitly_wait')
    driver.implicitly_wait(1)
    if len(driver.find_elements_by_xpath(element_str)) != 0:
        driver.implicitly_wait(implicitly_wait_int)
        return True
    else:
        driver.implicitly_wait(implicitly_wait_int)
        return False

