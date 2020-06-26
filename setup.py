#
# Copyright (C) 2020 PyCloud - All Rights Reserved
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from setuptools import setup

install_requires = []
with open("requirements.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            install_requires.append(line)

setup(
    name="pycloud-client",
    version="0.7.1",
    description="Connectors for PyCloud clusters",
    license="Apache 2.0",
    author="pycloud.ai",
    author_email="contact@pycloud.ai",
    url="https://pycloud.ai",
    long_description=open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
    ).read(),
    long_description_content_type="text/markdown",
    install_requires=["setuptools", "docopt"] + install_requires,
    packages=[
        "pycloud_client",
        "pycloud_client.proto",
    ],
    include_package_data=True,
)
