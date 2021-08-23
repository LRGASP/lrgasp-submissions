#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools

requirements = [
    "gtfparse==1.2.1",
    "validators==0.18.2",
    "synapseclient==2.4.0",
    "fasta-reader==1.0.0"
]

setuptools.setup(
    name = 'lrgasp-tools',
    version = '1.2.0',
    description = "LRGASP tools",
    long_description = "LRGASP tools for submission",
    author = "Mark Diekhans",
    author_email = 'markd@ucsc.edu',
    url = 'https://github.com/LRGASP/lrgasp-submissions',
    scripts=[
        'bin/lrgasp-validate-de-novo-rna',
        'bin/lrgasp-validate-entry',
        'bin/lrgasp-validate-entry-metadata',
        'bin/lrgasp-validate-experiment-metadata',
        'bin/lrgasp-validate-expression-matrix',
        'bin/lrgasp-validate-models',
        'bin/lrgasp-validate-read-model-map',
        'bin/lrgasp-upload-entry',
        'bin/lrgasp-synapse-download',
    ],
    packages = [
        'lrgasp',
    ],
    package_dir = {'': 'lib'},
    include_package_data = True,  # MUST update MANIFEST.in to include files
    install_requires = requirements,
    license = "MIT",
    zip_safe = True,
    keywords = ['Bioinformatics', 'genomics', 'transcriptomics'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.7',

)
