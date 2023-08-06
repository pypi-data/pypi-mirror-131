from setuptools import setup, find_packages

setup(
    name="spoceatmos",
    version="1.0",
    keywords=("Space", "Oceanic", "Atmospheric"),
    description="Space & Oceanic & Atmospheric Data Collector",
    long_description="Space & Oceanic & Atmospheric Data Collector",
    license="MIT Licence",

    url="https://lno1.com/spoceatmos",
    author="xiehai",
    author_email="xiehai@vip.qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[],

    scripts=[],
    entry_points={
        'console_scripts': [
            'test = test.help:main'
        ]
    }
)