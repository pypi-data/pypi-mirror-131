# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qualang_tools', 'qualang_tools.bakery', 'qualang_tools.config']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.20.3,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'qm-qua>=0.3.2,<0.4.0',
 'scipy>=1.7.1,<2.0.0']

setup_kwargs = {
    'name': 'qualang-tools',
    'version': '0.4.0',
    'description': 'The qualang_tools package includes tools for writing QUA programs in Python.',
    'long_description': '# qualang_tools\n\nThe qualang_tools package includes tools for facilitating writing of QUA programs and configurations in Python. \n\nIt includes:\n\n- The baking tool which allows defining waveforms in a QUA-like manner with for working with a 1ns resolution.  It can also be used to create even higher resolution waveforms.\n- Tools for converting a list of integration weights into the format used in the configuration.\n- Tools for creating waveforms commonly used in Quantum Science.\n- Tools for correcting mixer imbalances.\n\n## Installation\n\nInstall the current version using `pip`, the `--upgrade` flag ensures that you will get the latest version \n\n```\npip install --upgrade qualang-tools\n```\n\n## Usage\n\nExamples for 1-qubit randomized benchmarking, cross-entropy benchmark (XEB), high sampling rate baking and more  can be found in the examples folder of the [py-qua-tools repository](https://github.com/qua-platform/py-qua-tools/)\n\n\n',
    'author': 'QM',
    'author_email': 'qua-libs@quantum-machines.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/qua-platform/py-qua-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
