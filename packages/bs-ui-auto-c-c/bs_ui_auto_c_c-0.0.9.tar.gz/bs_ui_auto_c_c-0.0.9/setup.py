import setuptools

setuptools.setup(
    name="bs_ui_auto_c_c",
    version="0.0.9",
    author="sijunji",
    author_email="sijunji@outlook.com",
    description="一个selenium自动安装驱动、日志的项目",
    packages=setuptools.find_packages(),
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding='utf-8').read(),
    license='apache3.0',
    install_requires=[
        'pytest',
        'selenium',
        'requests',
        'biplist',
        'openpyxl',
        'pytest_html',
        'pytest_assume',
        'pytest-repeat',
        'pytest-metadata',
        'pytest-rerunfailures',
        'snownlp',
        'pyDes',
        'rsa',
        'xlrd==1.2.0',
        'xlutils==2.0.0'
    ]

)
