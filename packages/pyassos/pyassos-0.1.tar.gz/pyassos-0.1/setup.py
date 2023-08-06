import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyassos",
    version="0.1",
    author="Matthieu BOUCHET",
    author_email="matthieu.bouchet@outlook.com",
    description="Bibliothèque fournissant une interface de connexion "
                "avec l'API open-source du "
                "Répertoire National des Associations (RNA) "
                "fournie par Etalab ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MatthieuBOUCHET/PyAssos/",
    project_urls={
        "Bug Tracker": "https://github.com/MatthieuBOUCHET/"
                       "PyAssos/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Natural Language :: French",
        "Topic :: Utilities"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3",
)
