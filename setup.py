import io
import os
import re

from setuptools import find_packages, setup


###############################################################################

NAME = "aturtle"
PACKAGES = find_packages(where="src")
META_PATH = os.path.join("src", NAME, "__init__.py")
KEYWORDS = ["functions", "boilerplate"]
CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Framework :: AsyncIO",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Topic :: Education",
    "Topic :: Games/Entertainment",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
INSTALL_REQUIRES = [
]
EXTRAS_REQUIRE = {
    "pillow": [
        "pillow",
    ],
    "tests": [
        "coverage",
        "pylint",
        "hypothesis",
    ],
    "docs": [],
}
EXTRAS_REQUIRE["dev"] = [
    requirement
    for requirements in EXTRAS_REQUIRE.values()
    for requirement in requirements
]

###############################################################################

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with io.open(os.path.join(HERE, *parts), encoding="utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


VERSION = find_meta("version")
URI = find_meta("uri")
LONG = read("README.rst")


if __name__ == "__main__":
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=URI,
        version=VERSION,
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        long_description=LONG,
        packages=PACKAGES,
        package_dir={"": "src"},
        zip_safe=False,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
    )
