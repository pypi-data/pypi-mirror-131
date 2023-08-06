from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')
requirements = (here / 'requirements.txt').read_text(encoding='utf-8').strip().split('\n')

setup(
    name='mv-laplace',
    version='0.1.1',
    description='Multivariate Laplace Distribution Sampler',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Calvinxc1/mv-laplace',
    author='Jason M. Cherry',
    author_email='jcherry@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.10, <4',
)
