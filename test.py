from datetime import datetime

# Deux datetimes à soustraire
date1 = datetime(2023, 5, 15, 10, 30, 0)
date2 = datetime(2023, 5, 15, 8, 0, 0)

# Soustraction
difference = date1 - date2

# Affichage de la différence
print("Différence de temps:", difference.total_seconds()/60)
