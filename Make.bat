@echo off
::
:: Batch file to make the AutoItLibrary extesnsion for Robot Framework
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
:: Install the AutoItLibrary on the local PC
::
python setup.py install
::
:: Build the updated documentation before installing again
::
libdoc.py --output doc\AutoItLibrary.html AutoItLibrary
::
:: Now install the AutoItLibrary on the local PC including the updated documentation
::
python setup.py install
pause
::
:: -------------------------------- End of file --------------------------------
