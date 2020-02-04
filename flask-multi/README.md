# Docker compose

Docker Compose je nastroj pre definiciu a spustanei viacerych kontajnerov naraz.

Bezne nemame len jednu aplikaciu ale napr. aj databazu.

## Problem

Aplikacia sa sklada z viacerych komponentov

- server
- server2
- databaza

Predpokladame, ze vsetko je v kontajneroch.

## Riesenie:
Definovat celu strukturu pomocou docker-compose. Umoznuje nam to zapnut cely system naraz.

Docker-compose nam umoznuje pomocou yml definovat ako sa ma spustit viacero kontajnerov. Medzi najvacsie vyhody patri, ze automaticky riesi hlavne tieto problemy

- vsetko sa da zapnut jednym prikazom `docker-compose up` a vypnut a zmazat pomocou `docker-compose down`
- zosietuje vsetky services (kontajnery) v danom compose (hostname je nazov servicu)
- moznost pouzivat relativne adresy pri volumes (z docker cli je nutne absolutne) napr. `./file-reader/content.txt:/vol/content.txt`
- pekny pristup k logom pomocou `docker-compose logs`
- moznost templatovat compose file
- moznost spustat iba cast zo servicov

A ovela viac dokumentacia pomoze viac:
- https://docs.docker.com/compose/

## Kedy pouzit compose?
1. ak mame jednoduchy deployment na server
2. ak chceme jednoducho spustit viacero kontajnerov a nehrat sa s nastavenim sieti
3. lokalny development (ak potrebujeme napr. databazy)
4. na spustenie environmentu pre testovanie

Vsetko co sa da urobit cez compose je mozne urobit aj cez CLI ale je to omnoho jednoduchsie.

## Nas priklad

Nas priklad ([docker-compose.yml](docker-compose.yml)) sa sklada z 4 servicov (kontajnerov).

1. server
    - ziskava data z druhej service
    - data uklada do databazy (co je tiez dalsia service)
2. file-reader
    - ukazka ako pouzit `bind mount` a zdielat subor z hosta s kontajnerom
3. databaza
    - jednoduchy setup postgresql
4. pgadmin
    - priklad zaujimaveho kontajneru na spravu veci
