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
