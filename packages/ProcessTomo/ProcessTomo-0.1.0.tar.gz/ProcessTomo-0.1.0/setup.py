from distutils.core import setup

setup(
    name='ProcessTomo',
    version='0.1.0',
    author='Nirakar Basnet',
    author_email='nirakarbasnet@gmail.com',
    scripts=['bin/tomolist.py','bin/tomo.py','bin/rearrange_gctf','bin/organize_data.py','bin/motioncor2.py','bin/make_stack.py',
             'bin/input_parse2.py','bin/get_tomolist.py','bin/dose_info.py','bin/dose_filter.py','bin/ctf_estimate.py'],
    license='LICENSE.txt',
    description='Tomo preprocessing.',
    long_description=open('README.txt').read(),
    install_requires=[
        "Starfile",
    ],
)