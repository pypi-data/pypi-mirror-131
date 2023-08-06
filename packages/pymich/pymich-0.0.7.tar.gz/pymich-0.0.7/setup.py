from setuptools import setup


setup(
    name='pymich',
    version='0.0.7',
    setup_requires='setupmeta',
    install_requires=['pytezos', 'cli2'],
    extras_require=dict(
        test=[
            'freezegun',
            'pytest',
            'pytest-cov',
        ],
    ),
    author='Thomas Binetruy',
    author_email='tbinetruy@gmail.com',
    url='https://yourlabs.io/piratzlabs/pymich',
    include_package_data=True,
    license='MIT',
    keywords='cli',
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'pymich = pymich.pymich:cli.entry_point',
        ],
    },
)
