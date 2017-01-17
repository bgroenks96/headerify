import textwrap

class CStyleProcessor:
  def headerify(self, inputstr):
    header = "/*\n"
    for line in inputstr.splitlines(True):
      for wrapped in textwrap.wrap(line, 80, expand_tabs=False, drop_whitespace=False, replace_whitespace=False):
        header += " * " + wrapped.strip() + "\n"
    header += " */"
    return header
