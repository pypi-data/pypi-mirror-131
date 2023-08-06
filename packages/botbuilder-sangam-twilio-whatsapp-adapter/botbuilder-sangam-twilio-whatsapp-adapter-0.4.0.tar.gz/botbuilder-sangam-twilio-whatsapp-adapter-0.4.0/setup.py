from setuptools import setup
import os

REQUIRES = [
    "twilio~=7.3.1"   
]

root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root, "botbuilder", "sangam", "twilio", "whatsapp","adapter", "about.py")) as f:
    package_info = {}
    info = f.read()
    exec(info, package_info)

with open(os.path.join(root, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=package_info["__title__"],
    version=package_info["__version__"],
    url=package_info["__uri__"],
    author=package_info["__author__"],
    author_email=package_info["__author_email__"],
    description=package_info["__description__"],
    keywords="botbuilder bots ai botframework twilio whatsapp adapter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=package_info["__license__"],
    packages=[
        "botbuilder.sangam.twilio.whatsapp.adapter",
    ],
    install_requires=REQUIRES,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)