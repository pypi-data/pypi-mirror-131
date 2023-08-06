import os
import re
import sys
import traceback

from setuptools import setup, find_packages, Extension
from setuptools.command.install import install
from setuptools.command.egg_info import egg_info
from setuptools.command.build_ext import build_ext, _build_ext
import subprocess

# Convert distutils Windows platform specifiers to CMake -A arguments
PLAT_TO_CMAKE = {
    "win32": "Win32",
    "win-amd64": "x64",
    "win-arm32": "ARM",
    "win-arm64": "ARM64",
}
# command = "sh prepare_env_source.sh"
# process = subprocess.Popen(command, shell=True, cwd=".")


class CustomInstallCommand(install):
    """Custom install setup to help run shell commands (outside shell) before installation"""

    def run(self):
        custom_command = "sh prepare_env_source.sh"
        # custom_process = subprocess.Popen(custom_command, shell=True, cwd=".")
        # custom_process.wait()
        try:
            subprocess.check_call(custom_command, shell=True, cwd=".")
        except subprocess.CalledProcessError:
            print("Not have cmake")
        install.run(self)


class CustomEggInfoCommand(egg_info):
    """Custom install setup to help run shell commands (outside shell) before installation"""

    def run(self):
        egg_info.run(self)
        custom_command = "sh prepare_env_source.sh"
        # custom_process = subprocess.Popen(custom_command, shell=True, cwd=".")
        # custom_process.wait()
        try:
            subprocess.check_call(custom_command, shell=True, cwd=".")
        except subprocess.CalledProcessError:
            print("Not have cmake")


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        """Build extensions in build directory, then copy if --inplace"""
        self.inplace = 0
        _build_ext.run(self)

    def build_extension(self, ext):
        try:
            extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

            # required for auto-detection & inclusion of auxiliary "native" libs

            debug = (
                int(os.environ.get("DEBUG", 0)) if self.debug is None else self.debug
            )
            cfg = "Debug" if debug else "Release"

            # CMake lets you override the generator - we need to check this.
            # Can be set with Conda-Build, for example.
            cmake_generator = os.environ.get("CMAKE_GENERATOR", "")

            # Set Python_EXECUTABLE instead if you use PYBIND11_FINDPYTHON
            # EXAMPLE_VERSION_INFO shows you how to pass a value into the C++ code
            # from Python.
            cmake_args = [
                f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
                f"-DPYTHON_EXECUTABLE={sys.executable}",
                f"-DCMAKE_BUILD_TYPE={cfg}",  # not used on MSVC, but no harm
            ]
            build_args = []
            # Adding CMake arguments set as environment variable
            # (needed e.g. to build for ARM OSx on conda-forge)
            if "CMAKE_ARGS" in os.environ:
                cmake_args += [
                    item for item in os.environ["CMAKE_ARGS"].split(" ") if item
                ]

            # In this example, we pass in the version to C++. You might not need to.
            cmake_args += [f"-DEXAMPLE_VERSION_INFO={self.distribution.get_version()}"]

            if self.compiler.compiler_type != "msvc":
                # Using Ninja-build since it a) is available as a wheel and b)
                # multithreads automatically. MSVC would require all variables be
                # exported for Ninja to pick it up, which is a little tricky to do.
                # Users can override the generator with CMAKE_GENERATOR in CMake
                # 3.15+.
                if not cmake_generator:
                    try:
                        import ninja  # noqa: F401

                        cmake_args += ["-GNinja"]
                    except ImportError:
                        pass

            else:

                # Single config generators are handled "normally"
                single_config = any(x in cmake_generator for x in {"NMake", "Ninja"})

                # CMake allows an arch-in-generator style for backward compatibility
                contains_arch = any(x in cmake_generator for x in {"ARM", "Win64"})

                # Specify the arch if using MSVC generator, but only if it doesn't
                # contain a backward-compatibility arch spec already in the
                # generator name.
                if not single_config and not contains_arch:
                    cmake_args += ["-A", PLAT_TO_CMAKE[self.plat_name]]

                # Multi-config generators have a different way to specify configs
                if not single_config:
                    cmake_args += [
                        f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}"
                    ]
                    build_args += ["--config", cfg]

            if sys.platform.startswith("darwin"):
                # Cross-compile support for macOS - respect ARCHFLAGS if set
                archs = re.findall(r"-arch (\S+)", os.environ.get("ARCHFLAGS", ""))
                if archs:
                    cmake_args += [
                        "-DCMAKE_OSX_ARCHITECTURES={}".format(";".join(archs))
                    ]

            # Set CMAKE_BUILD_PARALLEL_LEVEL to control the parallel build level
            # across all generators.
            if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
                # self.parallel is a Python 3 only way to set parallel jobs by hand
                # using -j in the build_ext call, not supported by pip or PyPA-build.
                if hasattr(self, "parallel") and self.parallel:
                    # CMake 3.12+ only.
                    build_args += [f"-j{self.parallel}"]

            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)

            print(["cmake", ext.sourcedir] + cmake_args)
            subprocess.check_call(
                ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp
            )
            print(["cmake", "--build", "."] + build_args)
            subprocess.check_call(
                ["cmake", "--build", "."] + build_args, cwd=self.build_temp
            )
        except Exception as e:
            traceback.print_stack()
            print(e)
            print(f"c_tools module fail to compile")


with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    "pandas",
    "numpy",
    "aiosmtplib",
    "python-dateutil",
    "pymongo",
    "redis",
    "pyyaml",
    "motor",
]

extras_require = {
    "full": ["luigi", "scikit-learn", "joblib"],
}


setup(
    name="lightning_fast",
    version="0.0.99",
    author="yingxiongxqs",
    author_email="yingxiongxqs@126.com",
    description="Fast Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xuqiushi/lightning_fast",
    # cmdclass={
    #     "install": CustomInstallCommand,
    #     # 'develop': CustomDevelopCommand,
    #     "egg_info": CustomEggInfoCommand,
    # },
    ext_package="lightning_fast.c_tools",
    ext_modules=[CMakeExtension("encoders", "c_source")],
    cmdclass={"build_ext": CMakeBuild},
    # package_dir={"": "lightning_fast"},
    packages=find_packages(exclude=("tests",)),
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Text Processing",
    ],
    python_requires=">=3.7",
    zip_safe=False,
    extras_require=extras_require,
)
