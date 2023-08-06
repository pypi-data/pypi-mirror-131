# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['GPIOLibrary',
 'GPIOLibrary.keywords',
 'GPIOLibrary.mocks',
 'GPIOLibrary.mocks.RPi',
 'utests']

package_data = \
{'': ['*']}

install_requires = \
['robotframework']

setup_kwargs = {
    'name': 'robotframework-gpio',
    'version': '0.2.0',
    'description': "Robot Framework Library for interfacing GPIO pins on executing robot files on Raspberry Pi's. ",
    'long_description': "# GPIOLibrary\n\n![pypi-badge](https://img.shields.io/pypi/v/robotframework-gpio)\n[![build](https://github.com/yusufcanb/robotframework-gpio/actions/workflows/python-build.yml/badge.svg?branch=master)](https://github.com/yusufcanb/robotframework-gpio/actions/workflows/python-build.yml)\n![stable](https://img.shields.io/static/v1?label=status&message=stable&color=green)\n\n\nRobot Framework Library for interfacing GPIO pins on executing robot files on Raspberry Pi's.\n\nFor Library documentation you can visit; [https://yusufcanb.github.io/robotframework-gpio/](https://yusufcanb.github.io/robotframework-gpio/)\n\n## Requirements\n\n- [Robot Framework (^3.2.2) ](https://pypi.org/project/robotframework/)\n- [RPi.GPIO (^0.7.0)](https://pypi.org/project/RPi.GPIO/)\n\n## Installation\n\nInstall [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) with command below;\n\n```\npip install RPi.GPIO\n```\n\nThen install GPIOLibrary with;\n\n```shell\npip install robotframework-gpio\n```\n\n\n## Examples\n\nYou can find example robot files in the `/examples` directory.\n\n### Basic Usage\n\n```robot\n*** Settings ***\n\nDocumentation   Test LED is fully functional\nLibrary                     GPIOLibrary\nSuite Setup                 Begin GPIO Test\n\n*** Variables ***\n\n${LED_PIN}                  17\n\n*** Test Cases ***\n\nLED Should On\n    Set Output Pin                  ${LED_PIN}\n    Set Pin High                    ${LED_PIN}\n    ${pin_status}=                  Get Pin Status      ${LED_PIN}\n    Should Be Equal As Integers     ${pin_status}       1\n\nLED Should Off\n    Set Output Pin                  ${LED_PIN}\n    Set Pin Low                     ${LED_PIN}\n    ${pin_status}=                  Get Pin Status      ${LED_PIN}\n    Should Be Equal As Integers     ${pin_status}       1\n \n*** Keywords ***\n\nBegin GPIO Test\n    Set Mode                        BCM\n    Set Warnings Off\n```\n\n\n### Remote Library\xa0Usage\n\nFirst install robotframework/PythonRemoteServer to Raspberry Pi;\n\n```\npip install robotremoteserver\n```\n\n\nThen, start remote library server with following commands;\n\n```python\nfrom robotremoteserver import RobotRemoteServer\nfrom GPIOLibrary import GPIOLibrary\n\nRobotRemoteServer(GPIOLibrary(), host='0.0.0.0')\n```\n\nFinally, you can execute the robot file below from any machine within the same network of Raspberry Pi.\n\n\n``` robot\n*** Settings ***\n\nDocumentation                       Example robot file for using GPIOLibrary on a remote Raspberry Pi device\n\nLibrary                             Remote      http://${ADDRESS}:${PORT}\nLibrary                             Dialogs\nSuite Setup                         Begin GPIO Test\n\n*** Variables ***\n\n${ADDRESS}                          raspberrypi.local\n${PORT}                             8270\n\n${LED_PIN}                          17\n\n*** Test Cases ***\n\nLED Should On\n    Set Output Pin                  ${LED_PIN}\n    Set Pin High                    ${LED_PIN}\n    Execute Manual Step             LED is on?\n    \n\nLED Should Off\n    Set Output Pin                  ${LED_PIN}\n    Set Pin Low                     ${LED_PIN}\n    Execute Manual Step             LED is off?\n \n*** Keywords ***\n\nBegin GPIO Test\n    Set Mode                        BCM\n    Set Warnings Off\n\n```\n",
    'author': 'Yusuf Can Bayrak',
    'author_email': 'yusufcanbayrak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
