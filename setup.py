import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="easyddns",
    version="1.0.0 beta",
    author="viola",
    author_email="viola@aoitech.net",
    maintainer_email='viola@aoitech.net',
    description="a simple python client for ddns",
    platforms=["all"],
    license='Apache-2.0 license',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/viola-aoitech/easyddns",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache-2.0 license",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "requests>=2",
        "tqdm>=4"
    ]

)
