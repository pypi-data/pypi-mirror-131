from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read().replace(".. include:: toc.rst\n\n", "")

# The lines below can be parsed by `docs/conf.py`.
name = "circuitdb"
version = "1.1.0"

setup(
    name=name,
    version=version,
    packages=[name,],
    install_requires=["logical~=0.3",],
    license="MIT",
    url="https://github.com/reity/circuitdb",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Data set of optimal circuits for Boolean functions "+\
                "that have low arity.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
