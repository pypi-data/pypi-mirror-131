import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Dreamake",
    version="0.0.100",
    author="Nitebound",
    author_email="zvisger@gmail.com",
    license="MIT",
    description="A pygame based game engine made in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Boglov/dreamake",
    project_urls={
        "Bug Tracker": "https://github.com/Boglov/dreamake/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=["pygame"]
)