import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="goveelights",
    version="0.1.2",
    author="arcanearronax",
    description="A small package to interact with the Govee API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arcanearronax/govee_lights",
    project_urls={
        "Bug Tracker": "https://github.com/arcanearronax/govee_lights/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    keywords="govee, device, lights, client",
)
