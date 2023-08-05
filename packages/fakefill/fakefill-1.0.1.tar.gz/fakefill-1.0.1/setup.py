# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fakefill', 'fakefill.helpers']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.0,<8.0.0', 'loguru>=0.5.2,<0.6.0', 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['fakefill = fakefill.cli:cli']}

setup_kwargs = {
    'name': 'fakefill',
    'version': '1.0.1',
    'description': 'Fast & Fake Backfill Airflow DAGs Status',
    'long_description': '# Airflow Fakefill Marker\n\n\n\nDue to migrating to Kubernetes-host Airflow and using different backend, we need to find out a way to fill out all the history since its starting date for thousands of dags. To make this process going faster and easier, in the meantime, I didn\'t find this kind of tool on Github, so I implement this simple tool to help with marking dags as `success.` Hope it can also help others.\n\n\n\n## Installations\n\n### Method 1\n\n```bash\n$ pip install fakefill\n```\n\n### Method 2\n\n```bash\n$ pip install git+https://git@github.com/benbenbang/airflow_fastfill.git\n```\n\n### Method 3\n\n```bash\n$ git clone git@github.com:benbenbang/airflow_fastfill.git\n$ cd airflow_fastfill\n$ pip install .\n```\n\n\n\n## Usages\n\n```bash\n$ fakefill\n```\n\nIt takes 1 of 2 required argument, and 6 optional arguments. You can also define them in a yaml file and pass to the cli.\n\n- Options\n\n    - Required [1 / 2]:\n\n        > - dag_id [-d][reqired]: can be a real dag id or "all" to fill all the dags\n        > - config_path [-cp][choose one]: path to the config yaml\n\n    - Optional:\n        >- start_date [-sd]: starting date, default will be counted from 365 days ago\n        >- maximum_day [-md]: maximum fill date per dag, rangint: [1, 180]\n        >- maximum_unit [-mu]: maxium fill unit per dag, rangint: [1, 43200]\n        >- ignore [-i]: still procceed auto fill even the dag ran recently\n        >- pause_only [-p]: pass true to fill dags which are pause\n        >- confirm [-y]: pass true to bypass the prompt if dag_id is all\n        >- traceback [-v]: pass print our Airflow Database error\n\n\n\n## Examples\n\nFill all the dags for the past 30 days without prompt, and only fill if all the dags which have status == pause\n\n```bash\n$ fakefill -d all -p -md 30 -y\n```\n\n\n\nRun fastfill for dag id == `dag_a` by counting default fakefill days == 365\n\n```bash\n$ fakefill -d dag_a\n```\n\n\n\nRun fastfill with config yaml\n\n```bash\n$ fakefill -cp config.yml\n```\n\nThe yaml file needs to be defined with two dictonary types: `dags` and `settings`. For `dags` section, it needs to be a `list`, while the `settings`section is `dict`\n\nSample:\n\n```yaml\ndags:\n  - dag_a\n  - dag_b\n  - dag_c\n\nsettings:\n  start_date: 2019-01-01\n  maximum: "365"\n  traceback: false\n  confirm: true\n  pause_only: true\n\n```\n',
    'author': 'Ben CHEN',
    'author_email': 'bn@benbenbang.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benbenbang/airflow_fakefill',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
