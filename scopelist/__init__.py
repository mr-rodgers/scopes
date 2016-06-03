from os import path


# Read the package version from the VERSION.txt file.
this_dir = path.dirname(__file__)
version_file = open(path.join(this_dir, 'VERSION.txt'), encoding='ascii')
__version__ = version_file.read().strip()
version_file.close()


__all__ = ['__version__']
