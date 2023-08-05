from setuptools import setup
from setuptools.command.egg_info import egg_info


with open("README.md", "r") as f:
    long_description = f.read()


class egg_info_ex(egg_info):
    """Includes license file into `.egg-info` folder."""

    def run(self):
        # don't duplicate license into `.egg-info` when building a distribution
        if not self.distribution.have_run.get("install", True):
            # `install` command is in progress, copy license
            self.mkpath(self.egg_info)
            self.copy_file("LICENSE", self.egg_info)

        egg_info.run(self)


with open("LICENSE", "r") as f:
    license = "".join(["\n", f.read()])


setup(
    name="leetconfig",
    version="0.0.1",
    description="Reusable configuration definition for a Python application.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Red Balloon Security",
    url="https://gitlab.com/redballoonsecurity/leetconfig",
    packages=[
        "leetconfig",
        "leetconfig.definitions",
        "leetconfig.format",
    ],
    package_data={"leetconfig": ["py.typed"]},
    ext_modules=[],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Software Development",
    ],
    install_requires=[
        "enum34; python_version < '3.4'",
        "pyyaml==5.4",
        "structlog~=20.1.0",
    ],
    extras_require={
        "test": [
            "mypy; python_version>='3.5'",
            "pytest",
            "pytest-cov",
            "types-PyYAML==5.4; python_version>='3.5'",
        ]
    },
    license_files=["LICENSE"],
    cmdclass={"egg_info": egg_info_ex},
    project_urls={
        "Bug Tracker": "https://gitlab.com/redballoonsecurity/leetconfig/-/issues",
    },
    python_requires=">=3.7, <=3.8",
)
