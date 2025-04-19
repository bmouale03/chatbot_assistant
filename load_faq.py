import pandas as pd

import pandas as pd

# Lire le fichier CSV avec le bon délimiteur
df = pd.read_csv('faq.csv', sep=';')

# Affichez les colonnes pour vérifier
print(f"Colonnes trouvées : {df.columns}")

# Vérifiez les premières lignes pour voir les données
print(df.head())

