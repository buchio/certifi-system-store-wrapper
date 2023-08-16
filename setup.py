# Copyright (c) 2023 Yukio Obuchi
# Released under the MIT license
# https://github.com/buchio/certifi-system-store-wrapper/blob/main/LICENSE

import os
import sys
import distutils.sysconfig
from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.build_py import build_py


def check_pth(site_packages):
    pthfile = os.path.join(site_packages, 'certifi_system.pth')
    if not os.path.exists(pthfile):
        sys.stderr.write(
            'WARNING: certifi_system.pth not installed correctly, will try to correct.\n')
        sys.stderr.write(
            'Please report an issue at https://gitlab.com/alelec/pip-system-certs with your\n')
        sys.stderr.write(
            'python and pip versions included in the description\n')
        import shutil
        shutil.copyfile('certifi_system.pth', pthfile)


class InstallCheck(install):
    def run(self):
        install.run(self)
        check_pth(self.install_purelib)


class DevelopCheck(develop):
    def run(self):
        develop.run(self)
        check_pth(self.install_dir)


class BuildIncludePth(build_py):
    '''Include the .pth file for this project in the generated wheel.'''

    def run(self):
        super().run()
        pth_file_name = 'certifi_system.pth'
        srcfile = os.path.join('src', pth_file_name)
        outfile = os.path.join(self.build_lib, pth_file_name)
        self.copy_file(srcfile, outfile, preserve_mode=0)


site_packages = distutils.sysconfig.get_python_lib()

setup(
    cmdclass={
        'build_py': BuildIncludePth,
        'install': InstallCheck,
        'develop': DevelopCheck,
    },
)
