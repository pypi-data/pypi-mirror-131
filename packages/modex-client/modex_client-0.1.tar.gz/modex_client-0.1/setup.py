import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="modex_client",
    version="0.1",
    # scripts=["src/main.py"],
    author="Veelancing Inc",
    author_email="stefan@velancing.io",
    description="Modex client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.vbrlabs.io/vanea/veelancing-modex",
    packages=setuptools.find_packages(),
    install_requires=["requests", "decouple"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
