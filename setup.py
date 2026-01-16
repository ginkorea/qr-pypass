from setuptools import setup, find_packages

setup(
    name="qrpypass",
    version="0.2.3",
    description="Headless QR decoder + TOTP authenticator Flask mini-service",
    author="Josh Gompert",
    author_email="",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "Flask>=3.0.0",
        "cryptography>=41.0.0",
        "Pillow>=10.0.0",
        "numpy>=1.23.0",
        "qrcode[pil]>=7.4.2",
        "opencv-contrib-python-headless>=4.8.0",
        "pyzbar>=0.1.9",
        "zxing-cpp>=2.2.0",
    ],
    python_requires=">=3.9",
)
