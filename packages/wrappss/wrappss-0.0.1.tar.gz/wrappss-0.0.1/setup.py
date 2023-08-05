from setuptools import setup, find_packages

setup(
    # 包名
    name="wrappss",
    # find_packages()默认以setup.py所在路径为源路径,递归遍历找到所有的python包(含有init.py的文件夹)
    packages=find_packages(),
    # 版本，如修改后再次上传，需要使用不同版本号
    version='0.0.1',
    description="my wrappers",
    author="Tsurol",
    author_email='2656155887@qq.com',
    # 一般放项目的托管地址
    url='https://github.com/Tsurol',
    # 其他信息，一般包括项目支持的Python版本，License，支持的操作系统。
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
    # 项目依赖哪些库，这些库会在pip install的时候自动安装
    install_requires=[]
)
