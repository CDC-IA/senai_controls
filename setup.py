from setuptools import find_packages, setup

package_name = 'senai_controls'

def packages():
    pkg = find_packages(exclude=['test'])
    pkg.append(package_name)
    pkg.append(f'{package_name}.tests')

    return pkg

setup(
    name=package_name,
    version='0.0.0',
    packages=packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='gilmar',
    maintainer_email='gilmar.jeronimo@sp.senai.br',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'draw_square = senai_controls.tests.draw_square:main' 
        ],
    },
)
