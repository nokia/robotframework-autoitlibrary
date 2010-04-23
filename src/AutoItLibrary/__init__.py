"""
Package: robotframework-AutoItLibrary
Module:  AutoItLibrary
Purpose: Provides a Robot Framework keyword wrapper for the freeware AutoIt tool
         (http://www.autoitscript.com/autoit3/index.shtml) via AutoIt's AutoItX.dll COM object.

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
__version__ = "1.1"
#
# Import the libraries we need
#
import win32com.client                  # For COM interface to AutoIt
import sys                              # For command line args
import os                               # For file path manipulation
import types
import Logger
import Counter
try :
    import ImageGrab                    # For screen capture via Python Image Library (PIL)
except :
    ImageGrab = None
#
#-------------------------------------------------------------------------------
#
class AutoItLibrary(Logger.Logger, Counter.Counter) :
    """
    *AutoItLibrary* is a Robot Framework keyword library wrapper for for the freeware *AutoIt* tool
    (http://www.autoitscript.com/autoit3/index.shtml) using AutoIt's *AutoItX.dll* COM object. The
    *AutoItLibrary* class provides a proxy for the AutoIt keywords callable on the AutoIt COM object and
    provides additional high-level keywords implemented as methods in this class.

    In the following documentation on each keyword, the keywords whose documentation is simply
    _method <KeywordName>_ (e.g. "_method ControlClick_") are the native AutoIt keywords.  The detailed
    documentation for these keywords is available in the AutoItX documentation file:
    *AutoItX.chm*.  This file is installed as part of the installation of *AutoItLibrary* as:

        C:\RobotFramework\Extensions\AutoItLibrary\AutoItX.chm

    In order to discover the control identifiers in a given Windows GUI, AutoIt provides a standalone
    tool called the AutoIt Window Info Tool which is installed as part of the installation of
    *AutoItLibrary* as:

        C:\RobotFramework\Extensions\AutoItLibrary\Au3Info.exe

    This tool is documented here: http://www.autoitscript.com/autoit3/docs/intro/au3spy.htm
    """

    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self, OutputDir=".", TimeOut=60, CaptureScreenOnError=False) :
        """
        | OutputDir=<path>          | Output directory for captured screenshots. Should set to _${OUTPUTDIR}_ |
        | Timeout=<seconds>         | Default TimeOut value in seconds.                                       |
        |                           | This is used in other methods when their TimeOut parameter is not used. |
        | CaptureScreenOnError=True | Defaults to False.  Set to _${True}_ to capture the PC screen on any    |
        |                           | AutoItLibrary keyword failure.                                          |
        """
        #
        # Call super.__init__ for the Counter class
        #
        Counter.Counter.__init__(self)
        #
        # Make a connection to the AutoIt COM object
        #
        self._AutoIt = win32com.client.Dispatch("AutoItX3.Control")
        #
        # Remember our input parameters
        #
        self._OutputDir  = OutputDir
        self._TimeOut    = int(TimeOut)
        self._CaptureScreenOnError = CaptureScreenOnError
        #
        # Check that PIL is installed if CaptureScreenOnError is True
        #
        if self._CaptureScreenOnError and ImageGrab == None :
            self._warn("Python Imaging Library (PIL) is not installed, but is required for CaptureScreenOnError... set False")
            self._CaptureScreenOnError = False
        #
        # Set other properties
        #
        self._my_kws     = None
        self._AutoIt_kws = None
        #
        # Log our versions
        #
        self._info("AutoIt: Running %s" % (self.GetVersion()))
        self._info("AutoIt: Running %s" % (self.GetAutoItVersion()))
    #
    #-------------------------------------------------------------------------------
    #
    def __getattr__(self, Name) :
        """
        This bit of "Magic" makes all the AutoItX COM object methods appear as if they were methods of
        the AutoItLibrary class.  It relies on the fact that the AutoItLibrary installer ran the
        win32com/client/makepy.py program on the AutoItX3.dll COM file in order to make the COM methods
        visible to Python.  This tool is documented here:
            http://docs.activestate.com/activepython/2.6/pywin32/html/com/win32com/HTML/QuickStartClientCom.html
        and here:
            http://docs.activestate.com/activepython/2.6/pywin32/html/com/win32com/HTML/GeneratedSupport.html
        """
        if Name in self.__get_AutoIt_keywords() :
            retAttr = getattr(self._AutoIt, Name)
            return retAttr
        else :
            raise AttributeError(Name)
    #
    #-------------------------------------------------------------------------------
    #
    def __get_my_keywords(self):
        """
        Get the keywords implemented by the AutoItLibrary class.
        """
        if self._my_kws is None :
            self._my_kws = [ name for name in dir(self)
                              if not name.startswith('_') and name != 'get_keyword_names'
                              and type(getattr(self, name)) is types.MethodType ]
        return self._my_kws
    #
    #-------------------------------------------------------------------------------
    #
    def __get_AutoIt_keywords(self):
        """
        Get the keywords implemented by the underlying AutoItX COM object.
        """
        if self._AutoIt_kws is None:
            self._AutoIt_kws = [ name for name in dir(self._AutoIt)
                               if not name.startswith('_')
                               and not name.lower() == "sleep"      # Don't include AutoIt's sleep method
                               and type(getattr(self._AutoIt, name)) is types.MethodType ]
        return self._AutoIt_kws
    #
    #-------------------------------------------------------------------------------
    #
    def get_keyword_names(self) :
        """
        Return the list of keyword methods supported by this Robot Framework Test Engine which are its
        own native keywords plus the AutoIt keywords.
        """
        return self.__get_my_keywords() + self.__get_AutoIt_keywords()
    #
    #-------------------------------------------------------------------------------
    #
    def GetVersion(self):
        """
        Returns a string with the version of the AutoItLibrary.
        """
        strVersion = "File: %s, Version: %s" % (__file__, __version__)
        return strVersion
    #
    #-------------------------------------------------------------------------------
    #
    def GetAutoItVersion(self) :
        """
        Returns a string with the version of the AutoItX COM object.
        """
        return "AutoItX %s (COM object)" % self._AutoIt.version
    #
    #-------------------------------------------------------------------------------
    #
    def GetActiveWindowImage(self, FilePath) :
        """
        Capture an image of the active window into the given _FilePath_.
        The given _FilePath_ must be relative to Robot Framework output directory,
        otherwise the embedded image will not be shown in the log file.
        """
        #
        # Check that PIL is installed
        #
        if ImageGrab == None :
            raise RuntimeError("Python Imaging Library (PIL) is not installed, but is required for GetActiveWindowImage")
        #
        # Check for a valid FilePath and make sure the directories exist
        #
        if FilePath and os.path.isabs(FilePath):
            raise RuntimeError("Given FilePath='%s' must be relative to Robot outpudir" % FilePath)
        fullFilePath = os.path.join(self._OutputDir, FilePath)
        if not os.path.exists(os.path.split(fullFilePath)[0]):
            os.makedirs(os.path.split(fullFilePath)[0])
        self._info("GetActiveWindowImage(FilePath=%s)" % fullFilePath)
        #
        # Get the bounding box for the Active Window
        #
        x = self._AutoIt.WinGetPosX("")
        y = self._AutoIt.WinGetPosY("")
        width  = self._AutoIt.WinGetPosWidth("")
        height = self._AutoIt.WinGetPosHeight("")
        bbox   = [x, y, x+width-1, y+height-1]
        #
        # Capture and save the screen image of the window
        #
        GrabbedImage = ImageGrab.grab(bbox)     # store screenshot as "RGB" Image
        GrabbedImage.save(fullFilePath)         # PIL evaluates extension
        #
        # Embed the screenshot in the Robot Framework log file
        #
        self._html('<td></td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="700px"></a></td></tr>' % (FilePath, FilePath))
    #
    #-------------------------------------------------------------------------------
    #
    def GetScreenImage(self, FilePath) :
        """
        Capture a full screen image into the given _FilePath_.
        The given _FilePath_ must be relative to Robot Framework output directory,
        otherwise the embedded image will not be shown in the log file.
        """
        #
        # Check that PIL is installed
        #
        if ImageGrab == None :
            raise RuntimeError("Python Imaging Library (PIL) is not installed, but is required for GetScreenImage")
        #
        # Check for a valid FilePath and make sure the directories exist
        #
        if FilePath and os.path.isabs(FilePath):
            raise RuntimeError("Given FilePath='%s' must be relative to Robot outpudir" % FilePath)
        fullFilePath = os.path.join(self._OutputDir, FilePath)
        if not os.path.exists(os.path.split(fullFilePath)[0]):
            os.makedirs(os.path.split(fullFilePath)[0])
        self._info("GetScreenImage(FilePath=%s)" % fullFilePath)
        #
        # Capture and save the screen image of the whole screen
        #
        GrabbedImage = ImageGrab.grab()     # store screenshot as "RGB" Image
        GrabbedImage.save(fullFilePath)     # PIL evaluates extension
        #
        # Embed the screenshot in the Robot Framework log file
        #
        self._html('<td></td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="700px"></a></td></tr>' % (FilePath, FilePath))
    #
    #-------------------------------------------------------------------------------
    #
    def Run(self, FileName, WorkingDir="", Flag="") :
        """
        Direct wrapper for AutoIt's Run method.

        This is required in order to do error code translation into exceptions for Robot Framework.
        """
        self._infoKW(self.Run, FileName, WorkingDir, Flag)

        if WorkingDir == "" and Flag == "" :
            cmd = "FileName='%s'" % FileName
            self._AutoIt.Run(FileName)
        elif WorkingDir != "" and Flag == "" :
            cmd = "FileName='%s', WorkingDir='%s'" % (FileName, WorkingDir)
            self._AutoIt.Run(FileName, WorkingDir)
        else :
            cmd = "FileName='%s', WorkingDir='%s', Flag='%s'" % (FileName, WorkingDir, Flag)
            self._AutoIt.Run(FileName, WorkingDir, Flag)
        #
        # Check the AutoIt error property
        #
        if self._AutoIt.error == 1 :
            raise Exception, "Failed to run %s" % cmd
    #
    #-------------------------------------------------------------------------------
    #
    def WinWait(self, WindowTitle, WindowText="", TimeOut=-1) :
        """
        Direct wrapper for AutoIt's WinWait method.

        This is required in order to do return code translation into exceptions for Robot Framework.
        On failure, optionally captures the full screen image to FAIL_WinWait_<n>.png.
        """
        #
        # Apply default TimeOut if not set
        #
        if TimeOut == -1 :
            TimeOut = self._TimeOut
        self._infoKW(self.WinWait, WindowTitle, WindowText, TimeOut)
        #
        # Do the AutoIt call and handle failure result
        #
        Result = self._AutoIt.WinWait(WindowTitle, WindowText, TimeOut)
        if Result == 0 :
            Result = "Window '%s' (%s) failed to appear in %s seconds" % (WindowTitle, WindowText, TimeOut)
            if self._CaptureScreenOnError :
                self.GetScreenImage("FAIL_WinWait_%d.png" % self._next())
            raise Exception, Result
    #
    #-------------------------------------------------------------------------------
    #
    def WinWaitActive(self, WindowTitle, WindowText="", TimeOut=-1) :
        """
        Direct wrapper for AutoIt's WinWaitActive method.

        This is required in order to do return code translation into exceptions for Robot Framework.
        On failure, optionally captures the full screen image to FAIL_WinWaitActive_<n>.png.
        """
        #
        # Apply default TimeOut if not set
        #
        if TimeOut == -1 :
            TimeOut = self._TimeOut
        self._infoKW(self.WinWaitActive, WindowTitle, WindowText, TimeOut)
        #
        # Do the AutoIt call and handle failure result
        #
        Result = self._AutoIt.WinWaitActive(WindowTitle, WindowText, TimeOut)
        if Result == 0 :
            Result = "Window '%s' (%s) failed to be active in %s seconds" % (WindowTitle, WindowText, TimeOut)
            if self._CaptureScreenOnError :
                self.GetScreenImage("FAIL_WinWaitActive_%d.png" % self._next())
            raise Exception, Result
    #
    #-------------------------------------------------------------------------------
    #
    def WinWaitClose(self, WindowTitle, WindowText="", TimeOut=-1) :
        """
        Direct wrapper for AutoIt's WinWaitClose method.

        This is required in order to do return code translation into exceptions for Robot Framework.
        On failure, optionally captures the full screen image to FAIL_WinWaitClose_<n>.png.
        """
        #
        # Apply default TimeOut if not set
        #
        if TimeOut == -1 :
            TimeOut = self._TimeOut
        self._infoKW(self.WinWaitClose, WindowTitle, WindowText, TimeOut)
        #
        # Do the AutoIt call and handle failure result
        #
        Result = self._AutoIt.WinWaitClose(WindowTitle, WindowText, TimeOut)
        if Result == 0 :
            Result = "Window '%s' (%s) failed to close in %s seconds" % (WindowTitle, WindowText, TimeOut)
            if self._CaptureScreenOnError :
                self.GetScreenImage("FAIL_WinWaitClose_%d.png" % self._next())
            raise Exception, Result
    #
    #-------------------------------------------------------------------------------
    #
    def WaitForActiveWindow(self, WindowTitle, WindowText="", TimeOut=-1) :
        """
        Wait up to _TimeOut_ seconds for the window with the given _WindowTitle_ and optional
        _WindowText_ to appear. Force this to be the active window after it appears.  Optionally do a
        full screen capture on failure.

        Parameters:
        | WindowTitle=<string>  | Title of the application window expected to appear      |
        | [WindowText=<string>] | Optional text on the window expected to appear          |
        | [TimeOut=<seconds>]   | Optional overide to the default timeout set in __init__ |
        """
        self._infoKW(self.WaitForActiveWindow, WindowTitle, WindowText, TimeOut)
        #
        # Wait for the window to be up
        #
        self.WinWait(WindowTitle, WindowText, TimeOut)
        #
        # Force the window to be active
        #
        if not self._AutoIt.WinActive(WindowTitle, WindowText) :
            self._AutoIt.WinActivate(WindowTitle, WindowText)

        self.WinWaitActive(WindowTitle, WindowText, TimeOut)
#
# -------------------------------- End of file --------------------------------
