from conans import ConanFile, tools, AutoToolsBuildEnvironment
import shutil
import os

class CPython(ConanFile):
    name = "cpython"
    version = "3.7.3"

    settings = "os", "arch", "compiler", "build_type"

    def source(self):
        url = "https://github.com/python/cpython/archive/v{v}.tar.gz".format(v=self.version)
        tools.get(url)
        shutil.move("cpython-{v}".format(v=self.version), self.name)

        # Patch some Python modules to ensure 'is_python_build' returns True
        tools.replace_in_file(os.path.join(self.source_folder, self.name, "Lib", "sysconfig.py"),
                              "_sys_home = getattr(sys, '_home', None)",
                              "_sys_home = None  # Force it (we are calling this script from installed python)")

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(configure_dir=self.name)
        autotools.make()
        #autotools.install()

    def package(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = ["python3.7m",]
        self.cpp_info.includedirs = ["include/python3.7m", ]
