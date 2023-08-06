'''
@File       :   setup.py
@Author     :   Shawn
@Time       :   2021-12-15 17:22
@Version    :   1.0
@Contact    :   shx15979391664@163.com
@Dect       :   None
'''

from setuptools import setup, find_packages  # 这个包没有可以pip一下

setup(
    name="split-merge",  # 这个是pip项目发布的名称
    version="1.0.0",  # 版本号，pip默认安装最新版
    keywords=("pip", "split", "merge"),
    description="文件拆分 & 合并",
    long_description="文件拆分 & 合并",
    license="MIT Licence",

    # url="https://github.com/jiangfubang/balabala",  # 项目相关文件地址，一般是github，有没有都行吧
    author="Shawn",
    author_email="shx15979391664@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    py_modules=["split-merge-dir.split-merge"]  # 该模块需要的第三方库
)