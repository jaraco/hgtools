from setuptools import setup

long_description = """
setuptools_hg
=============

setuptools_hg is a plugin for setuptools that enables setuptools to find files
under the Mercurial version control system.

It uses the Mercurial Python library by default and falls back to use the
command line programm ``hg(1)``. That's especially useful inside virtualenvs
that don't have access to the system wide installed Mercurial lib (e.g. when
created with ``--no-site-packages``).

.. note:: The setuptools feature

  You can read about the hooks used by setuptool_hg in the
  `setuptools documentation`_. It basically returns a list of files that are
  under Mercurial version control when running the ``setup`` function, e.g. if
  you create a source and binary distribution. It's a simple yet effective way
  of not having to define package data (non-Python files) manually in MANIFEST
  templates (``MANIFEST.in``).

.. _setuptools documentation: http://peak.telecommunity.com/DevCenter/setuptools#adding-support-for-other-revision-control-systems

Usage
*****

Here's an example of a setup.py that uses setuptools_hg::

    from setuptools import setup, find_packages
    setup(
        name="HelloWorld",
        version="0.1",
        packages=find_packages(),
        setup_requires=["setuptools_hg"],
    )

If you run this setup.py setuptools will automatically download setuptools_hg
to the directory where the setup.py is located at (and won't install it
anywhere else) to get all package data files from the Mercurial repository.

Options
*******

Set the ``HG_SETUPTOOLS_FORCE_CMD`` environment variable before running
setup.py if you want to enforce the use of the hg command.
"""

setup(
    name="setuptools_hg",
    version='0.3',
    author="Jannis Leidel",
    author_email="jannis@leidel.info",
    url="http://bitbucket.org/jezdez/setuptools_hg/",
    download_url="http://bitbucket.org/jezdez/setuptools_hg/downloads/",
    description="Setuptools plugin for finding files under Mercurial version control.",
    long_description=long_description,
    license="GPL2",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Topic :: Software Development :: Version Control",
        "Framework :: Setuptools Plugin",
    ],
    py_modules=["setuptools_hg"],
    entry_points = {
        "setuptools.file_finders": [
            "hg = setuptools_hg:hg_file_finder"
        ]
    }
)
