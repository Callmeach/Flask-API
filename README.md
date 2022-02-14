# API GESTION DES LIVRES D'UNE BIBLIOTHEQUE

## A Propos
Cette API permet de gérer des livres et les catégories auxquelles ils appartiennent.

### Installation des dependances

#### Python 3.10.1
#### pip 22.0.3

Merci d'installer Python avant de continuer

#### Environnement Virtuel

Vous devez installer le package dotenv en utilisant la commande pip install python-dotenv 

#### Dependances PIP

Exécuter la commande ci dessous pour installer les dépendences
```bash
pip install -r requirements.txt
```

##### Dependances Clés

- [Flask](http://flask.pocoo.org/)  est un framework léger de microservices backend. Flask est nécessaire pour gérer les demandes et les réponses.

- [SQLAlchemy](https://www.sqlalchemy.org/) est la boîte à outils Python SQL et l'ORM que nous utiliserons pour gérer la base de données sqlite légère. Vous travaillerez principalement dans app.py et pourrez référencer models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) est l'extension que nous utiliserons pour gérer les demandes d'origine croisée de notre serveur front-end.

## Configuration de base de données
Avec Postgres en cours d'exécution, restaurez une base de données à l'aide du fichier database.sql fourni. Depuis le dossier backend dans le terminal, exécutez :
```bash
psql PythonProject < database.sql
```

## Demarrer le serveur

Placez vous dans le dossier dans lequel vous executez votre script Python
Pour demmarrer le serveur sur Linux ou Mac OS executez:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Pour demmarrer le serveur sur Windows executez:

```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

Définir la variable `FLASK_ENV` sur `development` détectera les modifications de fichiers et redémarrera le serveur automatiquement.

Définir la variable `FLASK_APP` sur `flaskr` indique à flask d'utiliser le répertoire `flaskr` et le fichier `__init__.py` pour trouver l'application.

## Error Handling
Les erreurs sont renvoyées sous forme d'objets JSON au format suivant :
{
    "success":False
    "erreurr": 400
    "message":"Bad request"
}

L'API retournera quatre types d'erreurs en cas d'echec:
. 400: Bad request
. 500: Internal server error
. 422: Unprocessable
. 404: Not found

## Endpoints
###  -GET/livres     
    GENERAL: Cet endpoint permet de récupérer la liste de tous les livres
        
    SAMPLE: curl -i http://localhost:5000/livres
    {
    "Livre": [
        {
            "Auteur": "Sthendal",
            "Categorie(id)": 7,
            "Date de publication": "Wed, 06 Jan 1999 00:00:00 GMT",
            "Editeur": "Gallimards",
            "Id": 2,
            "Isbn": 26891065,
            "Titre": "Le Rouge et le Noir"
        },
        {
            "Auteur": "Romain Gary",
            "Categorie(id)": 6,
            "Date de publication": "Wed, 04 Dec 2002 00:00:00 GMT",
            "Editeur": "Flammarion",
            "Id": 3,
            "Isbn": 43501937,
            "Titre": "La Promesse de l'aube"
        }
    ],
    "Success": true,
    "Total": 2
    }

### -GET/livres (id)

    GENERAL: Cet endpoint permet de rechercher un livre connaissant son id
        
    SAMPLE: curl -i http://localhost:5000/livres/6

    {
        "Id Selectionné": 6,
        "Success": true,
        "livre": {
            "Auteur": "Pierre Choderlos de Laclos",
            "Categorie(id)": 4,
            "Date de publication": "Sun, 19 Mar 2006 00:00:00 GMT",
            "Editeur": "Privat",
            "Id": 6,
            "Isbn": 90268394,
            "Titre": "Les liaisons dangereuses"
        }
    }

### -GET/livres/categories (id)

    GENERAL: Cet endpoint permet de recuperer tous les livres d'une categorie donnée
        
    SAMPLE: curl -i http://localhost:5000/livres/categories/4

    {
        "Id Selectionné": 4,
        "Success": true,
        "Total": 2,
        "livre": [
            {
                "Auteur": "Pierre Choderlos de Laclos",
                "Categorie(id)": 4,
                "Date de publication": "Sun, 19 Mar 2006 00:00:00 GMT",
                "Editeur": "Privat",
                "Id": 6,
                "Isbn": 90268394,
                "Titre": "Les liaisons dangereuses"
            },
            {
                "Auteur": "Toni Morrison",
                "Categorie(id)": 4,
                "Date de publication": "Mon, 16 Mar 1987 00:00:00 GMT",
                "Editeur": "Hachette",
                "Id": 17,
                "Isbn": 17937047,
                "Titre": "Beloved"
            }
        ]
    }

### -GET/categories (id)

    GENERAL: Cet endpoint permet de rechercher une categorie connaissant son id
        
    SAMPLE: curl -i http://localhost:5000/categories/4

    {
        "Categorie": {
            "Id": 4,
            "Libellé": "Harlequin"
        },
        "Id Selectionné": 4,
        "Success": true
    }

### -GET/categories

    GENERAL: Cet endpoint permet de recuperer la liste de toutes les categories disponibles
        
    SAMPLE: curl -i http://localhost:5000/categories

    {
        "Categories": [
            {
                "Id": 1,
                "Libellé": "Policier"
            },
            {
                "Id": 4,
                "Libellé": "Harlequin"
            }
        ],
        "Success": true,
        "Total": 2
    }

### -DELETE/livres (id)

    GENERAL: Cet endpoint permet de supprimer un livre
        
    SAMPLE: curl -i http://localhost:5000/livres/2

    {
        "Id supprimé": 2,
        "Livre": {
            "Auteur": "Sthendal",
            "Categorie(id)": 7,
            "Date de publication": "Wed, 06 Jan 1999 00:00:00 GMT",
            "Editeur": "Gallimards",
            "Id": 2,
            "Isbn": 26891065,
            "Titre": "Le Rouge et le Noir"
        },
        "Success": true,
        "Total Restant": 1
    }

### -DELETE/categories (id)

    GENERAL: Cet endpoint permet de supprimer une categorie de livres
        
    SAMPLE: curl -i http://localhost:5000/categories/3

    {
        "Categorie": {
            "Id": 3,
            "Libellé": Conte
        },
        "Id supprimé": 3,
        "Success": true,
        'Total Restant': 1
    }

### -PATCH/livres (id)

    GENERAL: Cet endpoint permet de modifier les informations d'un livre
        
    SAMPLE: curl -i http://localhost:5000/livres/1

    {
        "Livre": {
            "Auteur": "Victor Hugo",
            "Categorie(id)": 7,
            "Date de publication": "Fri, 10 Feb 1989 00:00:00 GMT",
            "Editeur": "Gallimards",
            "Id": 1,
            "Isbn": 62345611,
            "Titre": "Les Miserables"
        },
        "Livre Modifié": 1,
        "Success": true,
        "Total": 1
    }

### -PATCH/categories (id)

    GENERAL: Cet endpoint permet de modifier le libellé d'une categorie donnée
        
    SAMPLE: curl -i http://localhost:5000/categories/5

    {
        "Categorie": {
            "Id": 5,
            "Libellé": "Realiste"
        },
        "Categorie Modifié": 5,
        "Success": true,
        "Total": 1
    }