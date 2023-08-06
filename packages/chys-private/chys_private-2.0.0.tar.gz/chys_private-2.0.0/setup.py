from distutils.core import setup

with open('README') as file:
    readme = file.read()


setup(
    name='chys_private',
    version='2.0.0',
    packages=['wargame'],
    url='http://localhost:8071/simple',
    description='my private game',
    long_description=readme,
    author='luoquan',
    author_email='178517202@qq.com'
)
