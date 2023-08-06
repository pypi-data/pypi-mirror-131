from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='bitlogs',
    version='1.0.1',
    description='This python library allows you to easily create logs for your code.',
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    url='',
    author='Vladislav Korecký',
    author_email='vladislav.ml@korecky.org',
    license='MIT',
    classifiers=classifiers,
    keywords=["bitlogs", "bitlog", "logs", "log", "logging", "logger", "python log"],
    packages=find_packages(),
    install_requires=['']
)