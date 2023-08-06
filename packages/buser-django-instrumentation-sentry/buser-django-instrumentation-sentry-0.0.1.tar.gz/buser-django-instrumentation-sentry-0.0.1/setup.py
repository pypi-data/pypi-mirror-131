import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "buser-django-instrumentation-sentry",
    version = "0.0.1",
    author = "Erle Carrara",
    author_email = "erle.carrara@buser.com.br",
    description = ("A helper library to configure centry instrumentation in Django projects."),
    license = "MIT",
    keywords = "buser sentry django",
    url = "http://packages.python.org/buser-django-instrumentation-sentry",
    packages=find_packages('.'),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'django<4',
        'sentry_sdk<2',
        'raven<7',
    ],
    extras_require = {
        'redis_dedup':  ["redis<5"]
    }
)
