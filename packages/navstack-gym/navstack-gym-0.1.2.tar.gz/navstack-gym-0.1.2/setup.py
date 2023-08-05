# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['navstack_gym']

package_data = \
{'': ['*']}

install_requires = \
['descartes>=1.1.0,<2.0.0',
 'gym>=0.21.0,<0.22.0',
 'matplotlib>=3.5.0,<4.0.0',
 'nav-sim-modules>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'navstack-gym',
    'version': '0.1.2',
    'description': '',
    'long_description': "# navstack-gym\nSimulation environment of task with autonomous mobile robot using Navigation Stack.\n\n\n<img src='https://user-images.githubusercontent.com/41321650/145752733-cb9f80d7-2647-464f-8ee6-57ee3e53dbf2.png' width=100%>\n\nIn this environment, the agent do action of instructing relative navigation goal pose and observe a subjective occupancy map.\n\n<img src='https://user-images.githubusercontent.com/41321650/145782630-5cda4862-948c-4995-9739-ca002a77ae68.GIF' width=100%>\n\n\n## Implemented Task\n`TreasureChestRoom` :   \nAgent aim to open chests in unknown rooms with keys and discover as much treasure as possible.\n\nThe rooms in which agent spawned are randomly generated such as the following structure.\n\nYellow cube is key, and cyan cube is treasure chest. Each object will be generated based on different set of placing rules.\n\n<img src='https://user-images.githubusercontent.com/41321650/144612303-07df02c0-b4af-46e0-8eea-36d905246f76.png' width=100%>\n\n\n## Installation\n\n```\npip install navstack-gym\n```\n\n## Usage\n\nI'll add the note later.\n\nexample:\n\n```python\nimport gym\nimport navstack_gym\n\nenv = gym.make('TreasureChestRoom-v0')\nobs = env.reset(is_generate_pose=True, is_generate_room=True, obstacle_count=13)\n\nimgs = []\nimgs.append(env.render('rgb_array'))\n\nfor i in range(10):\n    action = env.action_space.sample()\n    obs, reward, done, info = env.step(action)\n    imgs.append(env.render('rgb_array'))\n```\n\n<img src='https://user-images.githubusercontent.com/41321650/145789880-f8bfd475-5ebd-4321-8406-5472985f1b97.gif' width=100%>\n",
    'author': 'Reona Sato',
    'author_email': 'www.shinderu.www@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wwwshwww/navstack-gym',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
