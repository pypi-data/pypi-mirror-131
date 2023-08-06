
import sys

import pytest

from v5_components.page.modlues import *


# def test_2(web_driver_initialize):
#     """
#     1
#     """
#     web_driver_initialize.def_name = sys._getframe().f_code.co_name
#     environment = web_driver_initialize.global_instance.get('element_str').environment
#     login(environment, 'liyan410071@beisen.com', 'ly123456', web_driver_initialize)
#     go_to_menu(web_driver_initialize, environment, '人才模型')
#     button_xpath = '//*[@id="indexPageViewName"]/div[2]/div/div/div[1]/div[3]/div[1]/div[1]/span'
#     # a = add_or_edit_manipulate_fields(web_driver_initialize, button_xpath)
#     # copy_list_data(web_driver_initialize, 14, '')
#     # delete_list_data(web_driver_initialize, 1, '')
#     # go_to_data_details(web_driver_initialize, environment, '人才模型', 'a3d06f77-3e9b-478c-830d-a53d162217a3')
#     check_list_data(web_driver_initialize)

def test_1(web_driver_initialize):
    """
    dsadas
    :param web_driver_initialize:
    :return:
    """
    web_driver_initialize.get('http://www.baidu.com')
    pytest_assume(web_driver_initialize, 1, 2, '111')
    set_screenshots(web_driver_initialize)


def test_2(web_driver_initialize):
    """
    dsadas
    :param web_driver_initialize:
    :return:
    """
    web_driver_initialize.get('http://www.baidu.com')
    pytest_assume(web_driver_initialize, 1, 2, '111')


def test_3(web_driver_initialize):
    """
    dsadas
    :param web_driver_initialize:
    :return:
    """
    web_driver_initialize.get('http://www.baidu.com')
    pytest_assume(web_driver_initialize, 1, 2, '111')
    set_screenshots(web_driver_initialize)

