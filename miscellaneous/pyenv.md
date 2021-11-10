# Working with pyenv and virtualenvwrapper

## Install
```bash
 # install brew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" 

# install pyenv 
brew install pyenv 
# install pyenv-virtualenv if needed
brew install pyenv-virtualenv 

# virtualenvwrapper 
pip3 install virtualenvwrapper
```

### Add to ~/.zshrac
```bash
# pyenv & pyenv-virtualenv
export PATH="$HOME/.pyenv/bin:$PATH"
export PATH="/usr/local/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
export LDFLAGS="-L/usr/local/opt/zlib/lib -L/usr/local/opt/bzip2/lib"
export CPPFLAGS="-I/usr/local/opt/zlib/include -I/usr/local/opt/bzip2/include"

alias pyenv-install="CFLAGS=-Wno-implicit-function-declaration pyenv install"  # error to install pyenv versions workaround
alias python=/usr/local/bin/python3.9  # system python version
alias python3.6="/Users/romanhartmann/.pyenv/versions/3.6.13/bin/python3.6"
alias python3.8="/Users/romanhartmann/.pyenv/versions/3.8.9/bin/python3.8"

# virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/work_folder  # update to where your work is
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3.9  # system python version used by pip3 and aliased to 'python' above
source /usr/local/bin/virtualenvwrapper.sh  # `which virtualenvwrapper.sh`
```

```bash
pyenv-install 3.6.13
pyenv-install 3.8.9
```


## Usage:


```bash
pyenv versions
ls ~/.pyenv/versions
pyenv install 3.8.7
pyenv install 3.6.13
```

```bash
mkvirtualenv --python ~/.pyenv/versions/3.6.13/bin/python myvirtualenv

```
