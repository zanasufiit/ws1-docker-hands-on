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