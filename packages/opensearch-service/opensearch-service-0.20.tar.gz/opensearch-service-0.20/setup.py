from setuptools import setup
import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name='opensearch-service',
      version='0.20',
      description='easy access to OpenSearch based on opensearch-dsl',
      url='https://github.com/bertrandchevrier/opensearch-service.git',
      author='The data handyman team',
      author_email='chevrierbertrand@yahoo.fr',
      license='MIT',
      classifiers=['Development Status :: 3 - Alpha'],
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=['opensearch_service'],
      install_requires=[
          'opensearch','opensearch-dsl','pandas'
      ],
      include_package_data=True,
      zip_safe=False,
      python_requires='>=3.5')