from distutils.core import setup

long_description = """RicciPy is a Python tensor algebra engine for
symbolically manipulating exact solutions to the Einstein Field Equations."""

setup(
    name='riccipy',
    author='Calvin Jay Ross',
    author_email='calvinjayross@gmail.com',
    description='A tensor algebra calculator for General Relativity',
    long_description=long_description,
    url='https://github.com/cjayross/riccipy',
    download_url='https://github.com/cjayross/riccipy/archive/v0.1-alpha.tar.gz',
    license='MIT',
    version='v0.1-alpha',
    packages=['riccipy',],
    install_requires=['numpy', 'sympy'],
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
    ],
)
