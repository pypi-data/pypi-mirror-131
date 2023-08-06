import json
import os
import time
import requests
from b_c_components.Intercept_requests.selenium_network import info
from b_c_components.custom_module.custom_exception import Configuration_file_error
from b_c_components.get_environment import get_environment_data
from b_c_components.pytest_model import pytest_assume, set_screenshots


def login(username, password, driver):
    """
    登陆，返回cookie
    """
    session = requests.session()
    login_data = {
        "UserName": f"{username}",
        "Password": f"{password}",
        "LoginType": "0",
        "Remember": "true",
        "IsShowValCode": "false",
        "ValCodeKey": ""}
    try:
        italent_url = get_environment_data(os.environ.get('environment')).get('italent_url')
        r = session.post(
            url=italent_url + '/Account/Account/LogInITalent',
            data=login_data)
        if r.status_code == 200:
            if json.loads(r.text).get('Code') == 1:
                driver.get(italent_url)
                driver.add_cookie(
                    {'name': 'Tita_PC', 'value': r.cookies.get('Tita_PC')})
                driver.get(italent_url)
            else:
                raise
        else:
            raise
    except Exception as e:
        raise e


def login_interface(username, password):
    """

    :param username:
    :param password:
    """

    session = requests.session()
    login_data = {
        "UserName": f"{username}",
        "Password": f"{password}",
        "LoginType": "0",
        "Remember": "true",
        "IsShowValCode": "false",
        "ValCodeKey": ""}
    italent_url = get_environment_data(os.environ.get('environment')).get('italent_url')
    r = session.post(url=italent_url + '/Account/Account/LogInITalent', data=login_data)
    if r.status_code == 200:
        return session
    else:
        return Configuration_file_error(msg=r.text)


def unfinished_transactions(driver, transaction_type, transaction_name):
    """
    cloud待办的处理
    transaction_type 待办所属产品
    transaction_name 以绩效为例，transaction_name代表活动
    """
    cookie = ''
    cookie_list = driver.get_cookies()
    driver.global_cases_instance.update(BSGlobal={})
    time.sleep(0.5)
    driver.global_cases_instance.get('BSGlobal').update(
        tenantInfo=driver.execute_script('return BSGlobal.tenantInfo'))
    driver.global_cases_instance.get('BSGlobal').update(
        userInfo=driver.execute_script('return BSGlobal.userInfo'))
    ssn_Tita_PC = ''
    for i in cookie_list:
        if i.get('name') == 'Tita_PC':
            cookie = f'{i.get("name")}={i.get("value")}' + \
                     f'; {"ssn_Tita_PC"}={i.get("value")}'
            ssn_Tita_PC = i.get("value")
            break
    headers = {
        'Cookie': cookie
    }
    tenantId = str(driver.global_cases_instance.get(
        'BSGlobal').get('tenantInfo').get('Id'))
    userId = str(driver.global_cases_instance.get(
        'BSGlobal').get('userInfo').get('userId'))

    session = requests.session()
    italent_url = get_environment_data(os.environ.get('environment')).get('italent_url')
    url = f'{italent_url}/api/v3/{tenantId}/{userId}/todo/Get?app_id=-1&deadline=&blackTodoIds=&page_size=10&status=1&__t={round(time.time() * 1000)}'
    all_transactions = json.loads(
        session.get(
            url=url,
            headers=headers).text).get('data').get('todos')
    cloud_url = get_environment_data(os.environ.get('environment')).get('cloud_url').split('://')[1]
    driver.add_cookie(
        {'domain': cloud_url, 'name': 'ssn_Tita_PC', 'value': ssn_Tita_PC})
    for i in all_transactions:
        if transaction_type == i.get('appName'):
            if transaction_name != "" and transaction_name in i.get('content'):
                driver.get(url='https:' + i.get('objUrl'))
                break


def go_to_menu(driver, environment, menu_name):
    """
    进入菜单
    menu_name: 菜单名称，默认菜单传应用名称，非默认菜单传应用名称_菜单名称
    """
    driver.add_cookie({'domain': 'cloud.italent.cn',
                       'name': 'ssn_Tita_PC',
                       'value': driver.get_cookie('Tita_PC').get('value')})
    driver.add_cookie({'domain': 'cloud.italent.cn',
                       'name': 'Tita_PC',
                       'value': driver.get_cookie('Tita_PC').get('value')})
    menu_mapping = requests.get('http://8.141.50.128:80/static/json_data/menu_mapping.json').json()
    host_url = get_environment_data(os.environ.get('environment')).get('cloud_url')
    driver.get(host_url + menu_mapping.get(menu_name))


def get_form_view(driver):
    """
    获取表单信息
    """
    fields_to_operate_on_list = []
    network_data = info(driver)
    network_data.reverse()
    datasource_data = []
    for data in network_data:
        url = data.get('request').get('url')
        if '/api/v2/data/datasource' in url:
            # 获取字段对应数据源
            datasource_data = json.loads(data.get('response_data').get('body'))
            break
    for data in network_data:
        # 解析formView接口，获取所有表单字段
        url = data.get('request').get('url')
        if '/api/v2/UI/FormView' in url:
            # 在这里获取所有需要操作的字段
            for sub in json.loads(
                    data.get('response_data').get('body')).get('sub_cmps'):
                for field in sub.get('sub_cmps'):
                    if field.get('cmp_data').get('showdisplaystate') == 'readonly' and field.get(
                            'cmp_data').get('required') is True:
                        dict_data = {}
                        for data_source in datasource_data:
                            if field.get('cmp_data').get(
                                    'datasourcename') == data_source.get('key'):
                                dict_data['dataSourceResults'] = data_source.get(
                                    'dataSourceResults')
                                break
                        dict_data.update({
                            'cmp_id': field.get('cmp_id'),
                            'cmp_label': field.get('cmp_label'),
                            'cmp_name': field.get('cmp_name'),
                            'cmp_type': field.get('cmp_type'),
                            'cmp_data': field.get('cmp_data')
                        })
                        fields_to_operate_on_list.append(dict_data)
    return fields_to_operate_on_list


def option_form(driver, fields_to_operate_on_list, **kwargs):
    """
    操作表单
    """
    if kwargs.keys() is not None:
        pass

    for field in fields_to_operate_on_list:
        """
        表单填充
        """
        if field.get('cmp_type') == 'BC_TextBox':
            driver.find_element_by_xpath(
                f"""//*[@class="bc-form-item clearfix bc-form-item-middle"]/div[{str(
                    fields_to_operate_on_list.index(field) + 1)}]/div[2]/input""").clear()
            driver.find_element_by_xpath(
                f"""//*[@class="bc-form-item clearfix bc-form-item-middle"]/div[{str(
                    fields_to_operate_on_list.index(field) + 1)}]/div[2]/input""").send_keys(
                '自动化人才模型数据' + str(int(time.time())))


def add_or_edit_manipulate_fields(driver, button_xpath):
    """
    视图新增按钮
    """
    time.sleep(1)
    # button_xpath = '//*[@id="indexPageViewName"]/div[2]/div/div/div[1]/div[3]/div[1]/div[1]/span'
    driver.find_element_by_xpath(button_xpath).click()
    driver.switch_to_frame(0)
    option_form(driver, get_form_view(driver))
    driver.find_element_by_xpath('//*[@id="formSubmitButton"]').click()
    driver.switch_to_default_content()
    # 获取添加成功后的返回值
    network_data = info(driver)
    network_data.reverse()
    for data in network_data:
        if '/api/v2/Data/ObjectData' in data.get('request').get('url'):
            response = json.loads(data.get('response_data').get('body'))
            break
    time.sleep(5)
    driver.refresh()
    return response if response.keys() else None


def copy_list_data(driver, list_index, button_xpath):
    """
    复制
    """
    time.sleep(2)
    # button_xpath = f'//*[@class="table-item-check table-item-check-back-noMoving pc-sys-Checkbox-nomal-svg"]'
    element = driver.find_elements_by_xpath(button_xpath)[list_index + 2]
    driver.execute_script(f'arguments[0].scrollIntoView()', element)
    driver.execute_script(f'arguments[0].click()', element)
    driver.find_element_by_xpath(
        '//*[@id="indexPageViewName"]/div[2]/div/div/div[1]/div[3]/div[1]/div[2]/span').click()
    driver.switch_to_frame(0)
    option_form(driver, get_form_view(driver))
    driver.find_element_by_xpath('//*[@id="formSubmitButton"]').click()
    driver.switch_to_default_content()
    time.sleep(5)
    driver.refresh()


def delete_list_data(driver, list_index, button_xpath):
    """
    复制
    """
    # button_xpath = f'//*[@class="table-item-check table-item-check-back-noMoving pc-sys-Checkbox-nomal-svg"]'
    time.sleep(2)
    element = driver.find_elements_by_xpath(button_xpath)[list_index + 1]
    driver.execute_script(f'arguments[0].scrollIntoView()', element)
    driver.execute_script(f'arguments[0].click()', element)
    driver.find_element_by_xpath(
        '//*[@id="indexPageViewName"]/div[2]/div/div/div[1]/div[3]/div[1]/div[3]/span').click()
    time.sleep(1)
    driver.find_elements_by_xpath(
        '//*[@class="us-footer clearfix"]/div/span')[0].click()
    time.sleep(5)
    driver.refresh()


def go_to_data_details(driver, details_page_name, details_page_id):
    """
    进入列表数据详情

    :param driver: driver: 实例
    :param details_page_name: 哪个产品的详情页
    :param details_page_id: 详情页的id('新增接口有返回')
    """
    host_url = get_environment_data(os.environ.get('environment')).get('cloud_url')
    details_page_mapping = requests.get(
        'http://8.141.50.128:80/static/json_data/details_page_mapping.json').json().get(details_page_name)
    interface_url = ''
    if interface_url.get(details_page_name) is None:
        raise Configuration_file_error(msg='mappings文件中没有对应的详情页地址')
    interface_url = details_page_mapping.get(details_page_name)
    driver.get(host_url + interface_url + details_page_id)


def check_list_data(driver):
    """
    校验列表数据当前分页中的指定数据或所有的所有字段是否有值
    """
    list_elements = list()
    for list_element in driver.find_elements_by_xpath('//*[@class="z-table"]/div/div'):
        col_element_data = dict()
        for col_element in list_element.find_elements_by_xpath('./div'):
            if col_element.get_attribute('name') == 'CreatedBy':
                col_element_data[col_element.get_attribute('name')] = \
                    col_element.find_element_by_xpath('./div/div/span[2]').text
                continue
            col_element_data[col_element.get_attribute('name')] = col_element.text
        list_elements.append(col_element_data)
    network_data = info(driver)
    tab_list_data = None
    for data in network_data:
        if '/api/v2/UI/TableList' in data.get('request').get('url'):
            tab_list_data = json.loads(data.get('response_data').get('body'))
            break
    if tab_list_data is not None:
        for biz_data in tab_list_data.get('biz_data'):
            col_list = list_elements.pop(0)
            failure_data = [c for c in list(col_list.keys()) if c not in list(biz_data.keys())]
            if failure_data:
                for data in failure_data:
                    pytest_assume(driver, col_list.get(data), list(biz_data.keys()), '列表中的字段在接口中不存在即没有数据')
            else:
                pytest_assume(driver, True, True, '对比当前页面的所有字段，数据正确')
                failure_data = [d for d in list(col_list.keys()) if col_list.get(d) not in biz_data.get(d).get('value')]
                if 'CreatedBy' in failure_data:
                    failure_data.pop(failure_data.index('CreatedBy'))
                    CreatedBy = biz_data.get('CreatedBy').get('text').split('(')[0]
                    pytest_assume(driver, col_list.get('CreatedBy'), CreatedBy, '创建人字段值正确')
                if failure_data:
                    for data in failure_data:
                        pytest_assume(driver, col_list.get(data), biz_data.get(data).get('value'),
                                      '列表中的字段对应值在接口中不存在即没有数据')
                else:
                    pytest_assume(driver, True, True, '对比当前页面的所有字段的值，数据存在')
                continue
