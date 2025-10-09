import pygame
import os

# Initialisation
pygame.init()
pygame.display.set_mode((1, 1))

# --- Paramètres ---
sprite_path = "src/assets/sprites/caracters/sarah/walk.png"  # Ton spritesheet
output_folder = "src/assets/sprites/caracters/sarah/actions/walk"
frame_width = 64
frame_height = 64

# --- Chargement de l'image ---
spritesheet = pygame.image.load(sprite_path).convert_alpha()
sheet_width, sheet_height = spritesheet.get_size()

# Calcul du nombre de colonnes et de lignes
cols = sheet_width // frame_width
rows = sheet_height // frame_height

# Si tu veux nommer les directions de haut en bas :
directions = ["top", "left", "bottom", "right"]
# Si le nombre de lignes dépasse 4, on complète automatiquement
if rows > len(directions):
    for i in range(len(directions), rows):
        directions.append(f"dir_{i+1}")

# Création des dossiers de sortie
for direction in directions:
    os.makedirs(os.path.join(output_folder, direction), exist_ok=True)

# --- Découpage automatique ---
for row in range(rows):
    direction = directions[row]
    for col in range(cols):
        x = col * frame_width
        y = row * frame_height
        frame = spritesheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
        frame_path = os.path.join(output_folder, direction, f"anim_{col+1}.png")
        pygame.image.save(frame, frame_path)
        print(f"✅ Saved {frame_path}")

print(f"🎉 Extraction terminée : {rows} directions, {cols} frames par direction.")
