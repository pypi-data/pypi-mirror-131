import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "sparkgeo-awscdk-construct-lib",
    "version": "0.0.3",
    "description": "awscdk-constructs-library",
    "license": "Apache-2.0",
    "url": "https://github.com/sparkgeo/awscdk-constructs-library",
    "long_description_content_type": "text/markdown",
    "author": "Mike Connor<mike@sparkgeo.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/sparkgeo/awscdk-constructs-library"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "sparkgeo-awscdk-construct-lib",
        "sparkgeo-awscdk-construct-lib._jsii"
    ],
    "package_data": {
        "sparkgeo-awscdk-construct-lib._jsii": [
            "awscdk-constructs-library@0.0.3.jsii.tgz"
        ],
        "sparkgeo-awscdk-construct-lib": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.49.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
