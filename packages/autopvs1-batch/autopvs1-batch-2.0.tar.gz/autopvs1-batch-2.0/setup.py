import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autopvs1-batch",
    version="2.0",
    author="Ying Zhu",
    author_email="win19890412@163.com",
    description="A tool for batch run autoPVS1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "autopvs1": ['config.ini', "data/*", 'maxentpy/data/*'],
    },
    scripts=['autopvs1-batch.py']
)
