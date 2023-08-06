import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

setuptools.setup(
    name='rest-db-client',
    version='2.2.0',
    author_email="info@librecube.org",
    description='Client for RESTful databases',
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/librecube/lib/python-rest-db-client",
    license="MIT",
    python_requires='>=3',
    packages=setuptools.find_namespace_packages(where="src"),
    package_dir={"": "src"},
    install_requires=['requests'],
)
