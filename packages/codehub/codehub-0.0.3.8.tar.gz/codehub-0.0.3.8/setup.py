import setuptools
import os, glob
from version import version_up

with open("README.md", "r") as fh:
    long_description = fh.read()




packages=setuptools.find_packages(exclude=['local','local.*'])

print('packages:', packages)

version = version_up()
print("version:", version)
setuptools.setup(
    executable=True,
    name="codehub",  # Replace with your own username
    version=version,
    author="Wang Pei",
    author_email="1535376447@qq.com",
    description="Cloud python code library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/peiiii/codehub",
    packages=packages,
    package_dir={'codehub': 'codehub'},
    install_requires=['jinja2', 'fire','pyyaml>=6.0'],
    entry_points={
        'console_scripts': [
            'codehub = codehub.clitools.cli:main',
            'codefire = codehub.clitools.codefire:main',
        ]
    },
    include_package_data=True,
    package_data={
        'codehub': [
            'data/*', 'data/*/*', 'data/*/*/*', 'data/*/*/*/*', 'data/*/*/*/*/*', 'data/*/*/*/*/*/*',
            'data/*/*/*/*/*/*/*',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)