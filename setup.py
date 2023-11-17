from setuptools import setup, find_packages
setup(
    name="autolab",
    version="0.1",
    packages=find_packages(),
    author = "Kyrylo",
    install_requires=[
        'opencv_python==4.6.0.66',
        'mindstorms==0.1.2',
        'pyserial==3.5',
        'numpy==1.23.1',
        'pytest==7.3.2',
        'pylint',
        'black'
    ],
    python_requires='>=3.6',

)