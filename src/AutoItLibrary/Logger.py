"""
Package: AutoItLibrary
Module:  Loggger
Purpose: Defines a Logger class from which other classes can inherit the ability to log messages to
         stdout.  The Logger class' _log method does this in the style required by Robot Framework, but
         this method could be overridden in the class that uses it in order to log in some other style
         or to some other output path.

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
__author__ = "Martin Taylor <cmtaylor@ti.com>"
__version__ = "1.0.1"

class Logger :
    def _log(self, message, level='INFO') :
        print '*%s* %s' % (level, message)

    def _info(self, message) :
        self._log(message)

    def _debug(self, message) :
        self._log(message, 'DEBUG')

    def _warn(self, message) :
        self._log(message,  "WARN")

    def _html(self, message) :
        self._log(message, 'HTML')

    def _infoKW(self, KW, *args, **kwargs) :
        """
        Print a generic log message for the entry point of a given keyword, KW at *INFO* level.
        """
        self._info("%s.%s(%s)" % (KW.im_class.__name__, KW.func_name, self._FormatArgs(KW, *args, **kwargs)))

    def _debugKW(self, KW, *args, **kwargs) :
        """
        Print a generic log message for the entry point of a given keyword, KW at *DEBUG* level.
        """
        self._debug("%s.%s(%s)" % (KW.im_class.__name__, KW.func_name, self._FormatArgs(KW, *args, **kwargs)))


    def _FormatASCII(self, pyObj) :
        """
        Format the given pyObj as an ASCII string.  This is first attempted by doing str(pyObj).
        If that fails then if pyObj is a Unicode string it replaces each non-ASCII character with its
        repr encoding.  For any other pyObj it simply returns the complete repr encoding of pyObj.
        """
        try :
            aString = str(pyObj)
        except UnicodeEncodeError :
            if isinstance(pyObj, type(u'')) :
                aString = ""
                for c in pyObj :
                    if ord(c) > 128 :
                        aString += repr(c)[2:-1]
                    else :
                        aString += c
            else :
                aString = repr(pyObj)
        finally :
            return aString


    def _FormatArg(self, fmtLine, argName, argVal) :
        """
        Format the given argName and argVal and add them to the current given fmtLine.
        If fmtLine is non-empty then ", " is appended to it before appending the formatted argName=argVal.
        """
        if len(fmtLine) > 0 :
            fmtLine += ", "

        if isinstance(argVal, type(1)) :
            fmtLine += "%s=%d" % (argName, argVal)

        elif isinstance(argVal, type(1.1)) :
            fmtLine += "%s=%g" % (argName, argVal)

        else :
            fmtLine += "%s='%s'" % (argName, self._FormatASCII(argVal))

        return fmtLine


    def _FormatArgs(self, func, *args, **kwargs) :
        """
        Format an arbitrary list of args and kwargs for function func for printing in a log line.
        TBD: Add any defaulted args not present in args or kwargs
        """
        fmtLine = ""
        funcArgs = None
        #
        # If we got some positional args then format those, adding the
        # argument name from the tuple of co_varnames obtained above.
        #
        if len(args) > 0 :
            funcArgs = func.func_code.co_varnames
            #
            # If func is a method of a class then it will have "self" as the first argument.
            # We don't want to print that, and it won't be in args or kwargs anyway, so remove it.
            #
            if funcArgs[0] == "self" :
                funcArgs = funcArgs[1:]
            ai = 0
            for arg in args :
                fmtLine = self._FormatArg(fmtLine, funcArgs[ai], arg)
                ai += 1
        #
        # If we got some kwargs, then format those.
        #
        if len(kwargs.keys()) > 0 :
            if funcArgs == None :
                funcArgs = func.func_code.co_varnames
                #
                # If func is a method of a class then it will have "self" as the first argument.
                # We don't want to print that, and it won't be in args or kwargs anyway, so remove it.
                #
                if funcArgs[0] == "self" :
                    funcArgs = funcArgs[1:]
                ai = 0

            for i in range(ai, len(funcArgs)) :
                key = funcArgs[i]
                if key not in kwargs.keys() :
                    continue
                fmtLine = self._FormatArg(fmtLine, key, kwargs[key])
                del kwargs[key]
        #
        # TBD: Add any defaulted args not present in args or kwargs
        #
        #
        # Add any additional args passed but not explicitly expected
        #
        if len(kwargs.keys()) > 0 :
            for key in kwargs :
                fmtLine = self._FormatArg(fmtLine, key, kwargs[key])

        return fmtLine
#
# -------------------------------- End of file --------------------------------
