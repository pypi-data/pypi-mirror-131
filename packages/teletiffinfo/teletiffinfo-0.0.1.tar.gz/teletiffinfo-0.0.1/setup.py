from setuptools import setup, find_packages

setup(
    name="teletiffinfo",
    version="0.0.1",
    author="Xiao Gui",
    author_email="xgui3783@gmail.com",
    description="Fetch metadata from remote (https) tiff.",
    packages=find_packages(
        include=["teletiffinfo"]
    ),
    install_requires=[
        "requests>=2.26.0",
    ],
)