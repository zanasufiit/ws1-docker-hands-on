# layers v dockerfile

Kazda instrukcia vytvara docasny kontajner v ktorom sa vykonava build krok. Instrukcie `RUN`, `ADD` `COPY` menia velkost imagu.

Ukazeme si to na priklade:

Mame jednoduchy Dockerfile:
```Dockerfile

# zaklad je ubuntu image s labelom 18.04
FROM ubuntu:18.04

# kde je nas workdir v image
WORKDIR /app

# skopiruje subor do workdiru
COPY file1.txt .

# skopiruje subor do workdiru
COPY file2.txt .
```

Zbuildime si tento image pomocou (terminal do priecinka `ukazka-layers`):

```bash
docker build . -t zanasufiit/ws-ukazka-layers
```

Vysledok by sa mal podobat na toto:
```
Sending build context to Docker daemon  9.728kB
Step 1/4 : FROM ubuntu:18.04
18.04: Pulling from library/ubuntu
5c939e3a4d10: Pull complete
c63719cdbe7a: Pull complete
19a861ea6baf: Pull complete
651c9d2d6c4f: Pull complete
Digest: sha256:8d31dad0c58f552e890d68bbfb735588b6b820a46e459672d96e585871acc110
Status: Downloaded newer image for ubuntu:18.04
 ---> ccc6e87d482b
Step 2/4 : WORKDIR /app
 ---> Running in a8a572b8931f
Removing intermediate container a8a572b8931f
 ---> 8648033e3814
Step 3/4 : COPY file1.txt .
 ---> 48e405405478
Step 4/4 : COPY file2.txt .
 ---> b6b55c7d5812
Successfully built b6b55c7d5812
Successfully tagged zanasufiit/ws-ukazka-layers:latest
```

Vidime, ze `Step 2/4` hovori o vymazani docasneho kontajnera ale pri `COPY` krokoch to uz tak nie je.

Ak teraz zmenime subor `file2.txt` a znova spustime build ale tentokrat

```bash
docker build . -t zanasufiit/ws-ukazka-layers-2
```

```
Sending build context to Docker daemon  9.728kB
Step 1/4 : FROM ubuntu:18.04
 ---> ccc6e87d482b
Step 2/4 : WORKDIR /app
 ---> Using cache
 ---> 8648033e3814
Step 3/4 : COPY file1.txt .
 ---> Using cache
 ---> 48e405405478
Step 4/4 : COPY file2.txt .
 ---> 5a78fad6e7d9
Successfully built 5a78fad6e7d9
Successfully tagged zanasufiit/ws-ukazka-layers-2:latest
```

Teraz pouzijeme `docker history`, ktory zobrazuje historiu imagu.
```
PS> docker history zanasufiit/ws-ukazka-layers
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
b6b55c7d5812        2 minutes ago       /bin/sh -c #(nop) COPY file:a9e64b3acd14e87f…   13B
48e405405478        2 minutes ago       /bin/sh -c #(nop) COPY file:25b74a870995f39f…   9B
8648033e3814        2 minutes ago       /bin/sh -c #(nop) WORKDIR /app                  0B
ccc6e87d482b        2 weeks ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>           2 weeks ago         /bin/sh -c mkdir -p /run/systemd && echo 'do…   7B
<missing>           2 weeks ago         /bin/sh -c set -xe   && echo '#!/bin/sh' > /…   745B
<missing>           2 weeks ago         /bin/sh -c [ -z "$(apt-get indextargets)" ]     987kB
<missing>           2 weeks ago         /bin/sh -c #(nop) ADD file:08e718ed0796013f5…   63.2MB
PS> docker history zanasufiit/ws-ukazka-layers-2
IMAGE               CREATED              CREATED BY                                      SIZE                COMMENT
5a78fad6e7d9        About a minute ago   /bin/sh -c #(nop) COPY file:527f8794f21513c0…   14B
48e405405478        2 minutes ago        /bin/sh -c #(nop) COPY file:25b74a870995f39f…   9B
8648033e3814        2 minutes ago        /bin/sh -c #(nop) WORKDIR /app                  0B
ccc6e87d482b        2 weeks ago          /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>           2 weeks ago          /bin/sh -c mkdir -p /run/systemd && echo 'do…   7B
<missing>           2 weeks ago          /bin/sh -c set -xe   && echo '#!/bin/sh' > /…   745B
<missing>           2 weeks ago          /bin/sh -c [ -z "$(apt-get indextargets)" ]     987kB
<missing>           2 weeks ago          /bin/sh -c #(nop) ADD file:08e718ed0796013f5…   63.2MB
```

Ak si pozrieme prvy stlpec tak vidime, ze rozdiel je iba v poslednej vrstve ostatne sa znovupouzivaju.

Tentokrat zmenime `file.txt` a `file2.txt` nechame tak.

```
Sending build context to Docker daemon  10.75kB
Step 1/4 : FROM ubuntu:18.04
 ---> ccc6e87d482b
Step 2/4 : WORKDIR /app
 ---> Using cache
 ---> 8648033e3814
Step 3/4 : COPY file1.txt .
 ---> 79bbab28e4d6
Step 4/4 : COPY file2.txt .
 ---> e76150211fa7
Successfully built e76150211fa7
Successfully tagged zanasufiit/ws-ukazka-layers-3:latest
```

Vidime, ze tento krat sa zmenil aj 3. aj 4. krok. Teda ak sa zmeni nejaky layer tak sa zmenia aj vsetky za nim.

Teraz si odsimulujeme znovupouzitie nasho base image. Pouzijeme na to `Dockerfile-reuse` v tomto priecinku.

```Dockerfile
FROM zanasufiit/ws-ukazka-layers-3

COPY file3.txt .
```

```bash
docker build . -f Dockerfile-reuse -t zanasufiit/ws-ukazka-layers-reuse
```

```
Sending build context to Docker daemon  11.78kB
Step 1/2 : FROM zanasufiit/ws-ukazka-layers-3
 ---> e76150211fa7
Step 2/2 : COPY file3.txt .
 ---> 7cd236f16033
Successfully built 7cd236f16033
Successfully tagged zanasufiit/ws-ukazka-layers-reuse:latest
```

Teraz si porovnajme `zanasufiit/ws-ukazka-layers-3` a `zanasufiit/ws-ukazka-layers-reuse`.

```
PS> docker history zanasufiit/ws-ukazka-layers-3
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
e76150211fa7        3 minutes ago       /bin/sh -c #(nop) COPY file:527f8794f21513c0…   14B
79bbab28e4d6        3 minutes ago       /bin/sh -c #(nop) COPY file:4e042e3d98545f89…   10B
8648033e3814        9 minutes ago       /bin/sh -c #(nop) WORKDIR /app                  0B
ccc6e87d482b        2 weeks ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>           2 weeks ago         /bin/sh -c mkdir -p /run/systemd && echo 'do…   7B
<missing>           2 weeks ago         /bin/sh -c set -xe   && echo '#!/bin/sh' > /…   745B
<missing>           2 weeks ago         /bin/sh -c [ -z "$(apt-get indextargets)" ]     987kB
<missing>           2 weeks ago         /bin/sh -c #(nop) ADD file:08e718ed0796013f5…   63.2MB
PS> docker history zanasufiit/ws-ukazka-layers-reuse
IMAGE               CREATED              CREATED BY                                      SIZE                COMMENT
7cd236f16033        About a minute ago   /bin/sh -c #(nop) COPY file:c3d7044c79885dec…   5B
e76150211fa7        3 minutes ago        /bin/sh -c #(nop) COPY file:527f8794f21513c0…   14B
79bbab28e4d6        3 minutes ago        /bin/sh -c #(nop) COPY file:4e042e3d98545f89…   10B
8648033e3814        9 minutes ago        /bin/sh -c #(nop) WORKDIR /app                  0B
ccc6e87d482b        2 weeks ago          /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
<missing>           2 weeks ago          /bin/sh -c mkdir -p /run/systemd && echo 'do…   7B
<missing>           2 weeks ago          /bin/sh -c set -xe   && echo '#!/bin/sh' > /…   745B
<missing>           2 weeks ago          /bin/sh -c [ -z "$(apt-get indextargets)" ]     987kB
<missing>           2 weeks ago          /bin/sh -c #(nop) ADD file:08e718ed0796013f5…   63.2MB
```

Ako vidime `zanasufiit/ws-ukazka-layers-reuse` ma iba o jednu vrstvu navyse ostatne su znovupouzite. 

Ak by tieto vrstvy boli vacsie a miesto miniaturnych textovych suborov by sme instalovali nejake velke baliky (napr. python, java sdk, ...) tak je hned vidiet vyhoda takehoto znovupouzitia vrstiev.

Ked sa kontajner spusta tak si prida iba jednu zapisovatelnu vrstvu navyse a teda aj ak ma image 1gb a bezi 20 kontajnerov tak na disku to bude zaberat iba 1gb (+ trochu v zapisovatelnej vrstve).

![](https://docs.docker.com/storage/storagedriver/images/container-layers.jpg)
![](https://docs.docker.com/storage/storagedriver/images/sharing-layers.jpg)

Zdroj: https://docs.docker.com/storage/storagedriver/