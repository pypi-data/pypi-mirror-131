import setuptools

with open("README.md", "r") as readme:
    readme_text = readme.read()

setuptools.setup(
    name="betterjsondb",
    version="0.1.7",
    author="DarkJoij",
    author_email="aleksey.c5@yandex.ru",
    description="A useful library for simplifying work with .json files.",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    url="https://github.com/DarkJoij/betterjsondb",
    packages=["betterjsondb"],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
