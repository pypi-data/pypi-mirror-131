import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-daily-spend-to-slack",
    "version": "0.0.2",
    "description": "daily-spend-to-slack",
    "license": "MPL-2.0",
    "url": "https://github.com/tom.stroobants/daily-spend-to-slack.git",
    "long_description_content_type": "text/markdown",
    "author": "Tom Stroobants<tom@stroobants.dev>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/tom.stroobants/daily-spend-to-slack.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_daily_spend_to_slack",
        "cdk_daily_spend_to_slack._jsii"
    ],
    "package_data": {
        "cdk_daily_spend_to_slack._jsii": [
            "daily-spend-to-slack@0.0.2.jsii.tgz"
        ],
        "cdk_daily_spend_to_slack": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk-lib>=2.0.0, <3.0.0",
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
