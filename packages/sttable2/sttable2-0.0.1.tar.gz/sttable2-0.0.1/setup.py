"""Setup for the sttable2 package."""

import setuptools

with open('README.rst', encoding='utf-8') as f:
    README = f.read()

setuptools.setup(
    author="Anderson.Yao",
    author_email="359747390@qq.com",
    name='sttable2',
    license="MIT",
    description='Parser of multi-lines string representation tables',
    version='0.0.1',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://github.com/yaoanderson/sttable2',
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
)
