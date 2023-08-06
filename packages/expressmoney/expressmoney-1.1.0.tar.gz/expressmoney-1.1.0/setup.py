"""
py setup.py sdist
twine upload dist/expressmoney-1.1.0.tar.gz
"""
import setuptools

setuptools.setup(
    name='expressmoney',
    packages=setuptools.find_packages(),
    version='1.1.0',
    description='SDK ExpressMoney',
    author='Development team',
    author_email='dev@expressmoney.com',
    # url='https://github.com/zsergey85/',
    install_requires=('google-cloud-secret-manager', 'google-cloud-error-reporting', 'google-cloud-pubsub',
                      'google-cloud-tasks', 'google-cloud-storage', 'requests'),
    # download_url='https://github.com/zsergey85/',
    keywords=('expressmoney',),
    classifiers=(),
    python_requires='>=3.7',
)
