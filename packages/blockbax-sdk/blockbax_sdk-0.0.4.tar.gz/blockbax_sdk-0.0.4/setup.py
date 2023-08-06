import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blockbax_sdk",
    version=os.environ["VERSION"],
    author="Blockbax",
    description="Blockbax Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "urllib3>=1.26.6",
        "pytz>=2020.1",
        "requests>=2.26.0",
        "python_dateutil>=2.8.2",
    ],
    url="https://blockbax.com/docs/integrations/python-sdk/",
    packages=setuptools.find_namespace_packages(include=["blockbax_sdk.*","blockbax_sdk"],exclude=["examples", "examples.*","tests","tests.*"]),
    include_package_data=True, 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    python_requires='>=3.8',
)