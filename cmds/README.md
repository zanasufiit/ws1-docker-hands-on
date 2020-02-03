# Zakladne Docker CLI prikazy

Zapnime si 2x terminal.

V jednom z nich si spustime `ubuntu` image s interaktivnym prikazovym riadkom.

## run

```
PS> docker run --rm -it ubuntu
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
Digest: sha256:8d31dad0c58f552e890d68bbfb735588b6b820a46e459672d96e585871acc110
Status: Downloaded newer image for ubuntu:latest
root@88cc1ca93a83:/#
```

- `--rm` - zmaze kontajner po ukonceni
- `-i` - pocuva stdin
- `-t` - alokuje tty (input)

Spustil sa nam kontajner a mame pristup k bashu.

## ps

```
PS> docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
88cc1ca93a83        ubuntu              "/bin/bash"         56 seconds ago      Up 55 seconds                           admiring_rubin
```
Pomocou docker ps vidime zoznam beziacich kontajnerov.

## start, stop, restart

zapne, vypne, restartuje kontajner (nevytvara novy)

## top
zobrazi beziace procesy v kontajneri

```
PS> docker top admiring_rubin
PID                 USER                TIME                COMMAND
3926                root                0:00                /bin/bash
```

## build
build image podla dockerfile

## push
pushne image do registry

## inspect
vracia informacie o docker objektoch (low level), je mozne formatovat, napr 
```
PS> docker inspect -f '{{ .Id }}' admiring_rubin
88cc1ca93a8386ac090dc9b5172214014d6c6c823901735e93efca98831d183a
```

## logs
zobrazuje stdout a stderr z kontajnera (ak to pouzity driver podporuje)

```
root@88cc1ca93a83:/# echo "abc"
abc
root@88cc1ca93a83:/# echo "efg"
efg
root@88cc1ca93a83:/#

---
PS> docker logs -f admiring_rubin
root@88cc1ca93a83:/# echo "abc"
abc
root@88cc1ca93a83:/# echo "efg"
efg
```

- `-f` - followuje vystup z kontajnera, bez prepinaca vypise vsetky logy co ma zaznamenane

## rm

sluzi na mazanie kontajnerov

## exec

executne nieco v kontajneri, taktiez podporuje aj interaktivny mod

```
PS> docker exec -it admiring_rubin bash
root@88cc1ca93a83:/# aa
```

```
(terminal 1) root@88cc1ca93a83:/# echo "abc" > x.txt

--

(terminal 2) root@88cc1ca93a83:/# cat x.txt
abc
```


## specifikejsie prikazy
`docker` <management-command>
```
Management Commands:
  builder     Manage builds
  checkpoint  Manage checkpoints
  config      Manage Docker configs
  container   Manage containers
  context     Manage contexts
  image       Manage images
  network     Manage networks
  node        Manage Swarm nodes
  plugin      Manage plugins
  secret      Manage Docker secrets
  service     Manage services
  stack       Manage Docker stacks
  swarm       Manage Swarm
  system      Manage Docker
  trust       Manage trust on Docker images
  volume      Manage volumes
```

kazdy podprikaz podporuje `help`