import setuptools

description = "Encode and decode HHC numbers, a compact number representation for URLs."
try:
    import pypandoc
    # This bit requires pandoc. On Mac OS X:
    #   brew install haskell-platform && cabal update && cabal install pandoc
    description = pypandoc.convert('README.md', 'rst', format='markdown')
except:
    pass

setuptools.setup(
    name='hhc',
    version='3.0.0',
    description='The best way to express a number in a URL.',
    author='Alexander Ljungberg',
    author_email='aljungberg@slevenbits.com',
    url='https://github.com/aljungberg/hexahexacontadecimal',
    packages=['hhc'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    keywords=["base64", "hexahexacontadecimal", "hhc", "base66", "url"],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
    ],
    long_description=description
)
