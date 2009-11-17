"""
Package: AutoItLibrary
Module:  Test
Purpose: This is a Robot Framework variable file according to the specifications provided here:
         http://robotframework.googlecode.com/svn/tags/robotframework-2.1/doc/userguide/RobotFrameworkUserGuide.html#variable-files
         It defines a Python dictionary variable "GUIMAP" that is used by the AutoItLibrary Robot
         Framework tests to map useful Windows Calculator GUI object names (such as the keypad keys) to
         their underlying Windows GUI object names required by AutoIt.

         Copyright (c) 2009 Texas Instruments

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
__version__ = "1.0"

GUIMAP = {"0" : "Button45",
          "1" : "Button44",
          "2" : "Button49",
          "3" : "Button54",
          "4" : "Button43",
          "5" : "Button48",
          "6" : "Button53",
          "7" : "Button42",
          "8" : "Button47",
          "9" : "Button52",
          "/" : "Button57",
          "*" : "Button58",
          "-" : "Button59",
          "+" : "Button60",
          "=" : "Button65",

          "Hex" : "Button5",
          "Dec" : "Button6",
          "Oct" : "Button7",
          "Bin" : "Button8",

          "Qword" : "Button14",
          "Dword" : "Button15",
          "Word"  : "Button16",
          "Byte"  : "Button17",

          "C"     : "Button74",
          "Clear" : "Button74",
         }
#
# Map application-specific names of menu items to the sequence of
# ALT keys used to access these menu items, since the Windows Calculator
# doesn't really use a "Menu" GUI object to implement its menus
# and AutoIt can't see these as GUI objects.
#
MENUMAP = {"View Standard"       : "VT",
           "View Scientific"     : "VS",
           "View Decimal"        : "VD",
           "View Hex"            : "VH",
           "View Digit grouping" : "VI",
           "Edit Copy"           : "EC",
           "Edit Paste"          : "EP",
           "Exit"                : "{F4}"
          }
#
# -------------------------------- End of file --------------------------------
