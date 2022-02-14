import os
from urllib.parse import quote_plus
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import Identity
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

ENV = 'prod'

password = quote_plus(str(os.getenv('password')))

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:{}@localhost:5432/PythonProject".format(password)
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://dxcfzdkqdqmvfr" \
                                            ":5f75c871d98dc969eb42ffb0fcf0e8ba4a709632ff178360565619b0ab5993d3@ec2-50" \
                                            "-19-32-96.compute-1.amazonaws.com:5432/ddhjnde96u4d6a"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Categorie(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, Identity(start=1, cycle=True), primary_key=True)
    libelle_categorie = db.Column(db.String(25), nullable=False)

    def cat_format(self):
        return {
            'Id': self.id,
            'Libellé': self.libelle_categorie
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Livre(db.Model):
    __tablename__ = 'livres'
    id = db.Column(db.Integer, Identity(start=1, cycle=True), primary_key=True)
    isbn = db.Column(db.Integer, nullable=False, unique=True)
    titre = db.Column(db.String(50), nullable=False)
    date_publication = db.Column(db.Date, nullable=False)
    auteur = db.Column(db.String(50), nullable=False)
    editeur = db.Column(db.String(50), nullable=False)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def book_format(self):
        return {
            'Id': self.id,
            'Isbn': self.isbn,
            'Titre': self.titre,
            'Date de publication': self.date_publication,
            'Auteur': self.auteur,
            'Editeur': self.editeur,
            'Categorie(id)': self.categorie_id
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


#db.create_all()


###########################################################################################
#                               LISTE DE TOUS LES LIVRES
###########################################################################################

@app.route('/livres')
def lister_tous_les_livres():
    livres = Livre.query.all()
    livres_formates = [livre.book_format() for livre in livres]
    return jsonify(
        {
            'Success': True,
            'Total': len(livres),
            "Livre": livres_formates
        }
    )


###########################################################################################
#                               CHERCHER UN LIVRE PAR SON ID
###########################################################################################

@app.route('/livres/<int:id>')
def chercher_livre(id):
    livre = Livre.query.get(id)
    if livre is None:
        abort(404)
    else:
        return jsonify(
            {
                'Success': True,
                'Id Selectionné': id,
                "livre": livre.book_format()
            }
        )


###########################################################################################
#                      LISTER LA LISTE DES LIVRES D'UNE CATEGORIE
###########################################################################################

@app.route('/livres/categories/<int:id_arg>')
def books_of_a_specified_category(id_arg):
    categorie = Categorie.query.get(id_arg)
    if categorie is None:
        abort(404)
    else:
        livre = Livre.query.filter(Livre.categorie_id == id_arg)
        book_formated = [book.book_format() for book in livre]

        return jsonify(
            {
                'Success': True,
                'Id Selectionné': id_arg,
                'Total': len(book_formated),
                "livre": book_formated
            }
        )


###########################################################################################
#                              CHERCHER UNE CATEGORIE PAR SON ID
###########################################################################################

@app.route('/categories/<int:id>')
def chercher_categorie(id):
    categorie = Categorie.query.get(id)
    if categorie is None:
        abort(404)
    else:
        return jsonify(
            {
                'Success': True,
                'Id Selectionné': id,
                "Categorie": categorie.cat_format()
            }
        )


###########################################################################################
#                              LISTE DE TOUTES LES CATEGORIES
###########################################################################################

@app.route('/categories')
def get_all_categories():
    categories = Categorie.query.all()
    cat_formated = [categorie.cat_format() for categorie in categories]
    return jsonify(
        {
            'Success': True,
            'Total': len(categories),
            "Categories": cat_formated
        }
    )


###########################################################################################
#                                   SUPPRIMER UN LIVRE
###########################################################################################

@app.route('/livres/<int:id>', methods=['DELETE'])
def supprimer_liver(id):
    livre = Livre.query.get(id)
    if livre is None:
        abort(404)
    else:
        livre.delete()
        return jsonify(
            {
                'Success': True,
                'Id supprimé': id,
                'Livre': livre.book_format(),
                'Total Restant': Livre.query.count()
            }
        )


###########################################################################################
#                                   SUPPRIMER UNE CATEGORIE
###########################################################################################

@app.route('/categories/<int:id>', methods=['DELETE'])
def supprimer_categorie(id):
    categorie = Categorie.query.get(id)
    if categorie is None:
        abort(404)
    else:
        livre = Livre.query.filter(Livre.categorie_id == id)
        livre.delete()

        categorie.delete()
        return jsonify(
            {
                'Success': True,
                'Id supprimé': id,
                'Categorie': categorie.cat_format(),
                'Total Restant': Categorie.query.count()
            }
        )


###########################################################################################
#                              MODIFIER LES INFORMATIONS D'UN LIVRE
###########################################################################################

@app.route('/livres/<int:id>', methods=['PATCH'])
def modifier_livre(id):
    livre = Livre.query.get(id)
    if livre is None:
        abort(404)
    else:
        body = request.get_json()
        livre.isbn = body.get('Isbn')
        livre.titre = body.get('Titre')
        livre.date_publication = body.get('Date de publication')
        livre.auteur = body.get('Auteur')
        livre.editeur = body.get('Editeur')
        livre.categorie_id = body.get('Categorie(id)')
        livre.update()
        return jsonify(
            {
                'Success': True,
                'Total': Livre.query.count(),
                'Livre Modifié': id,
                'Livre': livre.book_format()
            }
        )


###########################################################################################
#                              MODIFIER LE LIBELLE D'UNE CATEGORIE
###########################################################################################

@app.route('/categories/<int:id>', methods=['PATCH'])
def modifier_libelle_cat(id):
    categorie = Categorie.query.get(id)
    if categorie is None:
        abort(404)
    else:
        body = request.get_json()
        categorie.libelle_categorie = body.get('Libelle')

        categorie.update()
        return jsonify(
            {
                'Success': True,
                'Total': Categorie.query.count(),
                'Categorie Modifié': id,
                'Categorie': categorie.cat_format()
            }
        )


@app.errorhandler(404)
def not_found(error):
    return jsonify(
        {
            "Success": False,
            "Erreur": 404,
            "Message": "Not Found"
        }
    )


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, DELETE')
    return response


if __name__ == '__main__':
    app.run()
