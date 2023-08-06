from setuptools import setup

setup(
    name='Sentwits',
    version='0.0.3',
    description='Real-time sentiment Stocktwits analysis tool',
    url='https://github.com/brandonbondig/sentwits',
    author='Brandon Bondig',
    author_email='brandon@bondig.dk',
    license='MIT',
    packages=['sentwits'],
    classifiers=[
        # How mature is this project? Common values are
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='stocks analysis finance market shares stocktwits sentiment real-time',
    install_requires=['requests', 'setuptools', 'pandas'],
)