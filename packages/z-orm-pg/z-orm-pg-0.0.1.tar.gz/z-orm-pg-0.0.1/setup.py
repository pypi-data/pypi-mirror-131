from setuptools import setup

setup(
    name='z-orm-pg',
    version='0.0.1',
    author='homo-zhou',
    author_email='408088242@qq.com',
    url='http://127.0.0.1',
    description='An orm for postgresql using peewee',
    packages=['models'],
    install_requires=['peewee'],
    entry_points={
        'console_scripts': []
    }
)