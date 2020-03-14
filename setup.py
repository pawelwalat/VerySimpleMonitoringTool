from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Very Simple Monitoring Tool',
    version='0.1.0',
    description='Tool for simple monitoring activities',
    long_description=readme,
    author='Pawel Walat',
    author_email='pawel@walat.net',
    url='https://github.com/pawelwalat/VerySimpleMonitoringTool',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)