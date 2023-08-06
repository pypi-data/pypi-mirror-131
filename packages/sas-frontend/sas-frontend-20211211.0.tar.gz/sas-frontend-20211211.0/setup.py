from setuptools import setup, find_packages

setup(
    name="sas-frontend",
    version="20211211.0",
    description="The SmartAutomatic frontend",
    author="The SmartAutomatic Authors",
    license="Apache-2.0",
    packages=find_packages(include=["sas_frontend", "sas_frontend.*"]),
    include_package_data=True,
    zip_safe=False,
)
