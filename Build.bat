@echo off
::
:: Batch file to build the AutoItLibrary extesnsion for Robot Framework
::
:: Copyright (c) 2008-2009 Texas Instruments, Inc.
:: Author: Martin Taylor <cmtaylor@ti.com>
::
::  Licensed under the Apache License, Version 2.0 (the "License");
::  you may not use this file except in compliance with the License.
::  You may obtain a copy of the License at
::
::      http://www.apache.org/licenses/LICENSE-2.0
::
::  Unless required by applicable law or agreed to in writing, software
::  distributed under the License is distributed on an "AS IS" BASIS,
::  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
::  See the License for the specific language governing permissions and
::  limitations under the License.
::
::-------------------------------------------------------------------------------
::
:: Build the AutoItLibrary installer
::
IF EXIST .\dist   rmdir /S /Q .\dist
IF EXIST .\build  rmdir /S /Q .\build
call Make.bat
python setup.py sdist --format=zip
pause
::
:: -------------------------------- End of file --------------------------------
