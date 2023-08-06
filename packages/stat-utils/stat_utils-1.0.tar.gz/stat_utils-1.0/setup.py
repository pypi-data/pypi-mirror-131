from setuptools import setup

setup(
    name='stat_utils',
    version='1.0',
    description='Utils for statistics',
    url='https://github.com/KrozeRoll',
    author='Alexander Osikov',
    author_email='krozer95@gmail.com',
    license='BSD 2-clause',
    packages=['stat_utils'],
    install_requires=['typing',
                      'numpy'
                      ]
)