import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ezconn",
    version="0.0.5",
    author="ANALYTIKA PLUS",
    author_email="support@analytikaplus.ru",
    description="Easy python DB-API 2.0 connector for most popular analytical DB",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/analytikaplus/ezconn",
    project_urls={
        "Bug Tracker": "https://github.com/analytikaplus/ezconn/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    py_modules=['ezconn'],
    install_requires=[
          'JayDeBeApi',
      ],
    python_requires=">=3.6",
)