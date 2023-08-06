# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['rocktree', 'rocktree_server']
install_requires = \
['patchutils>=1.1.3,<2.0.0', 'requests>=2.26.0,<3.0.0']

extras_require = \
{'server': ['flask>=2.0.2,<3.0.0'],
 'server-gevent': ['flask>=2.0.2,<3.0.0', 'gevent>=21.12.0']}

setup_kwargs = {
    'name': 'rocktree',
    'version': '1.0.0',
    'description': 'Rock Solid Library for syncing progress online with byte to byte same working tree.',
    'long_description': '# Rocktree\n\nA tool for making keeping your working testing tree rock solid up to date\nwith the latest developments in place with upstream link.\n\nConsider giving us a :star:. Made with love by contributors.\n\n**In development, yet to be implemented**\n\n## Concept\n\nSo for example we have `http://example.com/testing-repo`. It gets updated\ntime to time and we want to keep up to date with it all the time blanking\nout all the local changes as soon as the changes are pulled from\nupstream. It works on the bases of [`patchutils`](https://github.com/xcodz-dot/patchutils)\nwhich works on the bases of patchfiles, update files and directory trees.\n\nTo download from upstream for the first time you can use the `rocktree.clone(url="http://my_url.com/repo", dir="local_repo")`\nafter that the repo should contain a `.rocktree` file which contains the\nupstream link. You can then use the method `rocktree.update_from_file(dir="local_repo")`.\nYou can also force update from a specified repo using the provided method\n`rocktree.update(dir="local_repo", url="http://my_url.com/repo")',
    'author': 'xcodz-dot',
    'author_email': '71920621+xcodz-dot@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xcodz-dot/rocktree',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
