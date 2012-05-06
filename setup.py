# -*- coding: UTF-8 -*-

"""
Setup script for building hgtools distribution

Copyright © 2010-2011 Jason R. Coombs
"""

import setuptools
long_description = open('README').read()

# HGTools uses a special technique for getting the version from
#  mercurial, because it can't require itself to install itself.
# Don't use this technique in your project. Instead, follow the
#  directions in the README or see jaraco.util for an example.
from hgtools.plugins import calculate_version, patch_egg_info
patch_egg_info(force_hg_version=True)

setup_params = dict(
	name="hgtools",
	version=calculate_version(options=dict(increment='0.0.1')),
	author="Jannis Leidel/Jason R. Coombs",
	author_email="jaraco@jaraco.com",
	url="http://bitbucket.org/jaraco/hgtools/",
	download_url="http://bitbucket.org/jaraco/hgtools/downloads/",
	description="Classes and setuptools plugin for Mercurial repositories",
	long_description=long_description,
	license="GPL2",
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 3",
		"Intended Audience :: Developers",
		"Operating System :: OS Independent",
		"License :: OSI Approved :: GNU General Public License (GPL)",
		"Topic :: Software Development :: Version Control",
		"Framework :: Setuptools Plugin",
	],
	packages=setuptools.find_packages(),
	entry_points = {
		"setuptools.file_finders": [
			"hg = hgtools.plugins:file_finder"
		],
		"distutils.setup_keywords": [
			"use_hg_version = hgtools.plugins:version_calc",
		],
	},
	use_2to3=True,
)

if __name__ == '__main__':
	setuptools.setup(**setup_params)
