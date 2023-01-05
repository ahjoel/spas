# SPAS - Système de gestion du Patrimoine et Appro Stock

Visitez [le site.](https://sg-spas.herokuapp.com)
[Paul MBUYI](https://github.com/PaulMbuyi)

# Fonctionnalités

SPAS est un logiciel de gestion du stock de matériel de bureau et du patrimoine qui peut être utilisé en entreprise tout comme à titre personnel. Il est conçu pour :

- éviter le surstockage des fournitures au stock
- optimiser le temps de traitement des activités lié à la gestion du stock et du patrimoine (immobilisations et biens) de l'entreprise
- optimiser les états mensuels du stock
- analyser la consommation des fournitures du stock sur une période donnée

# 

<a href="https://sg-spas.herokuapp.com" >
    <img width="100%"
      alt="Founitures"
      src="https://github.com/ahjoel/spas/blob/master/1.jpg"
    />
 </a>
 
#

<a href="https://sg-spas.herokuapp.com" >
    <img width="100%"
      alt="Liste Des Sorties"
      src="https://github.com/ahjoel/spas/blob/master/3.jpg"
    />
</a>

#

<a href="https://sg-spas.herokuapp.com" >
    <img width="100%"
      alt="Création De Sortie"
      src="https://github.com/ahjoel/spas/blob/master/2.jpg"
    />
</a>
  
#

1- Enregistrement des fournitures

2- Création des commandes

3- Opérations sur les entrees et sorties de fournitures

4- Opérations sur les sorties de fournitures

5- Bien d'autres..

# Getting started

1- Clone down the repo

2- Create and activate a virtual environment

3- Install the dependencies:

```python
  $ pip install -r requirements.txt
``` 

4- Apply the migrations:

```python
$ python manage.py migrate
``` 

## Development Example

```python
$ python manage.py runserver
``` 

## Production Example

1- Set DEBUG to False in the settings.py file

2- Then, collect the static files and run Gunicorn:

```python
$ python manage.py collectstatic
$ gunicorn core.wsgi:application
``` 
