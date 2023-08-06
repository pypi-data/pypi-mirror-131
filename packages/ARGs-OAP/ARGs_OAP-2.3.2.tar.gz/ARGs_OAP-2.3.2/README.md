# ARGs_OAP
Python wrapper of [ARGs_OAP](https://github.com/biofuture/Ublastx_stageone)

+ linux only
+ no modification of the source code and binaries, pure wrapper

## install
+ if both python2 and python3 are installed, please explicitly specify python3
```
git clone https://github.com/xinehc/ARGs_OAP
cd ARGs_OAP
python setup.py install
```

## example
```
# git clone https://github.com/xinehc/ARGs_OAP.git
ARGs_OAP stage_one -i ARGs_OAP/example/inputfqs -m ARGs_OAP/example/meta-data.txt -o ARGs_OAP/example/output -f 'fa' -n 8
ARGs_OAP stage_two -i ARGs_OAP/example/output/extracted.fa -m ARGs_OAP/example/output/meta_data_online.txt -o ARGs_OAP/example/output -n 8
```
