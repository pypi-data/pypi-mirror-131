from setuptools import setup

setup(
      name= 'testilo',
      version='0.0.3',
      author="ilo robot (SLB)",
      author_email="<ilotherobot@gmail.com>",
      url="https://github.com/ilorobot/python-library",
      description='lib test for ilo',
      py_modules=["print_ilo"],
      package = ['src'],
      package_dir={'':'src'},
      )