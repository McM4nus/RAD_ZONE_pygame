import pygame

class Weapon:
    def __init__(self, id, sound_manager):
        self.id = id                  # the ID string like "shotgun"
        self.name = id                # optional, keep for display if needed
        self.sound_manager = sound_manager

        # --- Weapon stats ---
        weapon_stats = {
            "knife": {
                "damage": 50,
                "range": 100,
                "fire_rate": 1.0,
                "width": 40,
                "full_auto": False
            },
            "pistol": {
                "damage": 20,
                "range": 400,
                "fire_rate": 0.1,
                "width": 20,
                "full_auto": False
            },
            "revolver": {
                "damage": 30,
                "range": 500,
                "fire_rate": 0.1,
                "width": 22,
                "full_auto": False
            },
            "shotgun": {
                "damage": 12,        # damage per pellet
                "range": 400,
                "fire_rate": 0.8,
                "width": 35,
                "full_auto": False,
                "pellets": 6,        # number of pellets
                "spread": 18         # degrees of spread
            },
            "crossbow": {
                "damage": 60,
                "range": 600,
                "fire_rate": 1.2,
                "width": 18,
                "full_auto": False
            },
            "machine_gun": {
                "damage": 15,
                "range": 600,
                "fire_rate": 0.1,
                "width": 22,
                "full_auto": True
            }
        }


        if id not in weapon_stats:
            raise ValueError(f"Unknown weapon id: {id}")

        stats = weapon_stats[id]

        # --- Assign basic stats ---
        self.damage = stats["damage"]
        self.range = stats["range"]
        self.fire_rate = stats["fire_rate"]
        self.width = stats["width"]
        self.full_auto = stats["full_auto"]
        self.angle_offset = stats.get("angle_offset", 0)  # ✅ rotation tweak

        # Optional: shotgun-only fields
        self.pellets = stats.get("pellets", 1)
        self.spread = stats.get("spread", 0)

        self._last_shot_time = 0

        # --- Weapon-specific scale and offset for drawing ---
        weapon_scales = {
            "knife": 0.5,
            "pistol": 0.4,
            "revolver": 0.45,
            "shotgun": 0.8,
            "crossbow": 0.75,
            "machine_gun": 0.6
        }

        weapon_offsets = {
            "knife": pygame.Vector2(10, 15),
            "pistol": pygame.Vector2(15, 20),
            "revolver": pygame.Vector2(18, 20),
            "shotgun": pygame.Vector2(30, 25),
            "crossbow": pygame.Vector2(25, 20),
            "machine_gun": pygame.Vector2(25, 20)
        }

        self.scale = weapon_scales.get(id, 0.6)
        self.offset = weapon_offsets.get(id, pygame.Vector2(20, 20))



    def equip(self):
        pass  # 🔇 intentionally silent

    def shoot(self, current_time):
        if current_time - self._last_shot_time >= self.fire_rate:
            self._last_shot_time = current_time
            return True
        return False

    def reload(self):
        pass  # 🔇 intentionally silent
