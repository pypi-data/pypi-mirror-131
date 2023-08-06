import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="hetu",
    version="0.0.1",
    author="xuelang AI",
    author_email="wunsch0106@gmail.com",
    description="XuelangCloud AI platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests"
    ],

    # entry_points={
    #     "console_scripts": [
    #         "",
    #     ]
    # }
)