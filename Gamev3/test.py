from map import Map

def main():
    print("Génération de la carte...")
    game_map = Map(width=5, height=5)
    print("Affichage de la carte :")
    game_map.display()

if __name__ == "__main__":
    main()
