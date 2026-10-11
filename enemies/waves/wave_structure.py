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
        self.enemy_type_map = {
            "NORMAL": Reg_Enemy(self.screen),
            "SPEEDY": Fast_Enemy(self.screen),
            "TANK": Tank_Enemy(self.screen),
            "ZOMBIE": Zombie_Enemy(self.screen),
            "BOSS": Boss_Enemy(self.screen)
        }

    def current_wave_display(self):
        text_surface = pygame.font.Font(None, 36).render(f"wave:{self.wave}", True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 50))

        return self.wave

    
    """ ADDED - helper method to get next info"""
    def get_next_enemy_chunk(self):
        if self.wave <= self.last_wave:
            wave_data = self.enemy_groups[self.wave - 1]
            self.enemy_reserves = wave_data[self.current_chunk]["enemy_count"]
            self.enemy_btwn = wave_data[self.current_chunk]["time_between"]
        else:
            self.enemy_reserves = 0
            self.enemy_btwn = 500


    def attempt_spawn(self, counter):
        spawned_enemy = None #setting variable to none so that the code wont be pissed

        if self.wave > self.last_wave:
            return (None, counter)

        counter -= 1
        if counter <= 0:
            # Spawn an enemy
            if self.enemy_reserves > 0:
                #spawned_enemy = self.enemy_groups[self.wave - 1][self.current_chunk]["enemy_type"] 
                spawned_enemy = self.enemy_type_map["NORMAL"] #for now, just spawn normal enemies
                counter = self.enemy_btwn
                self.enemy_reserves -= 1
            else:  # or try to advance to next enemy chunk
                wave_data = self.enemy_groups[self.wave - 1]
                if self.current_chunk < wave_data["total_chunks"]: 
                    self.current_chunk += 1
                    self.get_next_enemy_chunk()
                else:
                    counter = 500 # Wave time btwn, its like 5secs
                    self.current_chunk = 1
                    self.wave += 1
                    if self.wave <= self.last_wave:
                        self.get_next_enemy_chunk()
        
        return (self.enemy_type_map["NORMAL"], counter)
        

    """ ADDED - int conversion """
    def read(self, difficulty):
        self.enemy_groups = []
        waves_by_num = {}
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

                if wave_num not in waves_by_num:
                    waves_by_num[wave_num] = {"total_chunks": total_chunks}

                waves_by_num[wave_num]["total_chunks"] = total_chunks
                waves_by_num[wave_num][chunk] = {
                    "enemy_type": enemy_type,
                    "enemy_count": enemy_count,
                    "time_between": time_between
                }
                #------------------------------------------------------------------------------------#

        for wave_num in sorted(waves_by_num):
            self.enemy_groups.append(waves_by_num[wave_num])
            wave_data = waves_by_num[wave_num]
            for chunk in range(1, wave_data["total_chunks"] + 1):
                chunk_data = wave_data[chunk]
                print(f"Wave {wave_num} info: {chunk_data['enemy_type']} count: {chunk_data['enemy_count']}, time between: {chunk_data['time_between']}")
        
        self.last_wave = len(self.enemy_groups)
        self.wave = 1
        self.current_chunk = 1
        self.get_next_enemy_chunk()

        print(f"\nreading done! {len(self.enemy_groups)} waves loaded.") # Print every enemy on earth
