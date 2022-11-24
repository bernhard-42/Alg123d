from setuptools import setup, find_packages

setup_args = {
    "name": "alg123d",
    "version": "0.1.0",
    "description": "Algebraic 3D CAD",
    "long_description": "A system to create CAD objects in an algebraic way",
    "include_package_data": True,
    "python_requires": ">=3.8",
    "install_requires": [],
    "packages": find_packages(),
    "zip_safe": False,
    "author": "Bernhard Walter",
    "author_email": "b_walter@arcor.de",
    "url": "https://github.com/bernhard-42/py123d",
    "keywords": ["CAD", "cadquery"],
    "classifiers": [
        "Development Status :: 3 - Alpha",
        "Framework :: IPython",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Multimedia :: Graphics",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
}

setup(**setup_args)
