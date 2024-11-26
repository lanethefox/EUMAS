"""Setup script for EUMAS."""

from setuptools import setup, find_packages

setup(
    name="eumas",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "weaviate-client==4.9.4",
        "openai==1.55.1",
        "python-dotenv==1.0.0",
        "pyyaml==6.0.1",
        "loguru==0.7.2",
        "python-json-logger==2.0.7",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-cov==4.1.0",
            "black==23.11.0",
            "flake8==6.1.0",
            "mypy==1.7.0",
        ],
    },
    python_requires=">=3.9",
)
