from os.path import abspath, dirname, join as pjoin
from setuptools import setup, find_packages

root = dirname(abspath(__file__))


def execfile(fname, globs, locs=None):
    locs = locs or globs
    exec(compile(open(fname).read(), fname, "exec"), globs, locs)


source_path = 'src'
packages = find_packages(source_path)
root_packages = [
    package
    for package in packages
    if "." not in package
]

assert len(root_packages) == 1
package = root_packages[0]
package_directory = pjoin(root, source_path, package)


def get_variable_from_file(filepath, variable):
    filepath_in_package = pjoin(package_directory, filepath)
    globs = {}
    execfile(filepath_in_package, globs)
    variable_value = globs[variable]

    return variable_value


version = get_variable_from_file('_version.py', '__version__')

setup(
    name=package,
    version=version,
    python_requires='>=3.6',
    description='Python service registry used as a service container as well as defines and boots '
                'services',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers'
    ],
    packages=packages,
    maintainer='Omar Shaban',
    maintainer_email='omars@php.net',
    package_dir={'': source_path},
    include_package_data=True,
    package_data={package: []},
    license='MIT License',
    extras_require={
        'test': [
            'pytest'
        ]
    }
)
