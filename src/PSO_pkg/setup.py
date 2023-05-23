from setuptools import setup

package_name = 'PSO_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vboxuser',
    maintainer_email='vboxuser@todo.todo',
    description='PSO',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'Drone = PSO_pkg.Drone:main',
                'bot_1 = PSO_pkg.Bot_1:main',
                'bot_2 = PSO_pkg.Bot_2:main',
                'bot_3 = PSO_pkg.Bot_3:main',
                'bot_4 = PSO_pkg.Bot_4:main',
                'bot_5 = PSO_pkg.Bot_5:main',
                'PSO_Node = PSO_pkg.PSONode:main',
                
        ],
    },
)
