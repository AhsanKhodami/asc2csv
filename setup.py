from setuptools import setup, find_packages
import pathlib

# Read the contents of your README file
current_directory = pathlib.Path(__file__).parent
readme = (current_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='asc2csv',
    use_scm_version=True,  # Automatically determine the version using setuptools_scm
    author='Mohammad Ahsan Khodami',
    author_email='ahsan.khodami@gmail.com',
    description='A Python package for converting EyeLink .asc files to structured .csv files.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/AhsanKhodami/asc2edf',
    packages=find_packages(),
    install_requires=[
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ascii2edf=ascii2edf.converter:process_asc_file',
        ],
    },
    project_urls={
        'Source': 'https://github.com/AhsanKhodami/asc2csv',
        'Tracker': 'https://github.com/AhsanKhodami/asc2csv/issues',
    },
    setup_requires=['setuptools_scm'],)