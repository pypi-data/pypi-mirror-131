from setuptools import setup

setup(
    name='python_meijer',
    version='0.1.0',
    description='A python wrapper for the Meijer API',
    url='https://github.com/sllawcj/python_Meijer',
    author='sllawcj',
    author_email='cjsllaw@gmail.com',
    license='MIT',
    packages=['meijer'],
    install_requires=[
        'cached-property', 'certifi', 'charset-normalizer', 'idna', 'requests', 'urllib3'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
