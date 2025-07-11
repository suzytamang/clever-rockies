# README.md

## Assumptions

- Using python=3.11

## Supporting Changes

- ```.gitignore``` updated to exclude ```.\envs```, the intended folder for clever-rockies python environment.

## Python Environment (If Anaconda Available)

### How to Create Environment

The following command will create a local virutal environment at ```.\envs\vaParts```.  The ```.\envs\environment.yml``` file uses **conda** to create the environment **pip** to install packages.

```shell
# Run to create python environment
conda create -p .\envs\vaParts -f .\envs\environment.yml
```

### Breakdown of 

#### Channels

The VA will not allow use of the ```default``` channel, but ```conda-forge``` is fine.  

The ```envs/environment.yml``` file is set up to create a python environment with ```conda-forge``` set as the default channel.

```shell
# Information Only
conda config --remove channels defaults
conda config --remove channels main
conda config --remove channels anaconda
conda config --add channels conda-forge
conda config --set channel_priority strict
```

#### Automatic "yes" on Package Install

I have also updated the config to always answer "yet" for adding packages.

```shell
# Information Only
conda config --show always_yes
```

#### Environemnt Export

The ```envs/environment.yml``` created with

```shell
# Information Only
conda env export > envs\environment.yml
```

#### Example ```envs/environment.yml```

```yml
name: vaParts
channels:
  - conda-forge
dependencies:
  - bzip2=1.0.8=h2466b09_7
  - ca-certificates=2025.7.9=h4c7d964_0
  - libexpat=2.7.0=he0c23c2_0
  - libffi=3.4.6=h537db12_1
  - liblzma=5.8.1=h2466b09_2
  - libsqlite=3.50.2=hf5d6505_2
  - libzlib=1.3.1=h2466b09_2
  - openssl=3.5.1=h725018a_0
  - pip=25.1.1=pyh8b19718_0
  - python=3.11.13=h3f84c4b_0_cpython
  - setuptools=80.9.0=pyhff2d567_0
  - tk=8.6.13=h2c6b04d_2
  - ucrt=10.0.22621.0=h57928b3_1
  - vc=14.3=h41ae7f8_26
  - vc14_runtime=14.44.35208=h818238b_26
  - wheel=0.45.1=pyhd8ed1ab_1
  - pip:
      - attrs==25.3.0
      - certifi==2025.7.9
      - charset-normalizer==3.4.2
      - distlib==0.3.9
      - filelock==3.18.0
      - idna==3.10
      - joblib==1.5.1
      - jsonschema==4.24.0
      - jsonschema-specifications==2025.4.1
      - lockfile==0.12.2
      - msgpack==1.1.1
      - numpy==2.3.1
      - packaging==25.0
      - pandas==2.3.1
      - py4j==0.10.9.9
      - pyspark==4.0.0
      - python-dateutil==2.9.0.post0
      - pytz==2025.2
      - referencing==0.36.2
      - requests==2.32.4
      - rpds-py==0.26.0
      - scikit-learn==1.7.0
      - scipy==1.16.0
      - six==1.17.0
      - threadpoolctl==3.6.0
      - trove-classifiers==2025.5.9.12
      - typing-extensions==4.14.1
      - tzdata==2025.2
      - urllib3==1.26.20
      - webencodings==0.5.1
prefix: X:\_\tools\anaconda3\envs\vaParts

```

## Python Environment (If Anaconda *Not* Available)

### How to Create Environment

Create a local environment using 

```shell
python -m venv .\envs\vaParts
```

Activate the environment and add requirements.

```shell
.envs\vaParts\Scripts\activate
```

Update the environment using ```.\envs\requirements.txt```.

```shell
python -m pip install -r .\envs\requirements.txt
```

### Example requirements.txt file

```
attrs==25.3.0
certifi==2025.7.9
charset-normalizer==3.4.2
distlib==0.3.9
filelock==3.18.0
idna==3.10
joblib==1.5.1
jsonschema==4.24.0
jsonschema-specifications==2025.4.1
lockfile==0.12.2
msgpack==1.1.1
numpy==2.3.1
packaging==25.0
pandas==2.3.1
py4j==0.10.9.9
pyspark==4.0.0
python-dateutil==2.9.0.post0
pytz==2025.2
referencing==0.36.2
requests==2.32.4
rpds-py==0.26.0
scikit-learn==1.7.0
scipy==1.16.0
six==1.17.0
threadpoolctl==3.6.0
trove-classifiers==2025.5.9.12
typing_extensions==4.14.1
tzdata==2025.2
urllib3==1.26.20
webencodings==0.5.1
```