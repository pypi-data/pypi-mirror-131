from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='flutter_icon_search',
    version='0.0.1',
    description='Material Icon filter for HitsApp ',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Sumith SreeKumar',
    author_email='sumithkumar710@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Flutter Icon Search',
    packages=find_packages(),
    install_requires=['']
)