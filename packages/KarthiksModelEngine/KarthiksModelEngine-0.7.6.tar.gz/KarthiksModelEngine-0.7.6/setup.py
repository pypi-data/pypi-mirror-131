from setuptools import setup, find_packages
def readme():
    with open('README.md') as f:
        README=f.read()
    return README

setup(
      name="KarthiksModelEngine",
      version="0.7.6",
      description='Just an another Python Package with SuperMachine Abilities',
      long_description= readme(),
      keywords=['Automl','Supervised Learning',],
      long_description_content_type='text/markdown',
      url='https://github.com/import666/Karthiks_Model_Engine',
      author='Karthik Devalla',
      author_email='ihatecoding666@gmail.com',
       classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
      install_requires=['pandas','numpy','scikit-learn','scikit-optimize','matplotlib','xgboost','h5py','gdown',],
      packages=find_packages('KME'),
      package_dir={'': 'KME',
      },
      include_package_data=True,
      data_files= None,
      python_requires=">=3.6",
      )