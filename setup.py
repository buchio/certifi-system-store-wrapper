# Copyright (c) 2025 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

# This setup.py script configures the installation and packaging process for the certifi-system-store-wrapper project.
# It ensures that the .pth file is included in both development and installation, so that the bootstrap logic is executed automatically.

import os
import sys
import distutils.sysconfig
from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.build_py import build_py

pthfilename = 'certifi_system_store_wrapper.pth'

def check_pth(site_packages):
    """
    Ensure the .pth file is present in the site-packages directory.
    If not, attempt to copy it and notify the user.
    """
    global pthfilename
    pthfile = os.path.join(site_packages, pthfilename)
    if not os.path.exists(pthfile):
        sys.stderr.write(
            f'WARNING: {pthfilename} not installed correctly, will try to correct.\n')
        sys.stderr.write(
            'Please report an issue at https://gitlab.com/buchio/certifi-system-store-wrapper with your\n')
        sys.stderr.write(
            'python and pip versions included in the description\n')
        import shutil
        shutil.copyfile(pthfilename, pthfile)

class InstallCheck(install):
    """
    Custom install command to check and copy the .pth file after installation.
    """
    def run(self):
        install.run(self)
        check_pth(self.install_purelib)

class DevelopCheck(develop):
    """
    Custom develop command to check and copy the .pth file after development install.
    """
    def run(self):
        develop.run(self)
        check_pth(self.install_dir)

class BuildIncludePth(build_py):
    """
    Custom build_py command to include the .pth file in the generated wheel.
    """
    def run(self):
        super().run()
        global pthfilename
        srcfile = os.path.join('src', pthfilename)
        outfile = os.path.join(self.build_lib, pthfilename)
        self.copy_file(srcfile, outfile, preserve_mode=0)

site_packages = distutils.sysconfig.get_python_lib()

setup(
    cmdclass={
        'build_py': BuildIncludePth,
        'install': InstallCheck,
        'develop': DevelopCheck,
    },
)
