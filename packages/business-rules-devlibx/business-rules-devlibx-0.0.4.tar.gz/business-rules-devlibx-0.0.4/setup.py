#! /usr/bin/env python

import setuptools

with open('HISTORY.rst') as f:
    history = f.read()

description = 'Python DSL for setting up business intelligence rules that can be configured without code'

setuptools.setup(
    name='business-rules-devlibx',
    version="0.0.4",
    description='{0}\n\n{1}'.format(description, history),
    author='devlibx',
    author_email='devlibxgithub@gmail.com',
    url='https://github.com/devlibx/business-rules',
    packages=['business_rules'],
    package_dir={"": "."},
    license='MIT'
)
