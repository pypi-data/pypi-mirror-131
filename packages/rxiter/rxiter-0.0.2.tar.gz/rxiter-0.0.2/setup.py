from distutils.core import setup

setup(
    name="rxiter",
    license="MIT",
    version="0.0.2",
    packages=["rxiter"],
    install_requires=["functools"],
    description="Observable operations for async generators",
    classifiers=[
        "Development Status :: 6 - Mature",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python"
    ]
)
