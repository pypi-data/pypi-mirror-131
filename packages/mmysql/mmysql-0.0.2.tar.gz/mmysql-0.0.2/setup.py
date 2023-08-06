import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mmysql",
    version="0.0.2",
    author="lsw",
    author_email="lisw19@126.com",
    description="Wrapping pyMSQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/lisw19/dashboard/projects",
    packages=setuptools.find_packages(),
    platforms=["all"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
