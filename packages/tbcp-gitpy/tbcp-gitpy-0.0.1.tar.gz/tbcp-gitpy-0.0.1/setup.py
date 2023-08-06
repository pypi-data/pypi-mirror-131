#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()
with open('requirements') as req_file:
    reqs = req_file.read()

setup(
    name="tbcp-gitpy",
    license="MIT",
    version='0.0.1',
    description="TBCP - GitPy - Working with Git in Python",
    author="Bootcamp Contributors",
    author_email="contributors@bootcamp-project.com",
    keywords="Git, Branches, Repositories, Commits, Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/the-bootcamp-project/companion",
    project_urls={
        'Documentation': 'https://companion.bootcamp-project.com',
        'Source': 'https://gitlab.com/the-bootcamp-project/companion',
        'Tracker': 'https://gitlab.com/the-bootcamp-project/companion/-/issues',
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires=">=3.9",
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=[
                           "docs", "build", "dist"]),
    install_requires=reqs,
    include_package_data=True,
    zip_safe=False
)
