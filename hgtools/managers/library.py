from __future__ import absolute_import

import os
import sys
import io
import collections
import contextlib

from . import base
from . import cmd

try:
	import mercurial.__version__
	import mercurial.dispatch
except ImportError:
	pass
except Exception:
	pass

SavedIO = collections.namedtuple('SavedIO', 'stdout stderr')

@contextlib.contextmanager
def capture_stdio():
	sys_stdout, sys.stdout = sys.stdout, io.BytesIO()
	sys_stderr, sys.stderr = sys.stderr, io.BytesIO()
	try:
		yield SavedIO(sys.stdout, sys.stderr)
	finally:
		sys.stdout = sys_stdout
		sys.stderr = sys.stderr

@contextlib.contextmanager
def replace_sysargv(params):
	sys_argv, sys.argv = sys.argv, params
	try:
		yield
	finally:
		sys.argv = sys.argv

class Result(object):
	pass

@contextlib.contextmanager
def capture_system_exit():
	res = Result()
	try:
		yield res
		res.code = 0
	except SystemExit as e:
		if isinstance(e.code, int):
			res.code = e.code
		else:
			res.code = 1
	except Exception:
		res.code = 1
		raise

class ProcessResult(object):
	pass

@contextlib.contextmanager
def in_process_context(params):
	res = ProcessResult()
	with capture_stdio() as stdio, replace_sysargv(params), capture_system_exit() as proc_res:
		yield res
	res.stdio = stdio
	res.returncode = proc_res.code

class LibraryManager(cmd.Command, base.HGRepoManager):
	"""
	An HGRepoManager implemented by invoking the hg command in-process.
	"""

	def _run_hg(self, *params):
		"""
		Run the hg command in-process with the supplied params.
		"""
		cmd = [self.exe, '-R', self.location] + list(params)
		with in_process_context(cmd) as result:
			mercurial.dispatch.run()
		stdout = result.stdio.stdout.getvalue()
		stderr = result.stdio.stderr.getvalue()
		if not result.returncode == 0:
			raise RuntimeError(stderr.strip() or stdout.strip())
		return stdout.decode('utf-8')
