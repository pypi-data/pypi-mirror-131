import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "flureenjs.core",
    "version": "1.0.3",
    "description": "PoC app to try to generate libraries from flureenjs",
    "license": "ISC",
    "url": "https://github.com/fluree/fluree-jsii.git",
    "long_description_content_type": "text/markdown",
    "author": "Jacob Parsell<jparsell@flur.ee>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/fluree/fluree-jsii.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "flureenjs.core",
        "flureenjs.core._jsii"
    ],
    "package_data": {
        "flureenjs.core._jsii": [
            "fluree-jsii@1.0.3.jsii.tgz"
        ],
        "flureenjs.core": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.47.0, <2.0.0",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
