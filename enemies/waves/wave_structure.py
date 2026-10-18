import pygame
from enemies.reg_enemy import Reg_Enemy
from enemies.fast_enemy import Fast_Enemy
from enemies.tank_enemy import Tank_Enemy
from enemies.zombie_enemy import Zombie_Enemy
from enemies.boss_enemy import Boss_Enemy



class Wave_Structure():
    def __init__(self, screen):
        self.screen = screen
        self.wave = 1
        self.current_chunk = 1
        self.last_wave = 10
        self.enemy_groups = []
        self.enemies = []
        self.enemy_reserves = 0
        self.enemy_btwn = 0
        # classes, not objects - attempt_spawn makes a new enemy from these each time
        self.enemy_type_map = {
            "NORMAL": Reg_Enemy,
            "SPEEDY": Fast_Enemy,
            "TANK": Tank_Enemy,
            "ZOMBIE": Zombie_Enemy,
            "BOSS": Boss_Enemy
        }

    def current_wave_display(self):
        text_surface = pygame.font.Font(None, 36).render(f"wave:{self.wave}", True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 50))

        return self.wave

    
    """ ADDED - helper method to get next info"""
    def get_next_enemy_chunk(self):
        if self.wave <= self.last_wave:
            self.enemy_reserves = self.enemy_groups[self.wave - 1][self.current_chunk]["enemy_count"]
            self.enemy_btwn = self.enemy_groups[self.wave - 1][self.current_chunk]["time_between"]
        else:
            self.enemy_reserves = 0
            self.enemy_btwn = 500
            

    def attempt_spawn(self, counter):
        spawned_enemy = None #setting variable to none so that the code wont be pissed

        counter -= 1
        if counter <= 0:
            # Spawn an enemy
            if self.enemy_reserves > 0:
                #spawned_enemy = self.enemy_groups[self.wave - 1][self.current_chunk]["enemy_type"] 
                spawned_enemy = self.enemy_type_map["NORMAL"](self.screen) #for now, just spawn normal enemies
                counter = self.enemy_btwn
                self.enemy_reserves -= 1
            else:  # or try to advance to next enemy chunk
                if self.current_chunk < self.enemy_groups[self.wave - 1]["total_chunks"]: 
                    self.current_chunk += 1
                    self.get_next_enemy_chunk()
                else:
                    counter = 500 # Wave time btwn, its like 5secs
                    self.current_chunk = 1
                    self.wave += 1
            
            # Handle next wave            
            if len(self.enemies) == 0:
                if self.wave-1 > self.last_wave:
                    return(None, 0)
                else:
                    counter = 5
        
        return (spawned_enemy, counter)
        

    """ ADDED - int conversion """
    def read(self, difficulty):
        in_header = True
        with open(f"enemies/waves/waves_{difficulty}_new.csv", mode="r") as file:
            for row in file:
                if in_header == True:
                    in_header = False
                    continue
                #--------------------------------Enemy Group Maker----------------------------------#
                wave_num, chunk, total_chunks, enemy_type, enemy_count, time_between = row.strip().split(',')

                wave_num = int(wave_num)
                chunk = int(chunk)
                total_chunks = int(total_chunks)
                enemy_type = self.enemy_type_map[enemy_type]
                enemy_count = int(enemy_count)
                time_between = int(time_between)

                self.enemy_groups.append({
                    "wave_num": wave_num,
                    "chunk": chunk,
                    "total_chunks": total_chunks,
                    "enemy_type": enemy_type,
                    "enemy_count": enemy_count,
                    "time_between": time_between
                })
                #------------------------------------------------------------------------------------#

        for i in range(len(self.enemy_groups)):
            print(f"Wave {self.enemy_groups[i]['wave_num']} info: {self.enemy_groups[i]['enemy_type']} count: {self.enemy_groups[i]['enemy_count']}, time between: {self.enemy_groups[i]['time_between']}")
        
        print(f"\nreading done! {len(self.enemy_groups)} enemy groups loaded.") # Print every enemy on earth


