from setuptools import setup

__project__ = "motivatememore"
__version__ = "0.0.1"
__description__ = "a Python module to motivate you"
__packages__ = ["motivate"]
__author__ = "Francisco Gutierrez"
__author_email__="franciscocw0101@gmail.com"

__classifiers__ = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Education",
    "Programming Language :: Python :: 3",
]

__keywords__=["motivation","learning"]

# if the program requires other programs for running
#__requires__=["guizero"]
# * don't forget to include in setup(requires=__requi....)

setup(
    name = __project__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    author_email=__author_email__,
    classifiers=__classifiers__,
    keywords=__keywords__,
)