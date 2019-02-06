from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = open('README.md').read()

setup(
    name='httpie-aws-authv2',
    description='AWS auth v2 plugin for HTTPie.',
    version='0.0.1',
    author='kzmake',
    author_email='kazu.0516.k0n0f@gmail.com',
    license='MIT',
    url='https://github.com/kzmake/httpie-aws-authv2',
    download_url='https://github.com/kzmake/httpie-aws-authv2',
    py_modules=['httpie_aws_authv2'],
    zip_safe=False,
    long_description=long_description,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_aws_authv2 = httpie_aws_authv2:AWSv2AuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.9.7',
        'botocore'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
