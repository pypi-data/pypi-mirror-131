# -*- coding: utf-8 -*-
#
# setup.py
# Create source distribution with: python setup.py sdist
#
from distutils.core import setup
from dl2050utils.__config__ import name, package, description, author, author_email, keywords
from dl2050utils.__config__ import pump_version, get_camel, save_version
from dl2050utils.__version__ import version
from dl2050utils.fs import sh_run

sh_run('rm -rf dist/*.gz')
print(version)
version = pump_version(version)
version_camel = get_camel(version)
print(f'setup for package {package} version {version}')

url = f'https://github.com/jn2050/{name}'
download_url = f'https://github.com/jn2050/{name}/archive/v_{version_camel}.tar.gz'
install_requires = []
classifiers=[
      'Development Status :: 4 - Beta',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.7',
]

setup(name=package,
      packages=[package],
      version=version,
      license='MIT',
      description=description,
      author=author,
      author_email=author_email,
      keywords=keywords,
      url=url,
      download_url=download_url,
      install_requires=install_requires,
      classifiers=classifiers
)

cmd = f'gh release create -t "{version_camel}" --notes "Update" dist/{name}-{version}.tar.gz'
print(cmd)
res, sout = sh_run(cmd)
print(sout)

cmd = f'twine upload dist/* --repository {package}'
print(cmd)
res, sout = sh_run(cmd)
print(sout)

save_version(version)