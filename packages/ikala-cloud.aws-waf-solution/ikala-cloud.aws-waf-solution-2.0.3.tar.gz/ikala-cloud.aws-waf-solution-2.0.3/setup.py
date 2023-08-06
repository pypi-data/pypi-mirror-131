import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "ikala-cloud.aws-waf-solution",
    "version": "2.0.3",
    "description": "Cloudfront,ALB and API Gateway with Automated WAF",
    "license": "Apache-2.0",
    "url": "https://github.com/iKala-Cloud/aws-waf-solution",
    "long_description_content_type": "text/markdown",
    "author": "Chris Yang",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/iKala-Cloud/aws-waf-solution"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "ikala-cloud.aws-waf-solution",
        "ikala-cloud.aws-waf-solution._jsii"
    ],
    "package_data": {
        "ikala-cloud.aws-waf-solution._jsii": [
            "aws-waf-solution@2.0.3.jsii.tgz"
        ],
        "ikala-cloud.aws-waf-solution": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk-lib>=2.2.0, <3.0.0",
        "aws-cdk.aws-glue-alpha>=2.2.0.a0, <3.0.0",
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
