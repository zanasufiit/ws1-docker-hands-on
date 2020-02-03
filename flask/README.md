# Dockerizacia jednoducheho Flask servera

## Problem
Mame jednoduchy http server naprogramovany v pythone s pomocou Flask microframeworku. Chceme ho nasadit na vzdialeny server.

### Sucasny stav
Aby sme to vedeli vykonat teraz tak musime zarucit, ze na cielovom prostredi bude:

1. spravna verzia pythonu
2. nejaky virtual environment pre izolaciu potrebnych kniznic
3. vyriesit kam pojdu logy, a ako sa bude aplikacia spustat

Odsimulujeme si vzdialene prostredie lokalne. Predpokladame, ze python uz mame nainstalovany.

Co teraz?

### Lokalne spustenie
Aplikacia je jednoducha a obsahuje iba jeden subor `app.py`.

Vyskusame ju zapnut

```
PS> python .\app.py
Traceback (most recent call last):
  File ".\app.py", line 1, in <module>
    from flask import Flask
ModuleNotFoundError: No module named 'flask'
```

Samozrejme to nefunguje lebo sme nenainstalovali potrebny python balik. Standardne sa to riesi lokalny virtual environment (nechceme si instalovat baliky do globalneho pythonu).

```
PS> python -m venv venv
PS> .\venv\Scripts\activate
```

pre bash (?)
```
source venv/Scripts/activate
```

Teraz si nainstalujeme potrebny balik a exportujeme si zoznam balikov do `requirements.txt`

```
pip install flask
pip freeze > requirements.txt
```
A skusime znovu spustit nas server.

```
(venv) PS> python .\app.py
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 ```

Zrazu to uz funguje (mozeme si overit na http://localhost:5000/) a rovnake kroky je nutne vykonat aj na serveri kde by sme to chceli nasadit.

Pri upgrade na novu verziu je nutne adminom dat vsetky subory. Teda zdrojaky aplikacie a aj `requirements.txt` a dufat, ze vsetko sa podari nainstalovat.

Stym, ze je nutne riesit napr. logy na urovni aplikacie resp. OS.

## Dockerizacia
Ok. Kontajnery su vraj super a vedia nam pomoct vyriesit problemy. Ako sa zmeni tento proces ak budeme mat dockerizovanu aplikaciu?

### Poziadavky na server

1. nainstalovany docker
2. pristup k nasej docker registry (ak by bola privatna)

### Ako na to?

Ako prve si musime vytvorit Dockerfile najjednoduchsie je pouzit python base image.

```Dockerfile
FROM python:3.8.1-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

ENTRYPOINT ["python", "app.py"]
```

Vytvorime image pomocou `docker build`

```
(venv) PS> docker build . -t zanasufiit/handson-flask
Sending build context to Docker daemon  27.69MB
Step 1/6 : FROM python:3.8.1-slim-buster
3.8.1-slim-buster: Pulling from library/python
bc51dd8edc1b: Pull complete
dc4aa7361f66: Pull complete
f7d31f0d4202: Pull complete
edfb78ef674e: Pull complete
20cf94536d56: Pull complete
Digest: sha256:42cc96229ec610d84fe9c9de5c77ceaa97ea1f4d980e9bad90ef39eae63ded8b
Status: Downloaded newer image for python:3.8.1-slim-buster
 ---> 2454b9521053
Step 2/6 : WORKDIR /app
 ---> Running in 3c32b31ed2e1
Removing intermediate container 3c32b31ed2e1
 ---> 209a7f2f4b53
Step 3/6 : COPY requirements.txt .
 ---> 7f3c1abf2b2f
Step 4/6 : RUN pip install -r requirements.txt
 ---> Running in 35857f9d5d5f
Collecting Click==7.0
  Downloading Click-7.0-py2.py3-none-any.whl (81 kB)
Collecting Flask==1.1.1
  Downloading Flask-1.1.1-py2.py3-none-any.whl (94 kB)
Collecting itsdangerous==1.1.0
  Downloading itsdangerous-1.1.0-py2.py3-none-any.whl (16 kB)
Collecting Jinja2==2.11.1
  Downloading Jinja2-2.11.1-py2.py3-none-any.whl (126 kB)
Collecting MarkupSafe==1.1.1
  Downloading MarkupSafe-1.1.1-cp38-cp38-manylinux1_x86_64.whl (32 kB)
Collecting Werkzeug==0.16.1
  Downloading Werkzeug-0.16.1-py2.py3-none-any.whl (327 kB)
Installing collected packages: Click, Werkzeug, itsdangerous, MarkupSafe, Jinja2, Flask
Successfully installed Click-7.0 Flask-1.1.1 Jinja2-2.11.1 MarkupSafe-1.1.1 Werkzeug-0.16.1 itsdangerous-1.1.0
Removing intermediate container 35857f9d5d5f
 ---> 956144bff121
Step 5/6 : COPY app.py .
 ---> 750d91dafcc9
Step 6/6 : ENTRYPOINT ["python", "app.py"]
 ---> Running in 142b25eee25d
Removing intermediate container 142b25eee25d
 ---> 6899d1514d90
Successfully built 6899d1514d90
Successfully tagged zanasufiit/handson-flask:latest
```

Teraz mame vytvoreny docker image `zanasufiit/handson-flask` s tagom `latest`. Tento image obsahuje vsetko co nasa aplikacia potrebuje. Vsetky kniznice, python a od cieloveho miesta vyzaduje iba docker (a linux).

Podme si ju spustit.

`--rm` zaruci, ze sa kontajner po ukonceni zmaze a nebude zaberat miesto.

```
PS> docker run --rm zanasufiit/handson-flask:latest
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

Podme otvorit http://localhost:5000/

...

Nejde to, preco? Kontajner si zije vo svojom izolovanom svete, co teraz? Vyuzijeme moznost smerovanie portov pomocou prepinaca `-p`. 


```
PS> docker run --rm -p 44444:5000 zanasufiit/handson-flask:latest
```

`-p 44444:5000` znamena, ze port 44444 na nasom pocitaci bude smerovat na port `5000` v kontajneri.

Vyskusame a zrazu nam to funguje.

```
(venv) PS> docker run --rm -p 44444:5000 zanasufiit/handson-flask:latest
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
172.17.0.1 - - [03/Feb/2020 22:38:53] "GET / HTTP/1.1" 200 -
172.17.0.1 - - [03/Feb/2020 22:38:53] "GET /favicon.ico HTTP/1.1" 404 -
```

Ok. mame image lokalne, co teraz? Spomenme si na registry. V tomto pripade pouzijeme Docker Hub

- kto ma Win/Mac je urcite registrovany
- viete mat neobmedzene verejnych repozitarov
- skuste si vytvorit vlastny repozitar https://hub.docker.com/repository/create
- vykonajte `docker login`

Za predpokladu, ze vase meno je `znf` a repozitar ste nazvali `workshop-flask` tak mozeme teraz tagnut (ako keby skopirovat s novym menom) image.

```
docker tag zanasufiit/handson-flask znf/workshop-flask
```

Teraz mame 'novy' image s nazvom znf/workshop-flask ak ho chceme pushnut do registry tak staci spustit (v nasom pripade).

```
(venv) PS> docker push zanasufiit/handson-flask
The push refers to repository [docker.io/zanasufiit/handson-flask]
70a5824be261: Pushed
86af4de2582e: Pushed
c5906d001c46: Pushed
ea470e26bd55: Pushed
f881dc6a31f5: Mounted from library/python
3881a40200ec: Mounted from library/python
ad799e1faee3: Mounted from library/python
cb82f398d4bd: Mounted from library/python
488dfecc21b1: Mounted from library/python
latest: digest: sha256:2148bd57391a88bd1e3508f679dc657973793d6574acbc5e7998164c0b2ba1b0 size: 2202
```

Pekne je vidiet ako sa znovupouzili uz existujuce vrstvy z python image a my sme realne pushli iba nase nove vrstvy.

Vymazme si image z lokalneho uloziska

```
(venv) PS> docker image rm zanasufiit/handson-flask
Untagged: zanasufiit/handson-flask:latest
Untagged: zanasufiit/handson-flask@sha256:2148bd57391a88bd1e3508f679dc657973793d6574acbc5e7998164c0b2ba1b0
```

A teraz skusme znova spustit nasu aplikaciu (nahradte nazov imagu za to co ste prave pushli)

```
(venv) PS> docker run --rm -p 44444:5000 zanasufiit/handson-flask:latest
Unable to find image 'zanasufiit/handson-flask:latest' locally
latest: Pulling from zanasufiit/handson-flask
Digest: sha256:2148bd57391a88bd1e3508f679dc657973793d6574acbc5e7998164c0b2ba1b0
Status: Downloaded newer image for zanasufiit/handson-flask:latest
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

Hotovo nasa python aplikacia je dockerizovana a adminovi, ktory spravuje nas server staci poslat informaciu o tom ako ju nakonfigurovat (napr. na akom porte pocuva) a kde najde image (t.j. `zanasufiit/handson-flask:latest`). Nemusi riesit ziadny python, ziadne kniznice....
