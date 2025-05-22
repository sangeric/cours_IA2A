from map import Map
from entities import EntityRobot, EntityMine, EntityStorage, EntitySawmil, EntityFactory, EntityPipe
import pygame
from graphism.graphique import get_hex_from_pixel, draw_hexagone


dependencies = {
    "EntityMine": [],
    "EntitySawmil": [],
    "EntityFactory": ["EntityMine", "EntitySawmil"]
}

built_entities = set()

def can_build(entity_name, built_set, dependencies):
    return all(dep in built_set for dep in dependencies.get(entity_name, []))

def tri_topologique(graph):
    from collections import defaultdict, deque

    in_degree = defaultdict(int)
    adj = defaultdict(list)

    for node in graph:
        for neighbor in graph[node]:
            adj[neighbor].append(node)
            in_degree[node] += 1
        if node not in in_degree:
            in_degree[node] = 0

    queue = deque([node for node in graph if in_degree[node] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(graph):
        raise ValueError("Cycle détecté dans les dépendances")

    return order


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
    mode_build = False
    mode_mine = False
    mode_storage = False
    mode_sawmill = False
    mode_factory = False
    mode_factory_choice = False
    mode_pipe = False
    
    info_font = pygame.font.SysFont(None, 20)   
#coucou
    surface_w = int((game_map.getWidth() + 1) * 1.5 * game_map.getSize())
    surface_h = int((game_map.getHeight() + 2) * (3 ** 0.5) * game_map.getSize())
    ecran = pygame.display.set_mode((surface_w, surface_h))
    pygame.display.set_caption("Déplacement sur carte hexagonale avec graphe")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 30)
    move_button_rect = pygame.Rect(10, 10, 100, 40)
    collect_button_rect = pygame.Rect(120, 10, 100, 40)
    build_button_rect = pygame.Rect(230, 10, 100, 40)
    mine_button_rect = pygame.Rect(340, 10, 100, 40)
    storage_button_rect = pygame.Rect(340, 60, 100, 40) 
    factory_button_rect = pygame.Rect(340, 110, 100, 40) 
    stone_button_rect = pygame.Rect(230, 440, 100, 40)
    plank_button_rect = pygame.Rect(340, 440, 100, 40)
    brick_button_rect = pygame.Rect(450, 440, 100, 40)
    pipe_button_rect = pygame.Rect(450, 60, 100, 40)
    sawmill_button_rect = pygame.Rect(340, 110, 100, 40) 
    factory_button_rect = pygame.Rect(340, 160, 100, 40)
    
    def draw_button():
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

        build_color = (0, 0, 200) if not mode_build else (0, 0, 100)
        pygame.draw.rect(ecran, build_color, build_button_rect)
        build_text = font.render("Build", True, (255, 255, 255))
        ecran.blit(build_text, (build_button_rect.x + 20, build_button_rect.y + 8))
        if mode_factory_choice:
            plank_color = (181, 101, 29)
            pygame.draw.rect(ecran, plank_color, plank_button_rect)
            plank_text = font.render("Plank", True, (0, 0, 0))
            ecran.blit(plank_text, (plank_button_rect.x + 20, plank_button_rect.y + 8))
            
            stone_color = (120, 120, 120)
            pygame.draw.rect(ecran, stone_color, stone_button_rect)
            stone_text = font.render("Stone", True, (0, 0, 0))
            ecran.blit(stone_text, (stone_button_rect.x + 20, stone_button_rect.y + 8))
            
            brick_color = (178, 34, 34)
            pygame.draw.rect(ecran, brick_color, brick_button_rect)
            brick_text = font.render("Brick", True, (0, 0, 0))
            ecran.blit(brick_text, (brick_button_rect.x + 20, brick_button_rect.y + 8))

        if mode_build:
            mine_color = (200, 200, 0) if not mode_mine else (150, 150, 0)
            pygame.draw.rect(ecran, mine_color, mine_button_rect)
            mine_text = font.render("Mine", True, (0, 0, 0))
            ecran.blit(mine_text, (mine_button_rect.x + 20, mine_button_rect.y + 8))
            
            storage_color = (150, 150, 255) if not mode_storage else (100, 100, 200)
            pygame.draw.rect(ecran, storage_color, storage_button_rect)
            storage_text = font.render("Storage", True, (0, 0, 0))
            ecran.blit(storage_text, (storage_button_rect.x + 5, storage_button_rect.y + 8))
            
            sawmill_color = (139, 69, 19) if not mode_sawmill else (101, 67, 33)

            pygame.draw.rect(ecran, sawmill_color, sawmill_button_rect)
            sawmill_text = font.render("Sawmill", True, (255, 255, 255))
            ecran.blit(sawmill_text, (sawmill_button_rect.x + 5, sawmill_button_rect.y + 8))

            if can_build("EntityFactory", built_entities, dependencies):
                factory_color = (100, 100, 100)
                factory_button_rect = pygame.Rect(340, 160, 100, 40)
                pygame.draw.rect(ecran, factory_color, factory_button_rect)
                factory_text = font.render("Factory", True, (255, 255, 255))
                ecran.blit(factory_text, (factory_button_rect.x + 5, factory_button_rect.y + 8))

                
                factory_color = (255, 150, 100) if not mode_factory else (200, 100, 50)
                pygame.draw.rect(ecran, factory_color, factory_button_rect)
                factory_text = font.render("Factory", True, (0, 0, 0))
                ecran.blit(factory_text, (factory_button_rect.x + 5, factory_button_rect.y + 8))

                pygame.draw.rect(ecran, (100, 200, 100), pipe_button_rect)
                pipe_text = font.render("Pipe", True, (255, 255, 255))
                ecran.blit(pipe_text, (pipe_button_rect.x + 10, pipe_button_rect.y + 8))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if move_button_rect.collidepoint(pos):
                    mode_move = True
                    mode_collect = mode_build = mode_mine = mode_storage = mode_factory = mode_factory_choice = False
                    continue
                elif collect_button_rect.collidepoint(pos):
                    mode_collect = True
                    mode_move = mode_build = mode_mine = mode_storage = mode_factory = mode_factory_choice = False
                    continue
                elif build_button_rect.collidepoint(pos):
                    mode_build = True
                    mode_move = mode_collect = mode_mine = mode_storage = mode_factory = mode_factory_choice = False
                    continue
                elif mine_button_rect.collidepoint(pos):
                    mode_mine = True
                    mode_move = mode_collect = mode_storage = mode_factory = mode_factory_choice = False
                    continue
                elif storage_button_rect.collidepoint(pos):
                    mode_storage = True
                    mode_move = mode_collect = mode_mine = mode_factory = mode_factory_choice = False
                    continue
                elif factory_button_rect.collidepoint(pos):
                    mode_factory = True
                    mode_move = mode_collect = mode_mine = mode_storage = mode_factory_choice = False
                    continue
                elif plank_button_rect.collidepoint(pos):
                    if selected_factory_tile:
                        selected_factory_tile.setBuildingRecipe("plank")
                    continue
                elif stone_button_rect.collidepoint(pos):
                    if selected_factory_tile:
                        selected_factory_tile.setBuildingRecipe("stone")
                    continue
                elif brick_button_rect.collidepoint(pos):
                    if selected_factory_tile:
                        selected_factory_tile.setBuildingRecipe("brick")
                    continue
                elif pipe_button_rect.collidepoint(pos):
                    mode_pipe = True
                    mode_move = mode_collect = mode_build = mode_mine = mode_storage = mode_factory = mode_factory_choice = False
                    selected_source = None
                    continue


                tile_coord = get_hex_from_pixel(game_map, pos[0], pos[1])
                if not tile_coord:
                    continue

                tx, ty = tile_coord
                tile = game_map.get_tile(ty, tx)

                if tile and isinstance(tile.getBuilding(), EntityFactory):
                    selected_factory_tile = tile
                    mode_factory_choice = True
                    mode_move = mode_collect = mode_build = mode_mine = mode_storage = mode_factory = False
                    continue

                if mode_collect:
                    rx, ry = perso.getPos()
                    adjacent = game_map.get_neighbors(rx, ry)
                    adjacent.append((rx, ry))
                    mode_move = mode_mine = mode_collect = False
                elif sawmill_button_rect.collidepoint(pos):
                    mode_sawmill = True
                    mode_storage = mode_mine = mode_collect = mode_move = False

                    
                elif mode_collect:
                    coord = get_hex_from_pixel(game_map, *pos)
                    if coord:
                        rx, ry = perso.getPos()
                        adjacent = game_map.get_neighbors(rx, ry)
                        adjacent.append((rx, ry)) 

                    if (tx, ty) in adjacent:
                        tile = game_map.get_tile(ty, tx)
                        collected = perso.collect_from_tile(tile, max_to_collect=10)
                        if collected > 0:
                            print(f"{collected} ressource(s) récoltée(s) sur ({tx},{ty})")
                        else:
                            print(f"Aucune ressource à récolter sur ({tx},{ty})")
                    continue

                if mode_move:
                    if tile and tile.getName() != "-":
                        target = (tx, ty)
                        chemin = perso.dijkstra(graph, target)
                        chemin_index = 0
                    continue

                if mode_mine:
                    if tile and tile.getName() == "mountain":
                        if tx % 2 == 0:
                            offsets = [(1, 0), (1, -1), (0, -1), (0, 1), (-1, 0), (-1, -1)]
                        else:
                            offsets = [(1, 0), (1, 1), (0, -1), (0, 1), (-1, 0), (-1, 1)]
                        voisins = [(tx + dx, ty + dy) for dx, dy in offsets]
                        if perso.getPos() in voisins:
                            tile.setBuilding(EntityMine(tx, ty))
                                built_entities.add("EntityMine")
                            mode_mine = mode_build = False
                        else:
                            print("robot trop loin pour construire une mine")
                    continue

                if mode_storage:
                    if tile and tile.getName() in ("sand", "plains") and tile.getBuilding() is None:
                        if tx % 2 == 0:
                            offsets = [(1, 0), (1, -1), (0, -1), (0, 1), (-1, 0), (-1, -1)]
                        else:
                            offsets = [(1, 0), (1, 1), (0, -1), (0, 1), (-1, 0), (-1, 1)]
                        voisins = [(tx + dx, ty + dy) for dx, dy in offsets]
                        if perso.getPos() in voisins:
                            tile.setBuilding(EntityStorage(tx, ty))
                            print(f"Storage placé en ({tx}, {ty})")
                            mode_storage = mode_build = False
                    continue

                if mode_factory:
                    if tile and tile.getName() in ("sand", "plains") and tile.getBuilding() is None:
                        if tx % 2 == 0:
                            offsets = [(1, 0), (1, -1), (0, -1), (0, 1), (-1, 0), (-1, -1)]
                        else:
                            offsets = [(1, 0), (1, 1), (0, -1), (0, 1), (-1, 0), (-1, 1)]
                        voisins = [(tx + dx, ty + dy) for dx, dy in offsets]
                        if perso.getPos() in voisins:
                            tile.setBuilding(EntityFactory(tx, ty))
                            print(f"Factory placé en ({tx}, {ty})")
                            mode_factory = mode_build = False
                    continue

                if mode_pipe:
                    if not selected_source:
                        if isinstance(tile.getBuilding(), EntityMine):
                            selected_source = tile.getBuilding()
                            print("Source pipe sélectionnée")
                    else:
                        if isinstance(tile.getBuilding(), EntityStorage):
                            pipe = EntityPipe(tx, ty, selected_source, tile.getBuilding())
                            tile.setPipe(pipe)
                            print(f"Pipe créé de la mine à ({tx}, {ty})")
                            mode_pipe = False
                            selected_source = None
                    continue


                

                                
                elif mode_sawmill:
                    coord = get_hex_from_pixel(game_map, *pos)
                    if coord:
                        tx, ty = coord
                        tile = game_map.get_tile(ty, tx)
                        if tile and tile.getName() == "forest" and tile.getBuilding() is None:
                            if tx % 2 == 0:
                                offsets = [(1, 0), (1, -1), (0, -1), (0, 1), (-1, 0), (-1, -1)]
                            else:
                                offsets = [(1, 0), (1, 1), (0, -1), (0, 1), (-1, 0), (-1, 1)]

                            voisins = [(tx + dx, ty + dy) for dx, dy in offsets]
                            if perso.getPos() in voisins:
                                tile.setBuilding(EntitySawmil(tx, ty))
                                built_entities.add("EntitySawmil")
                                print(f"Sawmill placé en ({tx}, {ty})")
                                mode_sawmill = False
                            else:
                                print("Robot trop loin pour construire la scierie")
                elif mode_factory:
                    coord = get_hex_from_pixel(game_map, *pos)
                    if coord:
                        tx, ty = coord
                        tile = game_map.get_tile(ty, tx)
                        entity_name = "EntityFactory"

                        if tile and tile.getBuilding() is None:
                            if can_build(entity_name, built_entities, dependencies):
                                if perso.getPos() in game_map.get_neighbors(tx, ty):
                                    tile.setBuilding(EntityFactory(tx, ty))
                                    built_entities.add(entity_name)
                                    print(f"✅ Usine construite en ({tx}, {ty})")
                                    print("🧱 Ordre de construction :", tri_topologique(dependencies))
                                    mode_factory = False
                                else:
                                    print("Robot trop loin pour construire une usine")
                            else:
                                print("Impossible de construire une usine : mine + scierie requises")
                        else:
                            print("Emplacement invalide ou usine déjà présente")
                
                elif factory_button_rect.collidepoint(pos) and can_build("EntityFactory", built_entities, dependencies):
                    mode_factory = True
                    mode_storage = mode_mine = mode_collect = mode_move = False



                            
                            


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
                elif building and isinstance(building, EntitySawmil):
                    building.update(tile)
                pipe = tile.getPipe()
                if pipe:
                    pipe.update()


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
                if isinstance(tile.getBuilding(), EntityStorage):
                    center_x, center_y = draw_hexagone(game_map, ecran, x, y, tile, return_center=True)
                    pygame.draw.rect(ecran, (200, 200, 255), (center_x - 5, center_y - 5, 10, 10))
                if isinstance(tile.getBuilding(), EntitySawmil):
                    center_x, center_y = draw_hexagone(game_map, ecran, x, y, tile, return_center=True)
                    pygame.draw.rect(ecran, (160, 82, 45), (center_x - 4, center_y - 4, 8, 8)) 
                if isinstance(tile.getBuilding(), EntityFactory):
                    center_x, center_y = draw_hexagone(game_map, ecran, x, y, tile, return_center=True)
                    pygame.draw.rect(ecran, (100, 100, 100), (center_x - 5, center_y - 5, 10, 10))  


                

                if isinstance(tile.getBuilding(), EntityFactory):
                    center_x, center_y = draw_hexagone(game_map, ecran, x, y, tile, return_center=True)
                    size = 10  # taille du triangle
                    triangle_points = [
                        (center_x, center_y - size),  # sommet haut
                        (center_x - size, center_y + size),  # coin bas gauche
                        (center_x + size, center_y + size),  # coin bas droit
                    ]
                    pygame.draw.polygon(ecran, (255, 150, 100), triangle_points)


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
                    if hasattr(building, "selected_recipe") and building.selected_recipe:
                        lines.append(f"Recette sélectionnée : {building.selected_recipe}")

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
