# TP_01 INF37407 – Moissoneur et gestionnaire de données OGSL (Observatoire Globale du Saint Laurent)

Travail pratique 01 dans le cadre du cours Technologies de l'inforoute (INF 37407), Automne 2025, UQAR.
Ce travail consiste à développer une plateforme serveur (back-end) pour la collecte et la gestion de données issues du site de données ouvertes du gouvernement du Quebec (www.donneesquebec.ca)

## 🎯 Objectif
- Moissonner des données depuis Données Québecd
- Structurer et stocker ces données dans une base relationnelle
- Exposer les données via des APIs REST et GraphQL sécurisées
- Offrir une interface d’administration et une page de statistiques

## 🧰 Technologies utilisées
### Langages & Frameworks
- Python
- Django
- Django REST Framework
- Graphene-Django

### Outils & Librairies
- Swagger / drf-yasg (documentation REST)
- GraphiQL (documentation GraphQL)
- Bootstrap 5 + Font Awesome (interface graphique)
- Postman (tests API)
- MySQL Server + MySQL Workbench
- Git + GitHub (gestion de version)

## 🗂️ Structure du projet
Le projet est divisé en plusieurs applications Django :
- `moissoneur` : script python de moissonnage
- `catalogue` : modèle rélationnel
- `api` : endpoints REST et GraphQL
- `ui_admin` : interface d’administration
- `statistiques` : visualisation des statistiques

## 🔄 Étapes de réalisation
1. **Définition des filtres de moissonnage** (mots-clés, producteurs, localisation)
2. **Tests et analyse des schémas CKAN** via Postman
3. **Récupération automatisée** des données avec scripts Python
4. **Stockage structuré** via Django ORM
5. **Création d’une interface d’administration** ergonomique
6. **Développement des APIs REST et GraphQL** avec documentation interactive
7. **Affichage des statistiques** (nombre de jeux, répartition thématique, etc.)
8. **Sécurisation de l’accès** (authentification, permissions)
9. **Déploiement sur Render.com**
