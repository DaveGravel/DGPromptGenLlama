import os
import pkg_resources

# Déterminer automatiquement le chemin du projet (répertoire courant du script)
project_path = os.path.dirname(os.path.abspath(__file__))

# Récupérer tous les fichiers Python dans le projet
python_files = [
    os.path.join(root, file)
    for root, _, files in os.walk(project_path)
    for file in files
    if file.endswith(".py")
]

# Extraire les modules importés
imports = set()
for file in python_files:
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("import ") or line.startswith("from "):
                parts = line.split()
                if len(parts) > 1:
                    imports.add(parts[1].split(".")[0])

# Récupérer les paquets installés
installed_packages = {pkg.key for pkg in pkg_resources.working_set}

# Filtrer les dépendances utilisées
used_dependencies = [pkg for pkg in imports if pkg in installed_packages]

# Écrire dans requirements.txt
requirements_file = os.path.join(project_path, "requirements.txt")
with open(requirements_file, "w", encoding="utf-8") as req_file:
    req_file.write("\n".join(used_dependencies))

print(f"requirements.txt généré avec succès dans : {requirements_file}")