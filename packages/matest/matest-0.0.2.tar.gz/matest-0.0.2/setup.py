from setuptools import setup, find_packages

setup(
    name = "matest",
    version = "0.0.2",
    keywords = ("mate", "test", "matest"),
    description = "mate test",
    long_description = "测试伴侣工具集",
    license = "MIT Licence",

    url = "https://github.com/matest",
    author = "matest",
    author_email = "erenjian@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy", "pandas"]
)