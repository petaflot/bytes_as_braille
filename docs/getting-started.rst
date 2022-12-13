Getting started
===============

Installation
------------

The usual way is to use pip:

.. code:: shell

    pip install bytes_as_braille

Don't forget to add this to our app's dependencies.

To use input method:

.. code:: shell

    pip install readchar

If you want colored output, install truecolor:

.. code:: shell

    pip install truecolor

Usage
-----

.. code:: python

    from bytes_as_braille import *

//Command Line usage
//~~~~~~~~~~~~~~~~~~
//
//.. versionadded:: 0.7beta4
//
//This library also includes a cli app for quickly generating barcodes from the command
//line or from shell scripts:
//
//.. code:: console
//
//    $ # Save a barcode to outfile.svg:
//    $ python-barcode create "123456789000" outfile -b ean --text "text to appear under barcode"
//    $ # Generate a PNG (Require Pillow):
//    $ python-barcode create -t png "My Text" outfile
//    $ python-barcode --help
//    usage: python-barcode [-h] [-v] {create,list} ...
//
//    Create standard barcodes via cli.
//
//    optional arguments:
//      -h, --help     show this help message and exit
//      -v, --version  show program's version number and exit
//
//    Actions:
//      {create,list}
//        create       Create a barcode with the given options.
//        list         List available image and code types.
//
//    Image output enabled, use --type option to give image format (png, jpeg, ...).
//    $
