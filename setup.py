import setuptools
import os

install_requires = ["ipython>=1.0"]

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description =  f.read()

VERSION = "0.0.4"

setuptools.setup(
    name="iwut",
    version=VERSION,
    author="Alvin Wan",
    author_email="hi@alvinwan.com",
    description=(
        "Friendlier tracebacks, collapsing frames with library code,"
        "inline variable values, and adding context"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords="ipython traceback error exception",
    url="https://pypi.python.org/pypi/wut",
    license="MIT",
    packages=["iwut"],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
)
