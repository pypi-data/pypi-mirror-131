from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='domain-check',
    version='1.0.0',
    description='Check which TLDs are still free for a given name',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nonchris/check-domain/',
    author='nonchris',
    author_email='info@nonchris.eu',

    classifiers=[

        'Development Status :: 5 - Production/Stable',

        'Environment :: Console',

        'Intended Audience :: Other Audience',
        'Topic :: Internet',

        'Typing :: Typed',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='domain, tld, check, free',

    package_dir={'': 'src/'},

    packages=find_packages(where='src/'),

    python_requires='>=3.8, <4',

    install_requires=["requests"],

    entry_points={
        'console_scripts': [
            'domain-check=checker:main',
        ],
    },

    project_urls={
        'Bug Reports': 'https://github.com/nonchris/domain-check/issues',
        'Source': 'https://github.com/nonchris/domain-check/',
    },
)
