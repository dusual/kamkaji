from setuptools import setup


setup(
    name='jobs_manager',
    version='0.1',
    description='django task queue using beanstalkd'
    long_description=open('Readme.md').read(),
    author='E2Enetworks',
    url='https://github.com/E2ENetworksPrivateLimited/kamkaji',
    license='MPL',
    packages=['jobs_manager'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['pyyaml', 'beanstalkc'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
