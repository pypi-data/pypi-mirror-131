import setuptools

long_description = """
A collection of modern flat themes inspired by Bootstrap. There are more than a dozen built-in themes, and you also have
the ability to easily create your own.

## Links
- **Documentation:** https://ttkbootstrap.readthedocs.io/en/version-0.5/
- **GitHub:** https://github.com/israel-dryer/ttkbootstrap
"""

setuptools.setup(
    name="ttkbootstrap",
    version="0.5.3",
    author="Israel Dryer",
    author_email="israel.dryer@gmail.com",
    description="A collection of modern ttk themes inspired by Bootstrap",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/israel-dryer/ttkbootstrap",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["pillow>=8.2.0"],
    python_requires=">=3.6",
)
