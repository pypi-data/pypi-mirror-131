# bfa-fiscal

## Instrucciones de instalación

1) Comentar la línea 362 del archivo /etc/ssl/openssl.cnf donde dice:
```
CipherString = DEFAULT@SECLEVEL=2
```

1) Instalar python3-m2crypto, pip3:

```
# echo "deb http://deb.debian.org/debian buster-backports main" >> /etc/apt/sources.list

# apt update

# apt install python3-m2crypto python3-pip python3-httplib2
```

*Opcional*: Desisntalar python3-pysimplesoap

```
# apt purge -y python3-pysimplesoap && apt autoremove -y
```


3) Configurar pip3 para utilizar [devpi.basisty.com](http://devpi.basisty.com):

* Crear archivo /etc/pip.conf:
```
[global]
index_url = http://devpi.basisty.com/gbasisty/default/+simple/
trusted-host = devpi.basisty.com

[search]
index = http://devpi.basisty.com/gbasisty/default/
```
x) Desplegar nueva version Insalar **devpi** 

```
#pip3 install devpi
#devpi use http://devpi.basisty.com/gbasisty/default/+simple/
```


4) Instalar **bfa-fiscal**:
```
# pip3 install bfa-fiscal
```