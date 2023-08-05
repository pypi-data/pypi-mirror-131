import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="labjack-unified",
    version="0.0.2",
    author="Eduardo Nigro",
    author_email="eduardo.b.nigro@gmail.com",
    description="Unified methods for LabJacks U3, U6, and T7",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EduardoNigro/labjack-unified",
    project_urls={
        "Bug Tracker": "https://github.com/EduardoNigro/labjack-unified/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    install_requires=[
        "LabJackPython",
        "labjack-ljm",
        "plotly",
        "numpy"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
