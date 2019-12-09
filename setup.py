import setuptools
import re

short_desc = (
    'Steinhart -- Hart and Beta thermistor temperature model in '
    'Python and C. Implementation and utilities'
)

with open("README.md") as fh:
    raw_url = 'https://gitlab.com/geusebi/thermistor-utils/raw/master/'

    ref_re = re.compile("\[(.+?)]: *(.+?)")
    img_re = re.compile("!\[(.+?)] *\((.+?)\)")
    long_desc = ref_re.sub(f"[\\1]: {raw_url}\\2", fh.read())
    long_desc = img_re.sub(f"![\\1]({raw_url}\\2)", long_desc)

setuptools.setup(
    name='thermistor_utils',
    version='0.0.3',
    packages=('thermistor_utils', ),

    description=short_desc,
    long_description=long_desc,
    long_description_content_type='text/markdown',

    # url git
    url='https://gitlab.com/geusebi/thermistor-utils',

    python_requires='>=3.6',
    install_requires=tuple(),

    author='Giampaolo Eusebi',
    author_email='giampaolo.eusebi@gmail.com',

    license='GNU LGPL 3.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: C',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Utilities',
    ],
)
