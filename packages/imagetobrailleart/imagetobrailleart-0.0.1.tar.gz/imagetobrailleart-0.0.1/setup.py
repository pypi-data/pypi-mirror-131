from setuptools import setup,find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
    name="imagetobrailleart",
    version="0.0.1",
    description="To convert any image into braille art",
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    py_modules=["imagetobrailleart"],
    package_dir={' ' :'src'},
    author='Yash Chauhan',
    author_email='chauhanyash1029@gmail.com',
    license='MIT', 
    classifiers=classifiers,
    keywords=['braille', 'art', 'openCV'], 
    packages=find_packages(),
    install_requires=['opencv-python', 'Pillow'] 
)