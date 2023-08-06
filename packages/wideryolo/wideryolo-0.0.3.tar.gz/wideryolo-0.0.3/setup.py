from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="wideryolo",
    version="0.0.3",
    description="Wider-Yolo Kütüphanesi ile Yüz Tespit Uygulamanı Yap",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/kadirnar/",
    python_requires=">=3.7",
    author="Kadir Nar",
    author_email="kadir.nar@hotmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    packages=["wideryolo"],
    include_package_data=True,
    install_requires=["gdown==4.2.0", "Pillow==8.4.0"],
)
