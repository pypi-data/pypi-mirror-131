from pkg_resources import DistributionNotFound, get_distribution
from distutils.core import setup


def get_dist(pkgname):
    try:
        return get_distribution(pkgname)
    except DistributionNotFound:
        return None


install_deps = [
    'numpy',
    'regex',
    'tqdm',
    'gym'
]
tf_ver = '2.0.0a'
if get_dist('tensorflow>=' + tf_ver) is None and get_dist('tensorflow_gpu>=' + tf_ver) is None:
    install_deps.append('tensorflow>=' + tf_ver)

setup(
    name='musicgeneration',
    packages=['musicgeneration'],
    version='0.10.0',
    license='MIT',
    description='diploma project',
    author='Bohdan Kulynych',
    keywords=['deep learning', 'neural networks', 'tensorflow', 'introduction'],
    install_requires=install_deps,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    include_package_data=True,
    package_data={'musicgeneration': ['data/*', 'bin/*']}

)
