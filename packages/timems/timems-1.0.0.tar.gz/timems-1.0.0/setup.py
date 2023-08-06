import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="timems",
    version="1.0.0",
    author="Jamsson",
    description="Variable time formats in one package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['python', 'time', 'tools', 'utils', 'formats', 'seconds']
)