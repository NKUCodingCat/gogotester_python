import os, sys
def RootPath():
    if hasattr(sys, "frozen"):
        return os.path.dirname(unicode(sys.executable, sys.getfilesystemencoding( )))+"/"
    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))+"/"
