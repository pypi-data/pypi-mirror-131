
from b_c_components.get_config.get_config import Setting


def get_environment_data(environment):
    """

    :return:
    """
    url_dict = {

        'test': {
            'italent_url': 'https://www.italent.link',
            'cloud_url': 'https://cloud.italent.link',
            'tms_url': 'https://tms.beisen.net',

        },
        'prod': {
            'italent_url': 'https://www.italent.cn',
            'cloud_url': 'https://cloud.italent.cn',
            'tms_url': 'https://tms.beisen.com',

        }

    }

    return url_dict.get(environment)


