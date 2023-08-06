import setuptools
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hoothoot_logger",
    version="1.0.3",
    author="Victor Coelho",
    author_email="victorhdcoelho@gmail.com",
    description="Lib to connect with hoothoot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/victorhdcoelho/hoothoot-logger",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["dataclasses", "requests"],
    include_package_data=True,
    zip_safe=False
)
