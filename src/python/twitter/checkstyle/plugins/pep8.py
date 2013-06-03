from __future__ import absolute_import

from ..common import (
    CheckstylePlugin,
    Nit,
    PythonFile)

import pep8


class PEP8Error(Nit):
  def __init__(self, python_file, code, line_number, offset, text, doc):
    super(PEP8Error, self).__init__(code, Nit.ERROR, python_file, text, line_number)


class TwitterReporter(pep8.BaseReport):
  def init_file(self, filename, lines, expected, line_offset):
    super(TwitterReporter, self).init_file(filename, lines, expected, line_offset)
    self._python_file = PythonFile.parse(filename)
    self._twitter_errors = []

  def error(self, line_number, offset, text, check):
    code = super(TwitterReporter, self).error(line_number, offset, text, check)
    if code:
      self._twitter_errors.append(
          PEP8Error(self._python_file, code, line_number, offset, text[5:], check.__doc__))
    return code

  @property
  def twitter_errors(self):
    return self._twitter_errors


IGNORE_CODES = (
  # continuation_line_indentation
  'E121',
  'E124',
  'E125',
  'E127',
  'E128',

  # imports_on_separate_lines
  'E401',

  # indentation
  'E111',

  # trailing_whitespace
  'W291',
  'W293'
)


class PEP8Checker(CheckstylePlugin):
  STYLE_GUIDE = pep8.StyleGuide(
      max_line_length=100,
      verbose=False,
      reporter=TwitterReporter,
      ignore=IGNORE_CODES)

  def nits(self):
    report = self.STYLE_GUIDE.check_files([self.python_file.filename])
    return report.twitter_errors
