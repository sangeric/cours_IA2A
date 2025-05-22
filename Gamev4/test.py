from map import Map
from entities import EntityRobot, EntityMine
import pygame
from graphism.graphique import get_hex_from_pixel, draw_hexagone

def main():
    pygame.init()
    game_map = Map()
    game_map.generate_map()
    graph = game_map.build_graph()
    perso = EntityRobot(1,1)
    target = None
    chemin = []
    chemin_index = 0
    mode_move = False
    mode_collect = False

    collect_button_rect = pygame.Rect(120, 10, 100, 40)

    mode_build = False
    mode_mine = False
    info_font = pygame.font.SysFont(None, 20)

    surface_w = int((game_map.getWidth() + 1) * 1.5 * game_map.getSize())
    surface_h = int((game_map.getHeight() + 2) * (3 ** 0.5) * game_map.getSize())
    ecran = pygame.display.set_mode((surface_w, surface_h))
    pygame.display.set_caption("Déplacement sur carte hexagonale avec graphe")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 30)
    move_button_rect = pygame.Rect(10, 10, 100, 40)
    build_button_rect = pygame.Rect(230, 10, 100, 40)
    mine_button_rect = pygame.Rect(340, 10, 100, 40)

    def draw_button():
        # Bouton Move
        move_color = (0, 200, 0) if not mode_move else (200, 0, 0)
        pygame.draw.rect(ecran, move_color, move_button_rect)
        move_text = font.render("Move", True, (255, 255, 255))
        ecran.blit(move_text, (move_button_rect.x + 20, move_button_rect.y + 8))
        pygame.draw.rect(ecran, (0, 100, 200), collect_button_rect)
        collect_text = font.render("Collect", True, (255, 255, 255))
        ecran.blit(collect_text, (collect_button_rect.x + 10, collect_button_rect.y + 8))
        

        robot_lines = [f"Inventaire du robot ({sum(perso.inventory.values())}/{perso.inventory_capacity})"]
        for resource in ["wood", "coal", "rock", "water"]:
            amount = perso.inventory.get(resource, 0)
            robot_lines.append(f"  - {resource} : {amount}")


        padding = 10
        line_height = 18
        info_width = max(info_font.size(line)[0] for line in robot_lines) + 2 * padding
        info_height = line_height * len(robot_lines) + 2 * padding

        robot_info_surface = pygame.Surface((info_width, info_height), pygame.SRCALPHA)
        robot_info_surface.fill((40, 40, 40, 220))

        for i, line in enumerate(robot_lines):
            text = info_font.render(line, True, (255, 255, 255))
            robot_info_surface.blit(text, (padding, padding + i * line_height))

        ecran.blit(robot_info_surface, (10, 60))  



        # Bouton Build
        build_color = (0, 0, 200) if not mode_build else (0, 0, 100)
        pygame.draw.rect(ecran, build_color, build_button_rect)
        build_text = font.render("Build", True, (255, 255, 255))
        ecran.blit(build_text, (build_button_rect.x + 20, build_button_rect.y + 8))

        # Affichage conditionnel du bouton Mine
        if mode_build:
            mine_color = (200, 200, 0) if not mode_mine else (150, 150, 0)
            pygame.draw.rect(ecran, mine_color, mine_button_rect)
            mine_text = font.render("Mine", True, (0, 0, 0))
            ecran.blit(mine_text, (mine_button_rect.x + 20, mine_button_rect.y + 8))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if move_button_rect.collidepoint(pos):
                    mode_move = True
                    mode_collect = False 
                elif collect_button_rect.collidepoint(pos):
                    mode_collect = True
                    mode_move = False     
                elif mode_collect:
                    coord = get_hex_from_pixel(game_map, *pos)
                    if coord:
                        rx, ry = perso.getPos()
                        adjacent = game_map.get_neighbors(rx, ry)
                        adjacent.append((rx, ry)) 

                        if coord in adjacent:
                            tx, ty = coord
                            tile = game_map.get_tile(ty, tx)
                            collected = perso.collect_from_tile(tile, max_to_collect=10)

                            if collected > 0:
                                print(f"{collected} ressource(s) récoltée(s) sur ({tx},{ty})")
                            else:
                                print(f"Aucune ressource à récolter sur ({tx},{ty})")


                elif mode_move:
                    coord = get_hex_from_pixel(game_map, *pos)
                    if coord and game_map.getGrid()[coord[1]][coord[0]].getName() != "-":
                        target = coord
                        chemin = perso.dijkstra(graph, target)
                        chemin_index = 0

                elif mode_mine:
                    coord = get_hex_from_pixel(game_map, *pos)
                    if coord:
                        tx, ty = coord
                        tile = game_map.get_tile(ty, tx)
                        if tile and tile.getName() == "mountain":
                            print("clic  montagne")
                            # Vérifier si une entité (robot) est sur une tuile adjacente
                            if tx % 2 == 0:
                                offsets = [(1, 0), (1, -1), (0, -1), (0, 1), (-1, 0), (-1, -1)]
                                
                            else:
                                offsets = [(1, 0), (1, 1), (0, -1), (0, 1), (-1, 0), (-1, 1)]
                            voisins = [(tx + dx, ty + dy) for dx, dy in offsets]
                            if perso.getPos() in voisins:
                                print("robot adjacent a la montagne")
                                tile.setBuilding(EntityMine(tx, ty))
                                mode_mine = False
                            else:
                                print("robot trop loin pour construire une mine")


        if mode_move and chemin and chemin_index < len(chemin):
            perso.setPos(chemin[chemin_index])
            chemin_index += 1
            if chemin_index >= len(chemin):
                mode_move = False 
                
        for y in range(game_map.getHeight()):
            for x in range(game_map.getWidth()):
                tile = game_map.get_tile(y, x)
                building = tile.getBuilding()
                if building and isinstance(building, EntityMine):
                    building.update(tile)

        ecran.fill((0, 0, 0))
        for y in range(game_map.getHeight()):
            for x in range(game_map.getWidth()):
                tile = game_map.get_tile(y,x)
                if tile:
                    is_perso = (x, y) == perso.getPos()
                    draw_hexagone(game_map, ecran, x, y, tile, highlight=((x, y) in chemin and (x, y) != perso.getPos()), personnage=is_perso)
                if tile.getBuilding() and isinstance(tile.getBuilding(), EntityMine):
                    center_x, center_y = draw_hexagone(game_map, ecran, x, y, tile, return_center=True)
                    pygame.draw.circle(ecran, (0, 0, 0), (center_x, center_y), 5)


        mouse_x, mouse_y = pygame.mouse.get_pos()
        tile_coord = get_hex_from_pixel(game_map, mouse_x, mouse_y)
        if tile_coord:
            tx, ty = tile_coord
            try:
                tile = game_map.get_tile(ty, tx)
                if tile:
                    name = tile.getName()
                    resources = tile.getResources() 

                    lines = [f"({tx}, {ty}) \"{name}\""]
                    res_lines = [f"{res}: {qty}" for res, qty in resources.items() if qty > 0]

                    if res_lines:
                        lines.extend(res_lines)
                    else:
                        lines.append("Aucune ressource")

                    padding = 5
                    line_height = 18
                    width = max(info_font.size(line)[0] for line in lines) + 2 * padding
                    height = line_height * len(lines) + 2 * padding

                    tooltip_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                    tooltip_surface.fill((0, 0, 0, 180))  

                    for i, line in enumerate(lines):
                        text = info_font.render(line, True, (255, 255, 255))
                        tooltip_surface.blit(text, (padding, padding + i * line_height))

                    tooltip_x = mouse_x + 10
                    tooltip_y = mouse_y + 10
                    ecran.blit(tooltip_surface, (tooltip_x, tooltip_y))
            except IndexError:
                pass
        
        if tile_coord:
            tx, ty = tile_coord
            try:
                tile = game_map.get_tile(ty, tx)
                lines = []

                entity = tile.getEntity()
                building = tile.getBuilding()

                if entity:
                    lines.append(f"Entité : {entity.__class__.__name__}")
                    if hasattr(entity, "inventory") and hasattr(entity, "inventory_capacity"):
                        total_items = sum(v for v in entity.inventory.values() if v > 0)
                        lines.append(f"Inventaire : {total_items} / {entity.inventory_capacity}")
                        for resource, amount in entity.inventory.items():
                            if amount > 0:
                                lines.append(f"  - {resource} : {amount}")

                if building:
                    lines.append(f"Bâtiment : {building.__class__.__name__}")
                    if hasattr(building, "inventory") and hasattr(building, "inventory_capacity"):
                        total_items = sum(v for v in building.inventory.values() if v > 0)
                        lines.append(f"Stock : {total_items} / {building.inventory_capacity}")
                        for resource, amount in building.inventory.items():
                            if amount > 0:
                                lines.append(f"  - {resource} : {amount}")

                if lines:
                    padding = 10
                    line_height = 22
                    info_width = max(info_font.size(line)[0] for line in lines) + 2 * padding
                    info_height = line_height * len(lines) + 2 * padding
                    screen_width, screen_height = ecran.get_size()

                    info_x = 10
                    info_y = screen_height - info_height - 10

                    entity_info_surface = pygame.Surface((info_width, info_height), pygame.SRCALPHA)
                    entity_info_surface.fill((30, 30, 30, 230))

                    for i, line in enumerate(lines):
                        text = info_font.render(line, True, (255, 255, 255))
                        entity_info_surface.blit(text, (padding, padding + i * line_height))

                    ecran.blit(entity_info_surface, (info_x, info_y))
            except IndexError:
                pass



        
        draw_button()
        pygame.display.flip()
        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    main()
