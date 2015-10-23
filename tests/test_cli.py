from __future__ import print_function
import io
import sys

import gr1py
from gr1py import cli


def test_version():
    baitandswitch = io.StringIO()
    stdout_cache = sys.stdout
    sys.stdout = baitandswitch
    assert cli.main(args=['gr1py', '-V']) == 0
    sys.stdout = stdout_cache
    (progname, ver) = baitandswitch.getvalue().split()
    assert progname == 'gr1py'
    assert gr1py.__version__ == ver
    assert ('dev0' not in ver) and ('Unknown' not in ver)
