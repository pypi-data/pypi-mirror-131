import pathlib

from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
REQUIRED = (HERE / "requirements.txt").read_text().splitlines()

setup(
    name="modern-flask",
    version="202112b4",
    description="modern flask framework",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitee.com/modernapps/modern-flask",
    author="guoyk93",
    author_email="hi@guoyk.net",
    license="MIT",
    classifiers=[
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Framework :: Flask"
    ],
    packages=["modern"],
    include_package_data=True,
    install_requires=REQUIRED,
)
