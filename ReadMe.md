AutoItLibrary
=============
[![Latest Version](https://img.shields.io/pypi/v/robotframework-autoitlibrary.svg)](https://pypi.python.org/pypi/robotframework-autoitlibrary)

Changelog：
  2020/09/28 Return PID of the launched application using "Run" keyword
  2018/06/29 Added Python 3 support

Introduction
------------

AutoItLibrary is a Python keyword library that extends [Robot Framework](http://code.google.com/p/robotframework/) by providing keywords based on the COM interface to [AutoIt](http://www.autoitscript.com/autoit3/index.shtml). AutoIt is a freeware tool for automating the Windows GUI.

In order to do screenshots, the AutoItLibrary uses the PIL ([Python
Image Library](http://www.pythonware.com/products/pil/)).


Installation
------------
Make sure you run the installation command with administrative privilages.

#### pip install
   
```pip install robotframework-autoitlibrary```


#### source install
AutoItLibrary installs its own file and, if not already present, the 3rd party
AutoIt and PIL tools.  To install, unzip the release file into a temporary
directory on your PC, open a command window in that directory and type:

    python setup.py install

This installation creates the folder:

    RobotFramework\Extensions\AutoItLibrary

on your PC and puts various files into this directory folder.

When installed using pip this folder is placed in the Lib/site-packages folder of your python install.
However, if installed from source, this folder will be placed in the C:\ drive of your machine.


Documentation
-------------

AutoItLibrary documentation is installed by the installation process into:

    C:\RobotFramework\Extensions\AutoItLibrary\AutoItLibrary.html

The AutoItX documentation is also installed into this folder as AutoItX.chm.


Tests
-----

The AutoItLibrary installer puts a suite of self-tests here:

    C:\RobotFramework\Extensions\AutoItLibrary\tests

To run these tests, which exercise the Windows Calculator GUI, run the
RunTests.bat file in the above folder.

Note: Windows 10 Calculator is not supported.
