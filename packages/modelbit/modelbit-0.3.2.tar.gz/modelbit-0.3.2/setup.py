from setuptools import setup

setup(
    name='modelbit',
    version='0.3.2',    
    description='Python package to connect Jupyter notebooks to Modelbit',
    url='https://www.modelbit.com',
    author='Modelbit',
    author_email='tom@modelbit.com',
    license='MIT',
    packages=['modelbit'],
    install_requires=['timeago',
                      'pycryptodome',
                      'pandas',
                      'tqdm',
                      'requests',
                      'scikit-learn==1.0.1',
                      ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft',
        'Programming Language :: Python :: 3',
    ],
)