# -*- coding: utf-8 -*-
#
# setup.py
# Create source distribution with: python setup.py sdist
#
import re
from distutils.core import setup
# from dl2050utils.core import pump_version, get_version, get_minor, get_camel
from dl2050utils.fs import sh_run

NAME = 'dl2050utils'

def get_version():
    with open('./__version__.py', 'r') as f: v=f.read()
    v = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", v, re.M)
    if not v: raise RuntimeError('Unable to find version number')
    return v.group(1)

def get_version_parts(ver):
    res = re.split(r'\.', ver, maxsplit=2)
    if len(res)<3: raise RuntimeError('Unable to parse version number')
    return res

def get_minor(ver):
    res = get_version_parts(ver)
    return res[2]

def get_camel(ver):
    res = get_version_parts(ver)
    return f'{res[0]}_{res[1]}_{str(int(res[2])+1)}'

def pump_version():
    ver = get_version()
    res = get_version_parts(ver)
    ver = f'{res[0]}.{res[1]}.{str(int(res[2])+1)}'
    with open('./__version__.py', 'w') as f: f.write(f'__version__ = "{ver}"')

pump_version()
ver = get_version()
print(f'setup: preparing version {ver}')
minor = get_minor(ver)
ver_camel = get_camel(ver)

setup(name=NAME,
      packages=[NAME],
      version=ver,
      license='MIT',
      description='Utils lib',
      author='João Neto',
      author_email='joao.filipe.neto@gmail.com',
      keywords=['utils'],
      url='https://github.com/jn2050/utils',
      download_url=f'https://github.com/jn2050/utils/archive/v_{ver_camel}.tar.gz',
      # install_requires=[
      #       'pathlib',
      #       'zipfile',
      #       'json',
      #       'socket',
      #       'smtplib',
      #       'ssl',
      #       'boto3',
      #       'asyncpg',
      #       '',
      # ],
      classifiers=[
            'Development Status :: 4 - Beta',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.7',
      ],
)

cmd = f'gh release create -t "{ver_camel}" --notes "Update" dist/{NAME}-{ver}.tar.gz'
print(cmd)
res, sout, serr = sh_run(cmd)
if res!=0: raise RuntimeError(f'Unable to run:\n{cmd}\nERROR:{serr}')

cmd = f'twine upload dist/* --repository {NAME}'
print(cmd)
res, sout, serr = sh_run(cmd)
if res!=0: raise RuntimeError(f'Unable to run:\n{cmd}\nERROR:{serr}')