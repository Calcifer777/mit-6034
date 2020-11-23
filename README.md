# mit-6034


## Run python 2.6

```bash
wget https://www.python.org/ftp/python/2.6.7/Python-2.6.7.tgz
tar -zxvf Python-2.6.7.tgz
cd Python-2.6.7
mkdir $HOME/.localpython267
./configure --prefix=$HOME/.localpython267
make
make install
```

```bash
cd ~/src
wget https://files.pythonhosted.org/packages/d8/5f/9025f456f39ef825719d2b30090e240b382dcb4dcb3d0429b18c13176c98/virtualenv-14.0.4.tar.gz
tar -zxvf virtualenv-14.0.4.tar.gz
cd virtualenv-14.0.4/
~/.localpython267/bin/python setup.py install
virtualenv venv -p $HOME/.localpython267/bin/python2.6
source venv/bin/activate
```
