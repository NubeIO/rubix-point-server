from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')
with open('VERSION') as version_file:
    version = version_file.read().strip()

setup(
    name='point-server',  # Required
    version=version,  # Required
    description='Nube-iO Rubix Point Server',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional

    url='https://github.com/NubeIO/rubix-point-server',  # Optional
    author='Nube-iO',  # Optional
    author_email='tech-support@nube-io.com',  # Optional

    packages=find_packages(exclude=['tests', 'tests.*'], include=['src', 'src.*']),
    include_package_data=True,
    data_files=[('', [
        'run.py',
        'settings/config.example.ini',
        'logging/logging.example.conf',
        'systemd/nubeio-point-server.service',
        'script.bash',
        'runtime.txt',
        'requirements.txt',
        'VERSION',
    ])],
    python_requires='>=3.7, <4',

    # Any package you put here will be installed by pip
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'BAC0',
        'bacpypes',
        'pymodbus',
        'influxdb',
    ],  # Optional

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install .[standalone]
    #
    extras_require={  # Optional
        'standalone': [
            'Flask~=1.1.2',
            'Flask-RESTful',
            'Flask-JWT',
            'Flask-SQLAlchemy',
            'flask_cors',
            'uwsgi',
            'gunicorn',
            'gevent',
            'SQLAlchemy~=1.3.19',
            'requests',
            'pandas',
            'uuid==1.30',
            'schedule==0.6.0',
            'psycopg2-binary',
            'paho-mqtt',
        ]
    },
)

