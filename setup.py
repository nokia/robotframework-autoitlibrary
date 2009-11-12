"""
Package: robotframework-AutoItLibrary
Module:  AutoItLibrary Installation Module
Purpose: This is a Python "Distutils" setup program used to build installers for and to install the
         robotframework-AutoItLibrary.

         Copyright (c) 2008-2009 Texas Instruments, Inc.

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
            # Install AutoItX if not already installed
            #
            if not os.path.isfile(os.path.join(get_python_lib(), "AutoItLibrary/lib/AutoItX3.dll")) :
                instDir = os.path.normpath(os.path.join(get_python_lib(), "AutoItLibrary/lib"))
                if not os.path.isdir(instDir) :
                    os.makedirs(instDir)
                instFile = os.path.normpath(os.path.join(instDir, "AutoItX3.dll"))
                shutil.copyfile("3rdPartyTools/AutoIt/AutoItX3.dll", instFile)
                #
                # Register the AutoItX COM object
                # and make its methods known to Python
                #
                cmd = r"C:\WINDOWS\system32\regsvr32.exe /S %s" % instFile
                print cmd
                subprocess.check_call(cmd)
                makepy = os.path.normpath(os.path.join(get_python_lib(), "win32com/client/makepy.py"))
                cmd = "python %s %s" % (makepy, instFile)
                print cmd
                subprocess.check_call(cmd)
            #
            # Install PIL if it is not already installed
            #
            if not os.path.exists(os.path.join(get_python_lib(), "PIL")) :
                print "Installing PIL, please accept all defaults"
                subprocess.check_call(r"3rdPartyTools\PIL\PIL-1.1.6.win32-py2.5.exe")
        else :
            print "AutoIt cannot be installed on non-Windows platforms."
            sys.exit(2)
    #
    # Do the distutils installation
    #
    setup(name         = "AutoItLibrary",
          version      = "1.0",
          description  = "AutoItLibrary for Robot Framework",
          author       = "Martin Taylor",
          author_email = "cmtaylor@ti.com",
          url          = "http://code.google.com/p/robotframework-autoitlibrary/",
          license      = "Apache License 2.0",
          platforms    = "Microsoft Windows",
          classifiers  = CLASSIFIERS.splitlines(),
          long_description = DESCRIPTION,
          package_dir  = {'' : "src"},
          packages     = ["AutoItLibrary"],
          data_files   = [(r"C:\RobotFramework\Extensions\AutoItLibrary",
                             ["ReadMe.txt",
                              "COPYRIGHT.txt",
                              "LICENSE.txt",
                              "doc/AutoItLibrary.html",
                              "3rdPartyTools/AutoIt/Au3Info.exe",
                              "3rdPartyTools/AutoIt/AutoItX.chm",
                              "3rdPartyTools/AutoIt/AutoIt_License.html",
                              "3rdPartyTools/PIL/PIL_License.html",
                             ]),
                           (r"C:\RobotFramework\Extensions\AutoItLibrary\tests",
                             ["tests/CalculatorGUIMap.py",
                              "tests/Calculator_Test_Cases.html",
                              "tests/RobotIDE.bat",
                              "tests/RunTests.bat"
                             ]),
                         ]
         )
#
# -------------------------------- End of file --------------------------------
