import sys

from b_c_components.get_config.get_config import Setting


class element_str:
    """
    公用元素变量地址
    """

    def __init__(self):
        self.italent_url = 'https://www.italent.'
        self.environment = Setting('config.ini').get_setting('environment_data', 'environment')
        self.environment = 'cn' if self.environment == 'prod' else 'link' if self.environment == 'test' else None


class class1:

    class acticity_data:
        test_601022 = {'username': '123', 'password': '123'}


c = class1().acticity_data.test_601022
