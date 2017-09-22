from distutils.core import setup
import py2exe
import sys
 
#this allows to run it with a simple double click.
sys.argv.append('py2exe')
 
py2exe_options = {
        "dll_excludes": ["MSVCP90.dll",],
        "compressed": 1,
        "optimize": 2,
        "ascii": 0,
        "bundle_files": 1,
        }
 
setup(
      name = 'multiping',
      version = '1.0.3',
      console = [{ "script":'multiping.py',"icon_resources":[(1,"myico.ico")]}], 
      zipfile = None,
      options = {'py2exe': py2exe_options}
      )