import setuptools
import os, glob
from version import version_up

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = setuptools.find_packages(exclude=['local', 'local.*'])

print('packages:', packages)

version = version_up()
print("version:", version)
setuptools.setup(
    executable=True,
    name="pysimplese",  # Replace with your own username
    version=version,
    author="Wang Pei",
    author_email="1535376447@qq.com",
    description="A simple search engine for fun and simple use cases.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/peiiii/pysimplese",
    packages=packages,
    package_dir={'pysimplese': 'pysimplese'},
    install_requires=['fire', "lxml>=4",
                      "PyStemmer>=2",
                      "requests>=2", ],
    entry_points={
        'console_scripts': [
            'pysimplese = pysimplese.clitools.cli:main',
        ]
    },
    include_package_data=True,
    package_data={
        'pysimplese': [
            'data/*', 'data/*/*', 'data/*/*/*', 'data/*/*/*/*', 'data/*/*/*/*/*', 'data/*/*/*/*/*/*',
            'data/*/*/*/*/*/*/*',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
