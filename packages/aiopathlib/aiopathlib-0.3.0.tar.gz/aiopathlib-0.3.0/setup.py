# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aiopathlib']
install_requires = \
['aiofiles>=0.7.0,<0.8.0']

setup_kwargs = {
    'name': 'aiopathlib',
    'version': '0.3.0',
    'description': 'Pathlib support for asyncio',
    'long_description': 'aiopathlib: Pathlib support for asyncio\n=======================================\n\n[![image](https://img.shields.io/pypi/v/aiopathlib.svg)](https://pypi.org/project/aiopathlib/)\n[![image](https://img.shields.io/pypi/pyversions/aiopathlib.svg)](https://pypi.org/project/aiopathlib/)\n[![image](https://img.shields.io/pypi/l/aiopathlib.svg)](https://pypi.org/project/aiopathlib/)\n[![image](https://img.shields.io/codecov/c/github/waketzheng/aiopathlib/master.svg)](https://codecov.io/github/waketzheng/aiopathlib?branch=master)\n[![image](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)\n\n**aiopathlib** is written in Python, for handling local\ndisk files in asyncio applications.\n\nBase on `aiofiles` and just like pathlib, but use await.\n\n```py\nwith open(\'filename\', \'w\') as fp:\n    fp.write(\'My file contents\')\n\ntext = await aiopathlib.AsyncPath(\'filename\').read_text()\nprint(text)\n\'My file contents\'\n\ncontent = await aiopathlib.AsyncPath(Path(\'filename\')).read_bytes()\nprint(content)\nb\'My file contents\'\n```\n\nAsynchronous interface to create folder.\n\n```py\nfrom aiopathlib import AsyncPath\n\napath = AsyncPath(\'dirname/subpath\')\nif not await apath.exists():\n    await apath.mkdir(parents=True)\n```\n\n\nFeatures\n--------\n\n- a file API very similar to Python\'s standard package `pathlib`, blocking API\n- support for buffered and unbuffered binary files, and buffered text files\n- support for ``async``/``await`` (:PEP:`492`) constructs\n\n\nInstallation\n------------\n\nTo install aiopathlib, simply:\n\n\n```bash\n$ pip install aiopathlib\n```\n\n\nUsage\n-----\nThese functions are awaitable\n\n* ``read_text``\n* ``read_bytes``\n* ``read_json``\n* ``write_text``\n* ``write_bytes``\n* ``write_json``\n* ``mkdir``\n* ``touch``\n* ``exists``\n* ``rename``\n* ``unlink``\n* ``rmdir``\n* ``remove``\n* ``stat``\n* ``lstat``\n* ``is_file``\n* ``is_dir``\n* ``is_symlink``\n* ``is_fifo``\n* ``is_mount``\n* ``is_block_device``\n* ``is_char_device``\n* ``is_socket``\n\nExample\n-------\nSome common using cases:\n\n```\nfrom pashlib import Path\nfrom aiopathlib import AsyncPath\n\nfilename = \'test.json\'\nap = AsyncPath(filename)\np = Path(filename)\nassert (await ap.exists()) == p.exists() == False\nawait ap.touch()  # Create a empty file\nassert (await ap.is_file()) == p.is_file() == True\nassert (await ap.is_dir()) == p.is_dir() == False\nassert (await ap.is_symlink()) == p.is_symlink() == False\nfor func in (\'is_fifo\', \'is_mount\', \'is_block_device\', \'is_char_device\', \'is_socket\'):\n    assert (await getattr(ap, func)()) == getattr(p, func)()\nd = {\'key\': \'value\'}\nawait ap.write_json(d)  # == p.write_text(json.dumps(d))\nassert (await ap.read_json()) == d  # == json.loads(p.read_text())\nassert (await ap.read_bytes()) == p.read_bytes()  # b\'{"key": "value"}\'\nassert (await ap.stat()) == p.stat()\nassert (await ap.lstat()) == p.lstat()\nap = await ap.rename(\'test_dir\')  # == AsyncPath(p.rename(\'test_dir\'))\nawait ap.remove()  # == await ap.unlink() == p.unlink()\nawait ap.mkdir()  # == p.mkdir()\n\n# Synchronization functions\n[Path(i) for i in ap.glob(\'*\')] == list(p.glob(\'*\'))\n[Path(i) for i in ap.rglob(\'*\')] == list(p.rglob(\'*\'))\nap / \'filename\' == ap.joinpath(\'filename\') == AsyncPath(f\'{ap}/filename\')\nstr(AsyncPath(\'string-or-Path-or-AsyncPath\')) == str(Path(\'string-or-Path-or-AsyncPath\'))\nap.stem == p.stem\nap.suffix == p.suffix\nPath(ap.with_name(\'xxx\')) == p.with_name(\'xxx\')\nPath(ap.parent) == p.parent\nPath(ap.resolve()) == p.resolve()\n...\n```\n\n\nHistory\n-------\n\n#### 0.2.3 (2021-10-16)\n\n- Make `touch` pass test for py39.\n- Remove support for pypy3 from docs.\n\n#### 0.2.2 (2021-09-20)\n\n- Make `touch`/`stat`/`is_file`/... be awaitable.\n- Use `super().__new__` for initial.\n\n#### 0.2.0 (2021-08-29)\n\n- Make `AsyncPath` be subclass of `pathlib.Path`.\n- Add github action to show test coverage.\n\n#### 0.1.3 (2021-08-28)\n\n- Add makefile.\n- Test all functions.\n- Fix rename method error.\n- Support sync pathlib methods.\n\n#### 0.1.0 (2021-06-14)\n\n- Introduced a changelog.\n- Publish at gitee.\n\n\nContributing\n------------\n\nContributions are very welcome.\n',
    'author': 'Waket Zheng',
    'author_email': 'waketzheng@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/waketzheng/aiopathlib',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
