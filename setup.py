from setuptools import setup
long_description = """
hgtools
=======

hgtools builds on the setuptools_hg plugin for setuptools. hgtools
provides classes for inspecting and working with repositories in the
Mercurial version control system.

hgtools provides a plugin for setuptools that enables setuptools to find
files under the Mercurial version control system.

The classes provided by hgtools are designed to work natively with the
Mercurial Python libraries (in process) or fall back to using the
command-line program ``hg(1)`` if available. The command-line support is
especially useful inside virtualenvs
that don't have access to a system-wide installed Mercurial lib (i.e. when
the virtualenv was created with ``--no-site-packages``).

.. note:: The setuptools feature

  You can read about the setuptools plugin provided by hgtools in the
  `setuptools documentation`_. It basically returns a list of files that are
  under Mercurial version control when running the ``setup`` function, e.g. if
  you create a source and binary distribution. It's a simple yet effective way
  of not having to define package data (non-Python files) manually in MANIFEST
  templates (``MANIFEST.in``).

.. _setuptools documentation: http://peak.telecommunity.com/DevCenter/setuptools#adding-support-for-other-revision-control-systems

Usage
*****

Here's a simple example of a setup.py that uses hgtools::

    from setuptools import setup, find_packages
    setup(
        name="HelloWorld",
        version="0.1",
        packages=find_packages(),
        setup_requires=["hgtools"],
    )

If you run the setup.py above, setuptools will automatically download
hgtools to the directory where the setup.py is located at (and won't
install it anywhere else) to get all package data files from the
Mercurial repository.

Auto Version Numbering
**********************

With the 0.4 release, hgtools adds support for automatically generating
project version numbers from the mercurial repository in which the
project is developed.

To use this feature, your project must follow the following assumptions:

	 - Mercurial tags are used to indicate released versions.
	 - Tag names are specified as the version only (i.e. 0.1 and not
	   v0.1 or release-0.1)
	 - Released versions currently must conform to the StrictVersion in
	   distutils. Any tags that don't match this scheme will be ignored.
	   Future releases may relax this restriction.

Thereafter, you may use the HGToolsManager.get_current_version to
determine the version of the product. If the current revision is tagged
with a valid version, that version will be used. Otherwise, the tags in
the repo will be searched, the latest release will be found, and hgtools
will infer the upcoming release version.

For example, if the repo contains the tags 0.1, 0.2, and 0.3 and the
repo is not on any of those tags, get_current_version will return
'0.3.1dev' and get_current_version(increment='0.1') will return
'0.4dev'.

See the hgtools setup.py for an example of this technique.

Options
*******

Set the ``HGTOOLS_FORCE_CMD`` environment variable before running
setup.py if you want to enforce the use of the hg command (though it
will then fall back to the native libraries if the command is not
available or fails to run).
"""

try:
	# force cmd for now because some of the methods are not yet implemented
	#  in the library manager.
	import os; os.environ['HGTOOLS_FORCE_CMD'] = 'yes'
	from hgtools import get_manager
	mgr = get_manager()
	version = mgr.get_current_version(increment='0.1')
	tag_build = '' if mgr.get_tagged_version() else 'dev'
except Exception:
	version = None
	tag_build = None

setup(
    name="hgtools",
    version=version,
    author="Jannis Leidel/Jason R. Coombs",
    author_email="jaraco@jaraco.com",
    url="http://bitbucket.org/jaraco/hgtools/",
    download_url="http://bitbucket.org/jaraco/hgtools/downloads/",
    description="Classes and setuptools plugin for Mercurial repositories",
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
    py_modules=["hgtools"],
    entry_points = {
        "setuptools.file_finders": [
            "hg = hgtools:file_finder_plugin"
        ]
    },
    options = dict(
		egg_info = dict(
			tag_build = tag_build,
			),
		),
)
