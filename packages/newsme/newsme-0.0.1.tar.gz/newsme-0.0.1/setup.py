import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="newsme",
    version="0.0.1",
    author="lunfman",
    author_email="",
    description="package for simple interaction with NewsApi and sending html mails",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lunfman/NewsMe",
    install_requires=[
        'requests==2.25.1'
    ],
    project_urls={
        "Bug Tracker": "https://github.com/lunfman/NewsMe/issues",
    },
    license = 'MIT License',
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)