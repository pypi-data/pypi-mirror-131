from setuptools import setup


setup(
    exclude_package_data={"": ['.mypy_cache', '__pycache__']}
)
