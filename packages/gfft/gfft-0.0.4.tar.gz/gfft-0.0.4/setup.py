from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'gfft',
    version = '0.0.4',
    description = 'Initial python project VA & MS',
    url = 'https://github.com/vaalessi/gfft',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    license = 'BSD 3-Clause', 
    entry_points = {
        'console_scripts': [
            'gfft = gfft:main'
        ]
    },
    author = 'Vince Alessi', 
    packages=["gfft"],
    package_dir={'gfft': "./gfft"},
    author_email = 'valessi@umich.edu',
    classifiers = [ 
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'Framework :: IPython',
        'Topic :: Scientific/Engineering :: Bio-Informatics' 
    ]
)