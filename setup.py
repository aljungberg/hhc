import setuptools

description = "Encode and decode hexahexacontadecimal numbers, a compact number representation for URLs."
try:
    import pypandoc
    # This bit requires pandoc. On Mac OS X:
    #   brew install haskell-platform && cabal update && cabal install pandoc
    description = pypandoc.convert('README.md', 'rst', format='markdown')
except:
    pass

setuptools.setup(
    name='hexahexacontadecimal',
    version='2.2.1',
    description='The best way to express a number in a URL.',
    author='Alexander Ljungberg',
    author_email='aljungberg@slevenbits.com',
    url='https://github.com/aljungberg/hexahexacontadecimal',
    packages=['hexahexacontadecimal'],
    keywords=["base64", "hexahexacontadecimal", "hhc", "base66", "url"],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
    ],
    long_description=description
)
