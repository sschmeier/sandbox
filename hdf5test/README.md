# PROJECT: poreqc
AUTHOR: Sebastian Schmeier (s.schmeier@gmail.com) 
DATE: 2017-10-30

## INSTALL

```bash
# Install miniconda
# LINUX:
curl -O https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
bash Miniconda2-latest-Linux-x86_64.sh
# MACOSX:
curl -O https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh
bash Miniconda2-latest-MacOSX-x86_64.sh

# Add conda dir to PATH
echo 'export PATH="~/miniconda2/bin:$PATH"' >> ~/.bashrc

# Install bioconda
conda config --add channels conda-forge
conda config --add channels defaults
conda config --add channels r
conda config --add channels bioconda

# Make env
conda create --name poreqc --file conda-packages.txt
source activate poreqc
```


