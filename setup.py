from setuptools import setup

long_description = """RicciPy is a Python tensor algebra calculator for
symbolically manipulating exact solutions to the Einstein Field Equations."""

version = '0.2a'
version_ref = '1'

setup(
    name='riccipy',
    author='Calvin Jay Ross',
    author_email='calvinjayross@gmail.com',
    description='A tensor algebra calculator for General Relativity',
    long_description=long_description,
    url='https://github.com/cjayross/riccipy',
    download_url='https://github.com/cjayross/riccipy/archive/v' + version + '.tar.gz',
    license='MIT',
    version=version + version_ref,
    packages=['riccipy', 'riccipy.metrics', 'riccipy.tests'],
    install_requires=open('requirements.txt').read().split('\n')[:-1],
    keywords='general relativity physics math cas',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
