#!/usr/bin/env python3

## Gate test: opening a project with nonexistent file paths must not raise.
# Covers the checkTimestamp FileNotFoundError crash (commit 89a9ae5).
# A missing file's timestamp is legitimately absent, not exceptional.

import os
import sys

sys.path.insert(0, "lib")

from libdbr import fileinfo


def test_checkTimestamp_missing_path_returns_none():
  """checkTimestamp on a nonexistent path must return (None, False), not raise."""
  ts, changed = fileinfo.checkTimestamp("/nonexistent/path/that/does/not/exist")
  assert ts is None, "Expected None timestamp for missing path, got {}".format(ts)
  assert changed is False, "Expected False changed flag for missing path"


def test_checkTimestamp_existing_path_returns_timestamp():
  """checkTimestamp on an existing path must return a real mtime."""
  import tempfile
  with tempfile.NamedTemporaryFile(delete=False) as f:
    path = f.name
  try:
    ts, changed = fileinfo.checkTimestamp(path)
    assert ts is not None, "Expected real timestamp for existing file, got None"
    assert isinstance(ts, float), "Expected float mtime, got {}".format(type(ts))
  finally:
    os.unlink(path)


def test_checkTimestamp_missing_then_existing_no_crash():
  """Mixing missing and existing paths must not raise on either."""
  ts1, _ = fileinfo.checkTimestamp("/nonexistent/missing")
  assert ts1 is None
  import tempfile
  with tempfile.NamedTemporaryFile(delete=False) as f:
    real_path = f.name
  try:
    ts2, _ = fileinfo.checkTimestamp(real_path)
    assert ts2 is not None
  finally:
    os.unlink(real_path)


if __name__ == "__main__":
  test_checkTimestamp_missing_path_returns_none()
  test_checkTimestamp_existing_path_returns_timestamp()
  test_checkTimestamp_missing_then_existing_no_crash()
  print("All tests passed.")
