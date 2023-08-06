import os
from setuptools import setup, find_packages
from hmin import __version__, __author__, __description__
#from hmin.cli import main

def get_requires():
    result = []
    with open("./requirements.txt", "r") as f:
        for package_name in f:
            result.append(package_name)
    return result

setup(
    name='hmin',                  # 모듈명
    version=__version__,             # 버전
    author=__author__,             # 저자
    description=__description__,     # 설명
    packages=find_packages(),
    python_requires='>=3.6.0',
    install_requires=get_requires(), # 패키지 설치를 위한 요구사항 패키지들
    entry_points={
        # nmt라는 명령어를 실행하면
        # hmin모듈 cli.py에서 main함수를 실행한다는 의미
        "console_scripts" : ["hmin=hmin.cli:main"]
    },
    include_package_data=True,
    zip_safe=False,
)
