from setuptools import setup
import grouping_list_tuple

with open('README.md', encoding='UTF-8') as f:
    long_description = f.read()

setup(name=grouping_list_tuple.__title__,
      author=grouping_list_tuple.__author__,
      author_email=grouping_list_tuple.__email__,
      version=grouping_list_tuple.__version__,
      description='Package for grouping array objects in list by some key',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['grouping_list_tuple'],
      license='MIT',
      python_requires='>=3.9')
