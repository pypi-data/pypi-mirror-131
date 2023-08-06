from setuptools import find_packages, setup

from dir_struct_cli.main import __version__

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="dir-structure-cli",
    version=__version__,
    license="MIT",
    description="Generate directory skeletons for some famous frameworks",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Abdulrahman Dawoud",
    author_email="abdulrahman.goldendawn@gmail.com",
    packages=["dir_struct_cli"],
    url="https://github.com/gmyrianthous/example-publish-pypi",
    keywords="example project",
    install_requires=[
        "click",
    ],
)
