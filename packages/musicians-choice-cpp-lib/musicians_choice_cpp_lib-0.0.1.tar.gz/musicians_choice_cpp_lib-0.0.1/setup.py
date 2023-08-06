import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="musicians_choice_cpp_lib",
    # Replace with your own username above
    version="0.0.1",
    author="David Tynan",
    author_email="x20153104@student.ncirl.ie",
    description="Custom library for CPP project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[''],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

