import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

setuptools.setup(
    name="linkpredict",
    version="2.2.1",
    author_email="info@librecube.org",
    description="A generic and dynamic link budget tool",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/librecube/lib/python-linkpredict",
    license="MIT",
    python_requires='>=3.4',
    packages=setuptools.find_namespace_packages(where="src"),
    package_dir={"": "src"},
    install_requires=['numpy', 'scipy', 'skyfield'],
)
