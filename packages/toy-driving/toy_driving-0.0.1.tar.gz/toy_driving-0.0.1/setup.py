from setuptools import setup, find_packages

setup(
    name='toy_driving',
    packages=find_packages(),
    version='0.0.1',
    author='Zhang Dongkun',
    author_email='zhangdongkun98@gmail.com',
    url='https://github.com/zhangdongkun98/toy-driving',
    description='A gym-like autonomous driving environment for debugging RL algorithms.',
    install_requires=[
    ],

    include_package_data=True
)
