import re

from setuptools import setup

with open("voiceio/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

packages = [
    "voiceio",
]

setup(
    name="voiceio",
    version=version,
    packages=packages,
    project_utls={
        # "Documentation": "https://voiceio.rtfd.io",
        "Issue Tracker": "https://github.com/pycord/voiceio/issues",
        "Pull Request Tracker": "https://github.com/pycord/voiceio/pulls",
    },
    url="https://github.com/pycord/voiceio",
    license="BSD 3-Clause",
    author="Vincent",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=requirements,
    description="Voice Interfacing Module Adding Extra Features to Pycord",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
