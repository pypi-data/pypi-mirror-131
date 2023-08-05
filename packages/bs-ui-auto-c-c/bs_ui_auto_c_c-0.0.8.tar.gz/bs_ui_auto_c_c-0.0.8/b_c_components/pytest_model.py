import pytest


def pytest_assume(driver, expected_results, actual_results, msg):
    """
    断言
    :param driver:
    :param expected_results: 预期结果
    :param actual_results: 实际结果
    :param msg
    """
    screenshots = pytest.assume(
        expected_results == actual_results,
        f"预期结果与实际结果不一致：预期结果:{expected_results}   实际结果:{actual_results}")
    results_msg = f" : [不通过]" if not screenshots else ' : [通过]'
    driver.global_instance.get('assess_msg').append(
        {driver.def_name: msg + results_msg})
