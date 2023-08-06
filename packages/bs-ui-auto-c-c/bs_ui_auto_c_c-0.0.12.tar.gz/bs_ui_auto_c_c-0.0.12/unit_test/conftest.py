
import gc
import os
import sys
import pytest
from py.xml import html

global driver


@pytest.fixture(scope='session')
def web_driver_initialize():
    """ setup any state tied to the execution of the given function.
 Invoked for every test function in the module.
 """
    from b_c_components.pytest_model import web_driver_initialize_private

    global driver
    sys.path.append(os.path.dirname(__file__))
    driver = web_driver_initialize_private(os.path.dirname(__file__) + '/config_framework.ini')
    from .page_object.module_metadata import element_str
    driver.global_instance.update(element_str=element_str())
    return driver


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    """
    a
    """
    from b_c_components.pytest_model import pytest_html_results_table_header_private
    pytest_html_results_table_header_private(cells)


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    """
    a
    """
    from b_c_components.pytest_model import pytest_html_results_table_row_private
    pytest_html_results_table_row_private(report, cells)


@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    """
    a
    """
    if report.passed:
        del data[:]
        data.append(html.div("No log output captured.", class_="empty log"))


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html_str report, whenever test fails.
    :param item:
    """

    outcome = yield
    from b_c_components.pytest_model import pytest_runtest_makereport_private
    pytest_runtest_makereport_private(driver, item, outcome)


@pytest.fixture(scope='session', autouse=True)
def quit_driver(request):
    """

    :return:
    """

    def _quit_driver():
        if hasattr(driver, 'global_instance'):
            del driver.global_instance
            gc.collect()
        driver.quit()

    request.addfinalizer(_quit_driver)


@pytest.fixture(scope='function', autouse=True)
def cases_setup():
    """
    初始化driver用例级别参数
    driver已经初始化变量global_cases_instance
    global_cases_instance 中已初始化变量network_data
    自定义初始化变量写法： driver.global_cases_instance.update(变量名称=值)
                        driver.global_cases_instance.update(test=111)
    """

    from b_c_components.pytest_model import cases_setup_private
    cases_setup_private(driver)
