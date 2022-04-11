from setuptools import setup

setup(
    name="langpy",
    version="0.0.1",
    description="Executes commands from console while your bot is running.",
    long_description=open("README.md").read(),
    url="https://github.com/Mihitoko/LangPy",
    long_description_content_type="text/markdown",
    author="Mihito",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.7"
    ],
    packages=[
        "langpy",
        "langpy.compiler",
        "langpy.errors",
        "langpy.translator"
    ],
    include_package_data=True,
    install_requires=["PyYAML~=6.0", "deepl~=1.3.1"],
)
