#!/usr/bin/env python3
"""
Setup script for WhatsApp Profile Changer.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="whatsapp-profile-changer",
    version="0.1.0",
    author="WhatsApp Profile Changer Team",
    author_email="example@example.com",
    description="An automated tool to change your WhatsApp Web profile picture at regular intervals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ronaldlanton/whatsapp-profile-changer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "selenium>=4.0.0",
        "pillow>=8.0.0",
        "pytz>=2021.1",
    ],
    entry_points={
        "console_scripts": [
            "whatsapp-profile-changer=whatsapp_profile_changer.run:main",
        ],
    },
)