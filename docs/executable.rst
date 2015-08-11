Building a Windows Executable
=============================

To build a Windows executable that runs the updater once using settings read
from a configuration file on disk, follow these steps on a Windows machine:

#. Install strongarm-msdns and dependencies

   .. code-block:: powershell

      $ pip install -r requirements.txt

#. Install PyInstaller

   A required PyInstaller hook for the ``requests`` package is added in this
   `commit <https://github.com/pyinstaller/pyinstaller/commit/ed167ead62cddea86b049cb4ccb3e7716162afe2>`_.
   Until this is merged into the stable version, install directly from GitHub:

   .. code-block:: powershell

       $ pip install "https://github.com/pyinstaller/pyinstaller/tarball/ed167ead62cddea86b049cb4ccb3e7716162afe2"

#. Generate a bundled program using PyInstaller

   .. code-block:: powershell

       $ pyinstaller strongarm_msdns\run.py

   This creates the folder ``dist\run``, which contains the executable
   ``run.exe`` and all supporting files.

#. Generate a configuration file

   In the folder ``dist\run``, run the following Python code:

   .. code-block:: python

       from strongarm_msdns.config import write_config
       write_config(api_key="your_key_here", blackhole_ip="strongarm_ip_here")

The folder ``dist\run`` can now be moved to a convenient location.
Double-click ``run.exe`` to run the updater.
