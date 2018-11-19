import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlalchemy-model-convert",
    version="1.0",
    author="tystudy",
    author_email="",
    description="使用简单方便的模型转字典模块(Python3)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/persistty/sqlalchemy-model-convert",
    packages=setuptools.find_packages()
)
