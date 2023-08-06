# MIT License

# Copyright (c) 2021 Ben Tettmar

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from distutils.core import setup

readme = """
brainfuckery
============

The simplest and easiest to use Brainfuck interpreter in Python.

Install
~~~~~~~

::

   pip install brainfuckery

Examples
~~~~~~~~

Converting text to brainfuck code.

.. code:: python

   from brainfuckery import Brainfuckery

   textToConvert = input("text: ")
   result = Brainfuckery().convert(textToConvert)

   print(result)

Interpret brainfuck code/convert brainfuck to text

.. code:: python

   from brainfuckery import Brainfuckery

   codeToInterpret = input("code: ")
   result = Brainfuckery().interpret(codeToInterpret)

   print(result)

"""

setup(
  name = 'brainfuckery',
  packages = ['brainfuckery'],
  version = '1.0.1',
  license='MIT',
  description = 'The simplest and easiest to use Brainfuck interpreter in Python.',
  long_description_content_type="text/markdown",
  long_description=readme,
  author = 'Ben Tettmar',
  author_email = 'hello@benny.fun',
  keywords = ["brainfuck", "brainfuck interpreter", "brainfuck.py", "brainfuckery", "brainfuck generator", "brainfuck generator in python", "text to brainfuck", "text to brainfuck code", "execute brainfuck code", "convert text to brainfuck"]
)