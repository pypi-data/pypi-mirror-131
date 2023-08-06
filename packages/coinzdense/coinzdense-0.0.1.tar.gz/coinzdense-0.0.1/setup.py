from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='coinzdense',
    version='0.0.1',
    description='Simple Post-Quantum Signature library',
    long_description="""Library for hash-based signatures using BLAKE2, salt,
    double OTS chains, and Merkle-trees.
    """,
    url='https://github.com/pibara/coinzdense-python',
    author='Rob J Meijer',
    author_email='pibara@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Security :: Cryptography',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'Environment :: Other Environment'
    ],
    keywords='signing postquantum blake2 merkletree ots',
    install_requires=["libnacl","nacl"],
    packages=find_packages(),
)
