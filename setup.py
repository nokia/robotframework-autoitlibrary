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

from setuptools      import setup
from setuptools.command.install import install
from sysconfig import get_path
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

class InstallCommand(install):
    def initialize_options(self):
        install.initialize_options(self)

    def finalize_options(self):
        install.finalize_options(self)

    def run(self):
        if os.name != "nt" :
            print("AutoItLibrary cannot be installed on non-Windows platforms.")
            sys.exit(2)
        RegisterAutoIT()
        install.run(self)

def RegisterAutoIT():
    #
    # Install and register AutoItX
    #
    print("[INF] In RegisterAutoIT with params " + " ".join(str(x) for x in sys.argv))
    
    if os.path.isfile(os.path.join(get_path('platlib'), "AutoItLibrary/lib/AutoItX3.dll")) :
        print("[INF] Don't think we need to unregister the old one...")

    instDir = os.path.normpath(os.path.join(get_path('platlib'), "AutoItLibrary/lib"))
    if not os.path.isdir(instDir) :
        os.makedirs(instDir)
    instFile = os.path.normpath(os.path.join(instDir, "AutoItX3.dll"))
    if "32bit" in platform.architecture()[0] :
        print("[INF] Here is from 32bit OS")
        shutil.copyfile("3rdPartyTools/AutoIt/AutoItX3.dll", instFile)
    else :
        shutil.copyfile("3rdPartyTools/AutoIt/lib64/AutoItX3.dll", instFile)
    #
    # Register the AutoItX COM object
    # and make its methods known to Python
    #
    cmd = r"%SYSTEMROOT%\system32\regsvr32.exe /S " + '\"' + instFile + '\"'
    print(cmd)
    subprocess.check_call(cmd, shell=True) 

def getWin32ComRomingPath():
    for dirpath, dirs, files in os.walk(os.getenv('APPDATA')):
        for filename in files:
            if filename == "makepy.py" and (r'site-packages\win32com\client' in dirpath):
                fullpath = os.path.join(dirpath, filename)
                print("[INF] Found :", fullpath)
                return fullpath
    return None

if __name__ == "__main__":
    #
    # Figure out the install path
    #
    root_path = os.path.join(os.getenv("HOMEDRIVE"))
    if root_path != "C:":
        print("[INF] root path (%s) != C:" % root_path)
        root_path = "C:"
    destPath = os.path.normpath(os.path.join(root_path, r"\RobotFramework\Extensions\AutoItLibrary"))
    #
    # Do the distutils installation
    #
    setup(name         = "robotframework-autoitlibrary",
          version      = "1.2.8",
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
          cmdclass     = {'install': InstallCommand},
          install_requires = ['robotframework', 'pywin32', 'pillow'],
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
