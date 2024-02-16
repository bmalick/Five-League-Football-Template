# Five League Football Template

This project aims to create datasets of Football fixtures into your Notion page.
The teama and fixtures are taken from official leagues calendars and then they are embedded into Notion page.
The fetching of gameweek matches are scraped and there are commands to have updates every week.


# Notion API
Notion API is used for page creation. Follow the description [here](https://developers.notion.com/docs/authorization) to create your Notion Integration.




<!-- IMAGE DE LA PAGE -->


# Configs
Les entraînements sont lancés en exécutant:
```bash
make train cfg=[filename]
```

Le dossier [**configs**](/kss/configs/) contients les fichiers de configuration utiliser pour spécifier l'ensemble des paramètres pour un entraînement.

Voici la structure d'un fichier de configuration:

- La section **model** spécifie les paramètres du modèle

- La section **training** contient des paramètres liés à l'entraînement, tels que le nombre d'epochs, l'optimiseur, la fonction de perte, les métriques et les callbacks.

- La section **dataset** spécifie les détails sur les générateurs et les fichiers d'annotations.

