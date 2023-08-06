import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Soundboard",
    version="2.0.3",
    author="ghostlypi",
    author_email="contact@parthiyer.com",
    description="This is a wave form generator and interpreter!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghostlypi/Soundboard.git",
    project_urls={
        "Bug Tracker": "https://github.com/ghostlypi/Soundboard/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
