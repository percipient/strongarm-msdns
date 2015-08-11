Creating a Windows Service
==========================

To create a Windows service that runs the updater periodically using settings
read from a configuration file on disk, follow these steps on a Windows machine:

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

       $ pyinstaller service.py

   This creates the folder ``dist\service``, which contains the executable
   ``service.exe`` and all supporting files.

#. Generate a configuration file

   In the folder ``dist\service``, run the following Python code:

   .. code-block:: python

       from strongarm_msdns.config import write_config
       write_config(api_key="your_key_here", blackhole_ip="strongarm_ip_here")

#. Move the folder ``dist\service`` to a permanent location, such as Program
   Files.

#. In the new location, run ``service.exe install`` in the command line to
   install the service.

#. Start the service using the builtin Service Manager in Windows. You should
   see the service listed as "STRONGARM DNS Updater".

You can see the logs the service produces in Event Viewer - Windows Logs -
Application.
