"""
Apache-2.0

Copyright 2021 RPS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the LICENSE file for the specific language governing permissions and
limitations under the License.
"""
import re

from setuptools import find_packages, setup

with open("src/plugify/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

extra_requires = {
    "speed": [
        "orjson>=3.6.4",
        "aiodns>=1.1",
        "Brotlipy",
        "cchardet",
    ],
}

setup(
    name="plugify.py",
    version=version,
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    project_utls={
        "Documentation": "https://plugify.rtfd.io",
        "Issue Tracker": "https://github.com/RPSMain/plugify.py/issues",
        "Pull Request Tracker": "https://github.com/RPSMain/plugify.py/pulls",
    },
    url="https://github.com/RPSMain/plugify.py",
    license="Apache-2.0",
    author="RPS",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    install_requires=requirements,
    extra_requires=extra_requires,
    description="Pythonic API Wrapper For Plugify",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
