import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LatexTemplater",
    version="0.5.2",
    author="Nathan Rose",
    author_email="mail.nathanrose@gmail.com",
    description="A package to allow python templating in latex files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/NathanRoseCE/LatexTemplater',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        'ninja2',
    ],
    entry_points={
        'console_scripts': [
            'sample=ArgParser:main',
        ],
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
