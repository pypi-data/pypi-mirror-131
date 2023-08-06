import os
from setuptools import find_packages, setup


def get_dependencies():
    pwd = os.path.dirname(os.path.realpath(__file__))
    requirements_path = os.path.join(pwd, "requirements.txt")
    if os.path.isfile(requirements_path):
        with open(requirements_path) as f:
            return f.read().splitlines()


setup(
    name="meili-sdk",
    packages=find_packages(),
    version="0.1.0",
    description="Meili FMS SDK",
    author="Rimvydas Zilinskas",
    url="https://gitlab.com/meilirobots/dev/meili-sdk",
    author_email="rimvydas@meilirobots.com",
    license="MIT",
    install_requires=get_dependencies(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest==6.2.5", "pytest-mock==3.6.1"],
    test_suite="tests",
)
