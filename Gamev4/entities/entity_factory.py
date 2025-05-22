from .entity import Entity

class EntityFactory(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, inventory_capacity = 1000, linkable = True)
        self.selected_recipe = None
        self.recipes = {
            "plank": {"wood": 5},
            "stone": {"rock": 2},
            "coal": {"wood": 1},
            "brick": {"stone": 2, "coal": 5},
        }
    
    def set_recipe(self, recipe_name):
        if recipe_name in self.recipes:
            self.selected_recipe = recipe_name
            
    def can_craft(self):
        if not self.selected_recipe:
            return False
        cost = self.recipes[self.selected_recipe]
        for resource, amount in cost.items():
            if self.inventory.get(resource, 0) < amount:
                return False
        return True
    
    def craft(self):
        if self.can_craft():
            for resource, amount in self.recipes[self.selected_recipe].items():
                self.inventory[resource] -= amount
            self.inventory[self.selected_recipe] = self.inventory.get(self.selected_recipe, 0) + 1
            
    def getName(self):
        return "factory"
    
        
        