from setuptools import find_packages, setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')


# calling the setup function
setup(name='textual_name_analyzer',
      version='0.1.0',
      author='Zhihao Lin',
      author_email='zhihaolinsde@gmail.com',
      description='A framework to analyze textual name',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/LinZhihaozlin22/textual_name_analyzer',
      license='MIT',
      packages=find_packages(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
      ],
      install_requires=['boto3','DeepFace','botocore','BeautifulSoup4','requests'],
      keywords='name gender ethic',
      python_requires=">=3.5"
      )
