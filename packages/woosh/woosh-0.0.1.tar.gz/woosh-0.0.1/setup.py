from setuptools import setup, find_packages

requirements = [
]

setup(
    name="woosh",
    version="0.0.1",
    zip_safe=False,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        woosh=woosh.main:main
    ''',
    )
