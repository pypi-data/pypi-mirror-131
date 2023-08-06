import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airflow-commons",
    version="0.0.43",
    author="Startup Heroes",
    description="Common functions for airflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/migroscomtr/airflow-commons/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pytz>=2018.4",
        "datetime",
        "google-cloud-bigquery",
        "pandas",
        "sqlalchemy",
        "pymysql",
        "boto3==1.20.21",
        "botocore==1.23.22",
        "pyyaml",
        "s3fs",
        "s3transfer",
        "pyarrow>=5.0.0",
    ],
    include_package_data=True,
)
