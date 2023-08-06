import os

from setuptools import setup


def get_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, "times2/version.py")) as f:
        variables = {}
        exec(f.read(), variables)
        return variables.get("VERSION")
    raise RuntimeError("No version info found.")


setup(
    name="times2",
    version=get_version(),
    url="https://github.com/marcinn/times2",
    license="BSD",
    author="Marcin Nowak, Vincent Driessen",
    author_email="marcin.j.nowak@gmail.com",
    description="Times2 is a small, minimalistic, Python library for dealing "
    "with time conversions between universal time and arbitrary "
    "timezones.",
    long_description=__doc__,
    packages=["times2"],
    install_requires=["pytz", "python-dateutil", "arrow>=0.14.0,<1.0", "six"],
    include_package_data=True,
    zip_safe=False,
    platforms="any",
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        #'Development Status :: 1 - Planning',
        #'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        "Development Status :: 4 - Beta",
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: No Input/Output (Daemon)",
        "Environment :: Other Environment",
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Environment :: Win32 (MS Windows)",
        "Framework :: Buildout",
        "Framework :: CherryPy",
        "Framework :: Django",
        "Framework :: Plone",
        "Framework :: Pylons",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: System",
        "Topic :: Terminals",
        "Topic :: Utilities",
    ],
)
