import setuptools

import sphinx_inplace

with open("README.rst", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="sphinx-inplace",
    version=sphinx_inplace.__version__,
    author=sphinx_inplace.__author__,
    author_email=sphinx_inplace.__email__,
    description="Automatically manage *.rst files in sphinx projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/panhaoyu/sphinx-inplace",
    project_urls={
        "Bug Tracker": "https://github.com/panhaoyu/sphinx-inplace/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
)
