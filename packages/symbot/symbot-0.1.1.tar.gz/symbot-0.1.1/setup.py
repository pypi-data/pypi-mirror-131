import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="symbot",
    version="0.1.1",
    author="Tobias Lass",
    author_email="tobi208@github.com",
    description="A twitch chat bot for developers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tobi208/symbot",
    project_urls={
        "Bug Tracker": "https://github.com/tobi208/symbot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={"symbot": ["data/*.json"]},
    python_requires=">=3.7",
)
