from setuptools import setup, find_packages

setup(
    name='return_rates_data',
    description='Return Rate Data Generation Service',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),
    install_requires=[r.replace('\n', '') for r in open('requirements.txt')],
    entry_points={
        'console_scripts': ['return_rates_data=return_rates_data.__main__:main'],
    }
)
