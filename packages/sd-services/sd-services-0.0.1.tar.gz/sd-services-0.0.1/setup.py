import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sd-services",
    version="0.0.1",
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
            'cycler==0.11.0',
            'fonttools==4.28.2',
            'joblib==1.1.0',
            'kiwisolver==1.3.2',
            'kmodes==0.11.1',
            'matplotlib==3.5.0',
            'networkx==2.6.3',
            'numpy==1.21.4',
            'packaging==21.3',
            'pandas==1.3.4',
            'Pillow==8.4.0',
            'pomegranate==0.14.7',
            'pyparsing==3.0.6',
            'python-dateutil==2.8.2',
            'pytz==2021.3',
            'PyYAML==6.0',
            'scikit-learn==1.0.1',
            'scipy==1.7.3',
            'seaborn==0.11.2',
            'setuptools-scm==6.3.2',
            'six==1.16.0',
            'sklearn==0.0',
            'threadpoolctl==3.0.0',
            'tomli==1.2.2',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)
