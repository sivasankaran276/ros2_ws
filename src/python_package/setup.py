from setuptools import find_packages, setup

package_name = 'python_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='siva',
    maintainer_email='siva@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "template_node=python_package.template:main",
            "pub_num=python_package.pub:main",
            "pub_number=python_package.pub1:main",
            "pub2_num=python_package.pub2:main",
            "pub3_num=python_package.pub3:main",
            "sub_str=python_package.sub:main",
            "pubtemp_num=python_package.pubtemp:main",
            "subtemp_num=python_package.subtemp:main",
            "publisher=python_package.publisher:main",
            "subscriber=python_package.subscriber:main",
            "turtlebot=python_package.turtlebot:main",
            "turtle=python_package.turtle:main",
            "turtlecir=python_package.turtlecir:main",
            "subturtle=python_package.subturtle:main",
            "turpublisher=python_package.turpublisher:main",
            "service=python_package.service:main",
            "client=python_package.client:main",
            "goaltogo=python_package.goaltogo:main",
            "spawn=python_package.spawn:main",
            "turspawn=python_package.turspawn:main",
            "turspasub=python_package.turspasub:main",
            "rectangle=python_package.rectangle:main",
            "rectangleser=python_package.rectangleser:main",
            "turspasub2=python_package.turspasub2:main",
        ],
    },
)
