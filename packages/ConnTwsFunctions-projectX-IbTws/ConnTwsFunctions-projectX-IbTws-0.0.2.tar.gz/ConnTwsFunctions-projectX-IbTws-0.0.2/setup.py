import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ConnTwsFunctions-projectX-IbTws",
    version="0.0.2",
    author="ProjectX Authors",
    author_email="nikolay.gyuneliev@gmail.com",
    description="A package with Tws functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ProjectIbX/ConnTwsFunctions",
    project_urls={
        "Bug Tracker": "https://github.com/ProjectIbX/ConnTwsFunctions/src",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)