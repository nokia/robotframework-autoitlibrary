"""
Package: robotframework-AutoItLibrary
Module:  AutoItLibrary Installation Module
Purpose: This is a Python "Distutils" setup program used to build installers for and to install the
         robotframework-AutoItLibrary.

         Copyright (c) 2008-2010 Texas Instruments, Inc.

         Licensed under the Apache License, Version 2.0 (the "License");
         you may not use this file except in compliance with the License.
         You may obtain a copy of the License at

             http://www.apache.org/licenses/LICENSE-2.0

         Unless required by applicable law or agreed to in writing, software
         distributed under the License is distributed on an "AS IS" BASIS,
         WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
         See the License for the specific language governing permissions and
         limitations under the License.
"""
__author__  = "Martin Taylor <cmtaylor@ti.com>"

from distutils.core      import setup
from distutils.sysconfig import get_python_lib
import sys
import os
import shutil
import subprocess
import platform

CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: Microsoft :: Windows
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

DESCRIPTION = """
AutoItLibrary is a Robot Framework keyword library wrapper for for the
freeware AutoIt tool (http://www.autoitscript.com/autoit3/index.shtml)
using AutoIt's AutoItX.dll COM object. The AutoItLibrary class
provides a proxy for the AutoIt keywords callable on the AutoIt COM
object and provides additional high-level keywords implemented as
methods in this class.
"""[1:-1]

if __name__ == "__main__":
    #
    # Install the 3rd party packages
    #
    if sys.argv[1].lower() == "install" :
        if os.name == "nt" :
            #
            # Install and register AutoItX
            #
            if os.path.isfile(os.path.join(get_python_lib(), "AutoItLibrary/lib/AutoItX3.dll")) :
                print("Don't think we need to unregister the old one...")

            instDir = os.path.normpath(os.path.join(get_python_lib(), "AutoItLibrary/lib"))
            if not os.path.isdir(instDir) :
                os.makedirs(instDir)
            instFile = os.path.normpath(os.path.join(instDir, "AutoItX3.dll"))
            if "32bit" in platform.architecture()[0] :
                print("Here is from 32bit OS")
                shutil.copyfile("3rdPartyTools/AutoIt/AutoItX3.dll", instFile)
            else :
                shutil.copyfile("3rdPartyTools/AutoIt/lib64/AutoItX3.dll", instFile)
            #
            # Register the AutoItX COM object
            # and make its methods known to Python
            #
            cmd = r"%SYSTEMROOT%\system32\regsvr32.exe /S " + instFile
            print(cmd)
            subprocess.check_call(cmd, shell=True)
            makepy = os.path.normpath(os.path.join(get_python_lib(), "win32com/client/makepy.py"))
            #
            # Make sure we have win32com installed
            #
            if not os.path.isfile(makepy) :
                print("AutoItLibrary requires win32com. See http://starship.python.net/crew/mhammond/win32/.")
                sys.exit(2)

            cmd = "python %s %s" % (makepy, instFile)
            print(cmd)
            subprocess.check_call(cmd)
        else :
            print("AutoItLibrary cannot be installed on non-Windows platforms.")
            sys.exit(2)
    #
    # Figure out the install path
    #
    destPath = os.path.normpath(os.path.join(os.getenv("HOMEDRIVE"), r"\RobotFramework\Extensions\AutoItLibrary"))
    #
    # Do the distutils installation
    #
    setup(name         = "robotframework-autoitlibrary",
          version      = "1.2.5",
          description  = "AutoItLibrary for Robot Framework",
          author       = "Joe Hisaishi",
          author_email = "joehisaishi1943@gmail.com",
          url          = "https://github.com/nokia/robotframework-autoitlibrary",
          license      = "Apache License 2.0",
          platforms    = "Microsoft Windows",
          classifiers  = CLASSIFIERS.splitlines(),
          long_description = DESCRIPTION,
          package_dir  = {'' : "src"},
          packages     = ["AutoItLibrary"],
          install_requires = ['pywin32', 'pillow'],
          data_files   = [(destPath,
                             ["COPYRIGHT.txt",
                              "LICENSE.txt",
                              "doc/AutoItLibrary.html",
                              "3rdPartyTools/AutoIt/Au3Info.exe",
                              "3rdPartyTools/AutoIt/AutoItX.chm",
                              "3rdPartyTools/AutoIt/AutoIt_License.html",
                              "3rdPartyTools/AutoIt/AutoItX3.dll",
                              "3rdPartyTools/AutoIt/lib64/AutoItX3.dll",
                             ]),
                           (os.path.join(destPath, "tests"),
                             ["tests/CalculatorGUIMap.py",
                              "tests/__init__.html",
                              "tests/Calculator_Test_Cases.html",
                              "tests/RobotIDE.bat",
                              "tests/RunTests.bat"
                             ]),
                         ]
         )
#
# -------------------------------- End of file --------------------------------
