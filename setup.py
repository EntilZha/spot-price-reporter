from setuptools import setup, find_packages


setup(
    name='spot-price-reporter',
    description='Fetches the most recent aws spot prices, plots them, and sends them to you',
    url='https://github.com/EntilZha/spot-price-reporter',
    author='Pedro Rodriguez',
    author_email='ski.rodriguez@gmail.com',
    maintainer='Pedro Rodriguez',
    maintainer_email='ski.rodriguez@gmail.com',
    license='Apache License 2.0',
    keywords='aws spot price plot slack email',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*', 'test']),
    version='0.0.0',
    install_requires=['pandas', 'seaborn', 'click', 'awscli', 'slacker', 'matplotlib'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
