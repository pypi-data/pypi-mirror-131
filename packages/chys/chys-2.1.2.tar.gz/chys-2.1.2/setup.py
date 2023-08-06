from distutils.core import setup

with open('README') as file:
    readme = file.read()


setup(
    name='chys',
    version='2.1.2',
    packages=['wargame'],
    url='https://test.pypi.org/legacy',
    description='my game',
    long_description=readme,
    author='luoquan',
    author_email='178517202@qq.com'
)
