from setuptools import setup  # type: ignore

version = '1.0.0'

setup(
    name='parser_example',
    version=version,
    description="",
    package_dir={"": "src"},
    packages=[
        "parser",
        "common",
    ],
    install_requires=[
      "telethon==1.31.1"
    ],
    python_requires=">=3.11"
)
