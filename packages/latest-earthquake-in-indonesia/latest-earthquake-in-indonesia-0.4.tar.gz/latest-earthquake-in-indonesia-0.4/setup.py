"""
https://packaging.python.org/en/latest/tutorials/packaging-projects/
markdown guide:https://www.markdownguide.org/cheat-sheet/
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="latest-earthquake-in-indonesia",
    version="0.4",
    author="Rijaluddin",
    author_email="ortonrko90900@gmail.com",
    description="This package about the last earthquake from BMKG Indonesia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kuli-coding/last-indonesia-earthquake",
    project_urls={
        "Github": "https://github.com/kuli-coding/last-indonesia-earthquake",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    ##package_dir={"": "src"},
    ##packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)