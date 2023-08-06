from setuptools import setup,find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kolibri-report",
    version="0.1.1",
    author="Aneruth,Mohamed Ben Haddou",
    author_email="ane1998@gmail.com,mbenhaddou@mentis.io",
    description="A report package for kolibri-ml",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aneruth/kolibri-report",
    project_urls={
        "Bug Tracker": "https://github.com/Aneruth/kolibri-report/issues",
    },
    install_requires=["kolibri-ml","seaborn"],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.json', '*.npy', '*.db'],
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.7',
)