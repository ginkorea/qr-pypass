from setuptools import setup, find_packages

setup(
    name="qrpypass",
    version="0.1.0",
    description="Headless QR decoder + TOTP authenticator Flask mini-service",
    author="Josh Gompert",
    author_email="",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[],
    python_requires=">=3.9",
)
