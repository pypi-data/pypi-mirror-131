
import time

import pytest

if __name__ == '__main__':

    pytest.report_title = '中文浏览器环境'
    pytest.browser_language = 'zh,zh_CN'
    report_name = 'test_No.' + str(int(time.time() * 1000)) + '.html'
    pytest.main(['-v', 'test_demo.py',
                 '--html=static/report/' + report_name])
