import pygame

BLACK = (0, 0, 0)             # Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
GRAY = (128, 128, 128)
import random
pygame.init()#iniciar pygame y hacer load a imagenes y sonidos
screen = pygame.display.set_mode([800, 600])
player_img = pygame.image.load("deep_elf.png").convert()
player_img.set_colorkey(BLACK)
fireball =  pygame.image.load("fireball2.png").convert()
fireball.set_colorkey(BLACK)
fireball2 =  pygame.image.load("fireball3.png").convert()
fireball2.set_colorkey(BLACK)
boulder =  pygame.image.load("boulder.png").convert()
boulder.set_colorkey(RED)
necro_magic = pygame.image.load("cloud_tloc_energy.png").convert()
necro_magic.set_colorkey(BLACK)
necro_magic = pygame.image.load("cloud_tloc_energy.png").convert()
necro_magic.set_colorkey(BLACK)
enemy_img1 = pygame.image.load("draconian_m.png").convert()
enemy_img1.set_colorkey(BLACK)
enemy_img2 = pygame.image.load("frost_giant.png").convert()
enemy_img2.set_colorkey(BLACK)
wall_img = pygame.image.load("brick_dark1.png").convert()
wall_img.set_colorkey(BLACK)
hp_img = pygame.image.load("i-heal.png").convert()
hp_img.set_colorkey(BLACK)
rate_of_fire = pygame.image.load("conjure_flame.png").convert()
rate_of_fire.set_colorkey(BLACK)
enemy_img3 = pygame.image.load("dragon.png").convert()
enemy_img3.set_colorkey(BLACK)
enemy_img4 = pygame.image.load("zonguldrok_lich2.png").convert()
enemy_img4.set_colorkey(BLACK)
enemy_img5 = pygame.image.load("gargoyle.png").convert()
enemy_img5.set_colorkey(BLACK)
enemy_img6 = pygame.image.load("test_spawner.png").convert()
enemy_img6.set_colorkey(BLACK)
enemy_img7 = pygame.image.load("test_spawner2.png").convert()
enemy_img7.set_colorkey(BLACK)
final_boss = pygame.image.load("hydra5.png").convert()
final_boss.set_colorkey(BLACK)
hydra_growls = pygame.mixer.Sound("European_Dragon_Roaring_and_breathe_fire-daniel-si.ogg")
hydra_growls.set_volume(.09)
dead_boss_sound = pygame.mixer.Sound("Dragon_Growl_01.ogg")
dead_boss_sound.set_volume(.05)
player_shoot = pygame.mixer.Sound("foom_0.wav")
player_shoot.set_volume(.09)
game_over_sound = pygame.mixer.Sound("Dark_Souls_-_You_Died_Sound_Effect.ogg")
game_over_sound.set_volume(.09)
pygame.mixer.music.load("The Dark Amulet.mp3")
pygame.mixer.music.set_volume(0.09)



class Wall(pygame.sprite.Sprite): # clase para crear todas las paredes
    """Paredes"""
    
    def __init__(self, x, y, width, height):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(wall_img,(width,height))
        #self.image.fill(GRAY)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
class Player(pygame.sprite.Sprite): #Clase del jugador
    
    # velocidad
    change_x = 0
    change_y = 0
    hit_points = 100 #cuanto da~o puedo recibir
    
    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
 
        self.image = player_img
        
 
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 
    def changespeed(self, x, y):
        #Cambia velocidad del jugador
        self.change_x += x
        self.change_y += y
 
    def move(self, walls):
 
        # movimiento de derecha a izquierda
        self.rect.x += self.change_x
 
        # si chocamos con una pared
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:

            if self.change_x > 0:#si me muevo hacia la derecha
                self.rect.right = block.rect.left #las cordenadas del lado derecho del rectangulo(player) seran igual al lado izquierdo de la pared que chocamos
            else:
                self.rect.left = block.rect.right #lo mismo pero para la izquierda
 
        # arriba/abajo
        self.rect.y += self.change_y
 
        
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
 
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
                
    def collide(self,bullets):#Si a player le da una bala, menos 25 hp
          bullet_list = pygame.sprite.spritecollide(self, bullets, False)
    
          for bullet in bullet_list:
              if pygame.sprite.spritecollide(self, bullets, False):
                  self.hit_points -= 25

    def enemy_collide(self, enemies):#si player toca sprite enemigo, hp = 0(insta death)
         enemy_list = pygame.sprite.spritecollide(self, enemies,False)
         for enemy in enemy_list:
             if pygame.sprite.spritecollide(self, enemies, False):
                 self.hit_points = 0

class Restore_health(pygame.sprite.Sprite): #esta clase crea el icono de el item de vida
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(hp_img,(60,60))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


          
class Enemy_bullet(pygame.sprite.Sprite): #crea balas enemigas, recibe imagen
    def __init__(self,pic,w,h):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pic,(w,h))
        

        self.rect = self.image.get_rect()


    def update(self,x,y):
        self.rect.x -= x
        self.rect.y -= y
        
        
class Enemy_bouncing_bullet(pygame.sprite.Sprite):#solo un enemigo usa esta clase, es para que la bala rebote 4 vezes
    counter = 0
    change_x = 3
    change_y = -1
    counter = 0
    def __init__(self,pic,w,h):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pic,(w,h))
        self.rect = self.image.get_rect()

    def update(self,x,y,walls,count):
        
        self.rect.x -= self.change_x
        if pygame.sprite.spritecollide(self, walls, False):
            self.counter += 1
            self.change_x *=-1

        self.rect.y -= self.change_y
        
 
                

    def flag(self): # con esto sabemos cuantas vezes reboto, la idea es destruit bala al rebotar 4 vezes
        if self.counter == 4:
            return True
        else:
            return False
        
       
class Enemy1(pygame.sprite.Sprite): # crear enemigo, solo un enemigo lo usa, para los demas se usa Enemy2
    def __init__(self, x, y,img,w,h):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(img,(w,h))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Enemy2(pygame.sprite.Sprite): #Crea enemigos, recibe imagen y cuantos hitpoints tendra el enemigo
    hit_points = 0

    change_x = 3
    change_y = 3
    
    def __init__(self, x, y,img,w,h,health):
        pygame.sprite.Sprite.__init__(self)
        self.hit_points = health

        self.image = pygame.transform.scale(img,(w,h))
        
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        
    def update(self,walls): #esto es para que el enemigo rebote misma idea que con el player update

        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)

        for block in block_hit_list:

          if self.change_x > 0:
                self.rect.right = block.rect.left 
                self.change_x *= -1
          else:
                self.rect.left = block.rect.right 
                self.change_x *= -1
 
        # arriba/abajo
        self.rect.y += self.change_y
 
        
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
 
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.change_y *= -1
            else:
                self.rect.top = block.rect.bottom
                self.change_y *= -1

    def bugFix(self,walls): #boss utiliza esta funcion para moverse
        self.rect.y += self.change_y
 
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
 
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.change_y *= -1
            else:
                self.rect.top = block.rect.bottom
                self.change_y *= -1

    def room3_enemy(self): #el enemigo en el cuarto 3 tenia problemas con colision
        self.rect.x += self.change_x
      

        if self.rect.x >= 460 or self.rect.x <=200:
            self.change_x *= -1
           
       
                
 
        # arriba/abajo
        self.rect.y += self.change_y
 
        
    
 
        if self.rect.y >= 320 or self.rect.y <=154:
            self.change_y *= -1
        
                
class Room():
    """Cada cuarto tiene su propia lista de objetos/enemigos"""
    wall_list = None
    enemy1_sprites = None
    enemy2_sprites = None
    enemy3_sprites = None
    enemy4_sprites = None
    enemy5_sprites = None
    enemy6_sprites = None
    enemy7_sprites_top = None
    enemy7_sprites_bot = None
    enemy8_sprites = None
    
    hp_list = None
    enemy_list = None
    rate_of_fire_list = None
    def __init__(self):
        self.wall_list=pygame.sprite.Group()
        self.enemy1_sprites = pygame.sprite.Group()
        self.enemy2_sprites = pygame.sprite.Group()
        self.enemy3_sprites = pygame.sprite.Group()
        self.enemy4_sprites = pygame.sprite.Group()
        self.enemy5_sprites = pygame.sprite.Group()
        self.enemy6_sprites = pygame.sprite.Group()
        self.enemy7_sprites_top = pygame.sprite.Group()
        self.enemy7_sprites_bot = pygame.sprite.Group()
        self.enemy8_sprites = pygame.sprite.Group()
        self.hp_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.rate_of_fire_list = pygame.sprite.Group()


class Room1(Room):
    """This creates all the walls in room 1"""
    
    def __init__(self):
        Room.__init__(self)
        
         
        # Lista de paredes
        walls = [[0, 0, 20, 600],
                 [780, 0, 20, 250],
                 [780, 300, 20, 600],
                 [20, 0, 760, 20],
                 [20, 580, 760, 20],
                 [450, 60, 20, 477],
                 [100,20,20,450],
                 [280,20,20,350],
                 [280,470,20,110]
                ]
        enemies1 = [[330,400]]
        hp_pot = Restore_health(415,0)
        self.hp_list.add(hp_pot)
            
        # Loop de la lista walls, para crearlas
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)

        for item in enemies1:
            enemy = Enemy1(item[0],item[1],enemy_img1,50,50)
            self.enemy1_sprites.add(enemy)
            self.enemy_list.add(enemy)
        
  
class Room2(Room):
    
    def __init__(self):
        Room.__init__(self)
        
         
        # Lista de paredes
        walls = [[0, 0, 20, 250],
                 [0, 300, 20, 300],
                 [780, 0, 20, 250],
                 [780, 300, 20, 600],
                 [20, 0, 760, 20],
                 [20, 580, 760, 20],
                 [262, 20, 26, 158],
                 [505,20,43,77],
                 [376,71,41,161],
                 [210,232,407,38],
                 [449,270,37,235]
                ]
        
        
        rate_of_fire_buff = Fire_rate(230,30)
        hp_pot = Restore_health(450,240)
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)

        self.rate_of_fire_list.add(rate_of_fire_buff)
        self.hp_list.add(hp_pot)
        
class Room3(Room):
    
    def __init__(self):
        Room.__init__(self)
        
         
        # Lista de paredes
        walls =[[0, 0, 20, 250],
                 [0, 300, 20, 300],
                 [780, 0, 20, 250],
                 [780, 300, 20, 600],
                 [20, 0, 760, 20],
                 [20, 580, 760, 20],
                 [71,70,39,39],
                 [71,160,39,39],
                [71,250,39,39],
                [71,339,39,39],
                [71,428,39,39],
                [71,518,39,39],
                [160,25,39,39],
                [160,114,39,39],
                [160,199,39,39],
                [160,289,39,39],
                [160,378,39,39],
                [160,468,39,39],
                [160,560,39,20],#
                [249,70,39,39],
                [249,518,39,39],
                [338,26,39,39],
                [338,115,39,39],
                [338,469,39,39],
                [338,561,39,20],
                [427,70,39,39],
                [427,518,39,39],
                [517,26,39,39],
                [517,115,39,39],
                [517,469,39,39],
                [517,561,39,20],
                [606,70,39,39],
                [606,160,39,39],
                [606,250,39,39],
                [606,339,39,39],
                [606,428,39,39],
                [606,518,39,39],
                [696,25,39,39],
                [696,114,39,39],
                [696,199,39,39],
                [696,289,39,39],
                [696,378,39,39],
                [696,468,39,39],
                [696,560,39,20]]

        hp_pot = Restore_health(90,130)
        fire_rate_buff = Fire_rate(115,440)
        self.rate_of_fire_list.add(fire_rate_buff)
        self.hp_list.add(hp_pot)        
                

        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)

        

class Room4(Room):
    
    def __init__(self):
        Room.__init__(self)
        
         
        # Lista de paredes
        walls =[[0, 0, 20, 250],
                 [0, 300, 20, 300],
                 [780, 0, 20, 250],
                 [780, 300, 20, 600],
                 [20, 0, 760, 20],
                 [20, 580, 760, 20],
                 [0,230,800,20],
                 [0,300,800,20]]

        
        hp_pot = Restore_health(350,240)

        self.hp_list.add(hp_pot)
                
                

                


        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)



class Room5(Room):
    
    def __init__(self):
        Room.__init__(self)
        
         
        # Lista de paredes
        walls =[[0, 0, 20, 600],
                 #[0, 300, 20, 300],
                 [780, 0, 20, 600],
                 #[780, 300, 20, 600],
                 [20, 0, 760, 20],
                 [20, 580, 760, 20],
                [138,110,25,50],
                [138,460,25,50]]


        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3])
            self.wall_list.add(wall)

        hp_pot = [[80,90]]

            
        rate_of_fire_buff = Fire_rate(110,460)
        
        self.rate_of_fire_list.add(rate_of_fire_buff)

        for item in hp_pot:
            pot = Restore_health(item[0],item[1])
            self.hp_list.add(pot)
        


                
class Player_Bullet(pygame.sprite.Sprite): #bala del jugador
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(fireball,(15,15))
        self.rect = self.image.get_rect()


    def update(self):
        self.rect.x += 7

class Fire_rate(pygame.sprite.Sprite):#crea sprite del buff
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(rate_of_fire,(30,30))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
 
def main():
   
    background = pygame.image.load("topwall2.png").convert()
    game_over = pygame.image.load("game_over.png").convert()
    game_over=pygame.transform.scale(game_over,(800,600))
    pygame.display.set_caption('Maze Runner')
    font = pygame.font.SysFont('Calibri', 20, True, False)
    font2 = pygame.font.SysFont('Calibri', 100, True, False)
    font3 = pygame.font.SysFont('Calibri', 20, True, False)
    font4 = pygame.font.SysFont('Calibri', 50, True, False)
    font5 = pygame.font.SysFont('Calibri', 30, True, False)
    font6 = pygame.font.SysFont('Calibri', 20, True, False)
    font7 = pygame.font.SysFont('Calibri', 60, True, False)
    
    player = Player(50, 50) # Crear jugador
    
    text_GAME_OVER = font2.render("GAME OVER",True,RED)
    text_start = font4.render("Press Enter to begin",True, RED)
    text_start2 = font5.render("Use Spacebar to fire",True, RED)
    you_win = font7.render("You Win!",True, BLUE)
    
    
    player_sprite = pygame.sprite.Group() # lista del sprite del jugador
    player_bullets = pygame.sprite.Group()#lista de balas del jugador
    player_sprite.add(player)
   
    enemy1_bullets = pygame.sprite.Group()#lista de balas
    enemy2_bullets = pygame.sprite.Group()
    enemy3_bullets = pygame.sprite.Group()
    enemy4_bullets = pygame.sprite.Group()
    enemy5_bullets = pygame.sprite.Group()
    enemy6_bullets = pygame.sprite.Group()
    enemy7_bullets = pygame.sprite.Group()
    enemy8_bullets1 = pygame.sprite.Group()
    enemy8_bullets2 = pygame.sprite.Group()
    enemy8_bullets3 = pygame.sprite.Group()
    enemy8_bullets4 = pygame.sprite.Group()
    boss_bullet1 = pygame.sprite.Group()
    boss_bullet2 = pygame.sprite.Group()
    boss_bullet3 = pygame.sprite.Group()    

    room4_bullets_top = pygame.sprite.Group()
    room4_bullets_bot = pygame.sprite.Group()
    
    
    
 
    rooms = [] #lista de cuartos
 
    room = Room1()
    rooms.append(room)
    room = Room2()
    rooms.append(room)
    room = Room3()
    rooms.append(room)
    room = Room4()
    rooms.append(room)
    room = Room5()
    rooms.append(room)
    current_room_no = 0
    current_room = rooms[current_room_no] #cuarto donde esta el juador

    
    enemy2 = Enemy2(500,500,enemy_img2,70,70,50)#Crear enemigos
    enemy3 =Enemy2(300,300,enemy_img3,90,90,200) 
    enemy4 =Enemy2(300,450,enemy_img3,90,90,200)
    enemy5 =Enemy2(380,40,enemy_img4,30,30,25) 
    enemy6 =Enemy2(500,110,enemy_img4,30,30,25) 
    enemy7 =Enemy2(500,180,enemy_img4,30,30,25) 
    enemy8 =Enemy2(352,239,enemy_img5,150,150,500) 
    boss = Enemy2(470,160,final_boss,250,250,1000)
   

    
        
        
        
    rooms[0].enemy2_sprites.add(enemy2) #a~adir enemigos a sus listas de cuartos
    rooms[0].enemy_list.add(enemy2)

    rooms[1].enemy_list.add(enemy3)
    rooms[1].enemy_list.add(enemy4)
    rooms[1].enemy_list.add(enemy5)
    rooms[1].enemy_list.add(enemy6)
    rooms[1].enemy_list.add(enemy7)
    rooms[2].enemy_list.add(enemy8)
    
    
    
    rooms[1].enemy1_sprites.add(enemy3)
    rooms[1].enemy2_sprites.add(enemy4)
    rooms[1].enemy3_sprites.add(enemy5)
    rooms[1].enemy4_sprites.add(enemy6)
    rooms[1].enemy5_sprites.add(enemy7)

    rooms[2].enemy6_sprites.add(enemy8)
    
    for i in range(30,750,60):
        room4_enemies = Enemy2(i,560,enemy_img6,20,20,25)
        rooms[3].enemy_list.add(room4_enemies)
        rooms[3].enemy7_sprites_bot.add(room4_enemies)

    for i in range(63,723,60):
        room4_enemies = Enemy2(i,20,enemy_img7,20,20,25)
        rooms[3].enemy_list.add(room4_enemies)
        rooms[3].enemy7_sprites_top.add(room4_enemies)
   
    rooms[4].enemy_list.add(boss)
    rooms[4].enemy8_sprites.add(boss)
    
    clock = pygame.time.Clock()
    
    done = False    
    enemy1_bullet_timer = 0
    enemy2_bullet_timer = 0
    enemy3_bullet_timer = 0
    enemy4_bullet_timer = 0
    enemy5_bullet_timer = 0
    enemy6_bullet_timer = 0
    enemy7_bullet_timer = 0
    enemy8_bullet_timer = 0
    boss_timer = 0
    room4_timer=0
    player_bullet_timer = 0
    fire_rate_timer = 0
    score = 0
    boss_sound_timer = 599
    player_shoot_flag = False # para controlar el Rate of fire
    fire_rate = False
    enemy1_alive = True 
    enemy2_alive = True
    enemy3_alive = True
    enemy4_alive = True
    enemy5_alive = True
    enemy6_alive = True
    enemy7_alive = True
    enemy8_alive = True
    boss_alive = True
    boss_room = False
    music = False
    win = False
    pygame.mixer.music.play(loops=-1)
    #pygame.mixer.music.queue("Heroic Demise (New).mp3")
    boss_music = False
    begin = False
    dead = False
    while not done:
        player_bullet_timer += 1 # controla fire rate del player
        if fire_rate == True: #para mas fire rate 
            fire_rate_timer +=1
        if fire_rate_timer == 400:
            fire_rate_timer = 0
            fire_rate = False
            
 
        # --- Event Processing ---
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
               
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, -5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, 5)
                if event.key == pygame.K_SPACE:
                    if player_shoot_flag == True:#crea bala de jugador, 1 por segundo
                        bullet = Player_Bullet()
                        bullet.rect.x = player.rect.x + 10
                        bullet.rect.y = player.rect.y
                        player_bullets.add(bullet)
                        player_shoot_flag = False
                        player_bullet_timer =0
                        player_shoot.play()
                    elif fire_rate == True and fire_rate_timer <= 400:#si el buff esta activo, disparar cuando quiera
                        bullet = Player_Bullet()
                        bullet.rect.x = player.rect.x + 10
                        bullet.rect.y = player.rect.y
                        player_bullets.add(bullet)
                if event.key == pygame.K_RETURN:#comenzar juego
                    begin = True
                        
                        
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, 5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -5)

         # --- Game Logic ---
    
        player.move(current_room.wall_list) #le paso la lista de paredes a player
        player_bullets.update() #lista de balas de jugador para que muevan las balas
        if player_bullet_timer == 60:
            player_shoot_flag = True # si pasa un segundo permitir disparo
            
        
        if current_room_no == 0: #logica de la primera habitacion
            
            enemy2.update(current_room.wall_list) #para que se mueva el enemigo2
            enemy1_bullet_timer += 1 #timer de los disparos
            enemy2_bullet_timer += 1
            if enemy1_bullet_timer == 80 and enemy1_alive == True:
                enemy_bullet = Enemy_bullet(fireball2,30,30)#creacion y posicion del disparo
                enemy_bullet.rect.x = 330 #este enemigo no se mueve, solo puse la bala en su posicion
                enemy_bullet.rect.y = 400
                enemy1_bullets.add(enemy_bullet)
                enemy1_bullet_timer = 0

            enemy1_bullets.update(5,0)#update de la bala del primer enemigo
            if enemy2_bullet_timer == 60 and enemy2_alive == True:
                enemy_bullet2 = Enemy_bullet(boulder,30,30) #creacion y posicion del disparo
                enemy_bullet2.rect.x = enemy2.rect.x
                enemy_bullet2.rect.y = enemy2.rect.y
                enemy2_bullets.add(enemy_bullet2)
                enemy2_bullet_timer = 0
            enemy2_bullets.update(5,0)#update de la bala del segundo enemigo
            
            for bullet in player_bullets:#por cada bala en lista de balas de jugador
                wall_hit_list = pygame.sprite.spritecollide(bullet,current_room.wall_list,False) #verificar si choco con una pared
                enemy1_hit_list = pygame.sprite.spritecollide(bullet,current_room.enemy1_sprites,False)#verifica si la bala le dio al primer enemigo NO lo borra,
                                                                                                       #se usa luego para borrar bala del player
                enemy2_hit_list = pygame.sprite.spritecollide(bullet,current_room.enemy2_sprites,False)
                if pygame.sprite.spritecollide(bullet,current_room.enemy1_sprites,True): #bala choca con enemigo, esto SI elimina enemigo
                    enemy1_alive = False
                    score +=10
                if pygame.sprite.spritecollide(bullet,current_room.enemy2_sprites,False): #bala choca con enemigo, esto NO elimina enemigo
                    enemy2.hit_points -= 25
                    if enemy2.hit_points <= 0:
                        if pygame.sprite.spritecollide(bullet,current_room.enemy2_sprites,True):#este si
                            enemy2_alive = False
                            score += 20
                for block in wall_hit_list:
                    player_bullets.remove(bullet) #si choca con pared, eliminar bala
                for enemy in enemy1_hit_list:
                    player_bullets.remove(bullet) #si choca con enemigo1, eliminar bala
                for enemy in enemy2_hit_list:
                    player_bullets.remove(bullet) #si choca con enemigo2, eliminar bala
                if bullet.rect.x > 800:
                    player_bullets.remove(bullet)

            #Destruye balas enemigas al chocar con pared
            for bullet in enemy1_bullets:
                wall_hit_list = pygame.sprite.spritecollide(enemy_bullet,current_room.wall_list,False)
                
                for block in wall_hit_list:
                    enemy1_bullets.remove(bullet) #si choca con pared, eliminar bala
                if pygame.sprite.spritecollide(player,enemy1_bullets,False):#si bala choca con jugador 
                    player.collide(enemy1_bullets)#enviarle bala a collide para que player reciba da~o
                    enemy1_bullets.remove(bullet)#borrar bala
            for bullet in enemy2_bullets:
                wall_hit_list = pygame.sprite.spritecollide(enemy_bullet2,current_room.wall_list,False)
                
                for block in wall_hit_list:
                    enemy2_bullets.remove(bullet) #si choca con pared, eliminar bala
                if pygame.sprite.spritecollide(player,enemy2_bullets,False):
                    player.collide(enemy2_bullets)
                    enemy2_bullets.remove(bullet)
            #cura a player cuando choca con un sprite de vida
            for healt_pot in current_room.hp_list:
                if pygame.sprite.spritecollide(player,current_room.hp_list,False):
                    current_room.hp_list.remove(healt_pot)#borrar sprite al tocarlo
                    player.hit_points += 25

            for enemy in current_room.enemy_list: # para ver si choque con enemigo
                if pygame.sprite.spritecollide(player,current_room.enemy_list,False):#si choco con enemigo
                        player.enemy_collide(current_room.enemy_list)#enviar lista de enemigos a enemy collide






                        
        #Logica del segundo cuarto        
        elif current_room_no == 1:
            enemy3_bullet_timer +=1
            enemy4_bullet_timer +=1
            enemy5_bullet_timer +=1
            enemy6_bullet_timer +=1
            enemy7_bullet_timer +=1
            
            if enemy3_bullet_timer == 80 and enemy3_alive == True:
                enemy_bullet3 = Enemy_bullet(fireball2,50,50) #creacion y posicion del disparo
                enemy_bullet3.rect.x = enemy3.rect.x
                enemy_bullet3.rect.y = enemy3.rect.y
                enemy3_bullets.add(enemy_bullet3)
                enemy3_bullet_timer = 0
            enemy3_bullets.update(5,0)

            if enemy4_bullet_timer == 60 and enemy4_alive == True:
                enemy_bullet4 = Enemy_bullet(fireball2,50,50) #creacion y posicion del disparo
                enemy_bullet4.rect.x = enemy4.rect.x
                enemy_bullet4.rect.y = enemy4.rect.y
                enemy4_bullets.add(enemy_bullet4)
                enemy4_bullet_timer = 0
            enemy4_bullets.update(5,0)

            if enemy5_bullet_timer == 150 and enemy5_alive == True:
                enemy_bullet5 = Enemy_bouncing_bullet(necro_magic,20,20) #creacion y posicion del disparo
                enemy_bullet5.rect.x = enemy5.rect.x
                enemy_bullet5.rect.y = enemy5.rect.y
                enemy5_bullets.add(enemy_bullet5)
                enemy5_bullet_timer = 0
            enemy5_bullets.update(5,-1,current_room.wall_list,2)

            if enemy6_bullet_timer == 90 and enemy6_alive == True:
                enemy_bullet6 = Enemy_bullet(necro_magic,20,20) #creacion y posicion del disparo
                enemy_bullet6.rect.x = enemy6.rect.x
                enemy_bullet6.rect.y = enemy6.rect.y
                enemy6_bullets.add(enemy_bullet6)
                enemy6_bullet_timer = 0
            enemy6_bullets.update(5,0)

            if enemy7_bullet_timer == 70 and enemy7_alive == True:
                enemy_bullet7 = Enemy_bullet(necro_magic,20,20) #creacion y posicion del disparo
                enemy_bullet7.rect.x = enemy7.rect.x
                enemy_bullet7.rect.y = enemy7.rect.y
                enemy7_bullets.add(enemy_bullet7)
                enemy7_bullet_timer = 0
            enemy7_bullets.update(5,0)

            
            for bullet in player_bullets:#por cada bala en lista de balas de jugador
                wall_hit_list = pygame.sprite.spritecollide(bullet,current_room.wall_list,False) #verificar si choco con una pared
                enemy_list = pygame.sprite.spritecollide(bullet,current_room.enemy_list,False)
                for block in wall_hit_list:
                    player_bullets.remove(bullet) #si choca con pared, eliminar bala

                for enemy in enemy_list:
                    player_bullets.remove(bullet)

                if pygame.sprite.spritecollide(bullet,current_room.enemy1_sprites,False): #bala choca con enemigo
                    enemy3.hit_points -= 25
                    if enemy3.hit_points <= 0:
                        if pygame.sprite.spritecollide(bullet,current_room.enemy1_sprites,True):
                            enemy3_alive = False
                            score += 50
                            
                if pygame.sprite.spritecollide(bullet,current_room.enemy2_sprites,False): #bala choca con enemigo
                    enemy4.hit_points -= 25
                    if enemy4.hit_points <= 0:
                        if pygame.sprite.spritecollide(bullet,current_room.enemy2_sprites,True):
                            enemy4_alive = False
                            score +=50

                if pygame.sprite.spritecollide(bullet,current_room.enemy3_sprites,False): 
                    enemy5.hit_points -= 25
                    if enemy5.hit_points <= 0:
                        if pygame.sprite.spritecollide(bullet,current_room.enemy3_sprites,True):
                            enemy5_alive = False
                            score += 15
                if pygame.sprite.spritecollide(bullet,current_room.enemy4_sprites,False): 
                    enemy6.hit_points -= 25
                    if enemy6.hit_points <= 0:
                        if pygame.sprite.spritecollide(bullet,current_room.enemy4_sprites,True):
                            enemy6_alive = False
                            score += 15

                if pygame.sprite.spritecollide(bullet,current_room.enemy5_sprites,False): 
                    enemy7.hit_points -= 25
                    if enemy7.hit_points <= 0:
                        if pygame.sprite.spritecollide(bullet,current_room.enemy5_sprites,True):
                            enemy7_alive = False
                            score += 15
            
                    if bullet.rect.x > 800:
                        player_bullets.remove(bullet)#borrar bala si se sale de la pantalla


            for healt_pot in current_room.hp_list:#health pot
                if pygame.sprite.spritecollide(player,current_room.hp_list,False):
                    current_room.hp_list.remove(healt_pot)
                    player.hit_points += 25

            for enemy in current_room.enemy_list: # para ver si choque con enemigo
                if pygame.sprite.spritecollide(player,current_room.enemy_list,False):
                        player.enemy_collide(current_room.enemy_list)

            for fire_rate in current_room.rate_of_fire_list:#buff de Fire rate
                if pygame.sprite.spritecollide(player,current_room.rate_of_fire_list,False):
                    current_room.rate_of_fire_list.remove(fire_rate)
                    fire_rate = True#prender bandera del buff

            for bullet in enemy3_bullets:
                wall_hit_list = pygame.sprite.spritecollide(enemy_bullet3,current_room.wall_list,False)
                
                for block in wall_hit_list:
                    enemy3_bullets.remove(bullet) #si choca con pared, eliminar bala
                if pygame.sprite.spritecollide(player,enemy3_bullets,False):
                    player.collide(enemy3_bullets)
                    enemy3_bullets.remove(bullet)

                    
            for bullet in enemy4_bullets:
                wall_hit_list = pygame.sprite.spritecollide(enemy_bullet4,current_room.wall_list,False)
                
                for block in wall_hit_list:
                    enemy4_bullets.remove(bullet) #si choca con pared, eliminar bala
                if pygame.sprite.spritecollide(player,enemy4_bullets,False):
                    player.collide(enemy4_bullets)
                    enemy4_bullets.remove(bullet)
                    

            for bullet in enemy5_bullets:
                wall_hit_list = pygame.sprite.spritecollide(enemy_bullet5,current_room.wall_list,False)
##                
                for block in wall_hit_list:
                    if enemy_bullet5.flag() == True:
                       enemy5_bullets.remove(bullet) #si choca con pared, eliminar bala
                if pygame.sprite.spritecollide(player,enemy5_bullets,False):
                    player.collide(enemy5_bullets)
                    enemy5_bullets.remove(bullet)
                    

            for bullet in enemy6_bullets:
                wall_hit_list = pygame.sprite.spritecollide(enemy_bullet6,current_room.wall_list,False)
                
                for block in wall_hit_list:
                    enemy6_bullets.remove(bullet) #si choca con pared, eliminar bala
                if pygame.sprite.spritecollide(player,enemy6_bullets,False):
                    player.collide(enemy6_bullets)
                    enemy6_bullets.remove(bullet)


            for bullet in enemy7_bullets:
                wall_hit_list = pygame.sprite.spritecollide(enemy_bullet7,current_room.wall_list,False)
                
                for block in wall_hit_list:
                    enemy7_bullets.remove(bullet) #si choca con pared, eliminar bala
                if pygame.sprite.spritecollide(player,enemy7_bullets,False):
                    player.collide(enemy7_bullets)
                    enemy7_bullets.remove(bullet)
                    
        elif current_room_no == 2:
            enemy8_bullet_timer +=1
            enemy8.room3_enemy()
            if enemy8_bullet_timer == 100 and enemy8_alive == True:
                bullet1 = Enemy_bullet(necro_magic,35,35)
                bullet1.rect.x = enemy8.rect.x
                bullet1.rect.y = enemy8.rect.y
                bullet2 = Enemy_bullet(necro_magic,35,35)
                bullet2.rect.x = enemy8.rect.x+100
                bullet2.rect.y = enemy8.rect.y
                bullet3 = Enemy_bullet(necro_magic,35,35)
                bullet3.rect.x = enemy8.rect.x
                bullet3.rect.y = enemy8.rect.y+100
                bullet4 = Enemy_bullet(necro_magic,35,35)
                bullet4.rect.x = enemy8.rect.x+100
                bullet4.rect.y = enemy8.rect.y+100
                enemy8_bullets1.add(bullet1)
                enemy8_bullets2.add(bullet2)
                enemy8_bullets3.add(bullet3)
                enemy8_bullets4.add(bullet4)
                enemy8_bullet_timer =0
            enemy8_bullets1.update(5,10)
            enemy8_bullets2.update(-5,10)
            enemy8_bullets3.update(5,-10)
            enemy8_bullets4.update(-5,-10)
            for bullet in player_bullets:
                if pygame.sprite.spritecollide(bullet,current_room.enemy6_sprites,False): #bala choca con enemigo
                    enemy8.hit_points -= 25
                    if enemy8.hit_points <= 0:
                        if pygame.sprite.spritecollide(bullet,current_room.enemy6_sprites,True):
                            enemy8_alive = False
                            score += 100
                            player_bullets.remove(bullet)
                wall_hit_list = pygame.sprite.spritecollide(bullet,current_room.wall_list,False) #verificar si choco con una pared
                for block in wall_hit_list:
                    player_bullets.remove(bullet) #si choca con pared, eliminar bala
                enemy_list = pygame.sprite.spritecollide(bullet,current_room.enemy_list,False)
                for enemy in enemy_list: # si bala choca con enemigo borrar bala
                    player_bullets.remove(bullet)
                    
            for bullet in enemy8_bullets1:#borrar bala si se va de la pantalla o si le da al jugador, esto se repite 4 vezes
                if bullet.rect.y<0:
                    enemy8_bullets1.remove(bullet)
                if pygame.sprite.spritecollide(player,enemy8_bullets1,False):
                    player.collide(enemy8_bullets1)
                    enemy8_bullets1.remove(bullet)

            for bullet in enemy8_bullets2:
                if bullet.rect.y<0:
                    enemy8_bullets2.remove(bullet)
                if pygame.sprite.spritecollide(player,enemy8_bullets2,False):
                    player.collide(enemy8_bullets2)
                    enemy8_bullets2.remove(bullet)
                    
            for bullet in enemy8_bullets3:
                if bullet.rect.y>600:
                    enemy8_bullets3.remove(bullet)
                if pygame.sprite.spritecollide(player,enemy8_bullets3,False):
                    player.collide(enemy8_bullets3)
                    enemy8_bullets3.remove(bullet)

            for bullet in enemy8_bullets4:
                if bullet.rect.y>600:
                    enemy8_bullets4.remove(bullet)
                if pygame.sprite.spritecollide(player,enemy8_bullets4,False):
                    player.collide(enemy8_bullets4)
                    enemy8_bullets4.remove(bullet)
                    
            for enemy in current_room.enemy_list: # para ver si choque con enemigo
                if pygame.sprite.spritecollide(player,current_room.enemy_list,False):
                        player.enemy_collide(current_room.enemy_list)

            for healt_pot in current_room.hp_list:
                if pygame.sprite.spritecollide(player,current_room.hp_list,False):
                    current_room.hp_list.remove(healt_pot)
                    player.hit_points += 25

            for fire_rate in current_room.rate_of_fire_list:#buff de Fire rate
                if pygame.sprite.spritecollide(player,current_room.rate_of_fire_list,False):
                    current_room.rate_of_fire_list.remove(fire_rate)
                    fire_rate = True#prender bandera del buff
                
                



        elif current_room_no == 3:
            room4_timer+=1
            if room4_timer==200:
                for enemy in current_room.enemy7_sprites_bot: #crear balas en ciclo
                    bullet = Enemy_bullet(necro_magic,15,15)
                    bullet.rect.x = enemy.rect.x
                    bullet.rect.y = enemy.rect.y
                    room4_bullets_bot.add(bullet)
                    room4_timer=0
            room4_bullets_bot.update(0,5)

            if room4_timer==100:
                for enemy in current_room.enemy7_sprites_top:#crear balas en ciclo
                    bullet = Enemy_bullet(necro_magic,15,15)
                    bullet.rect.x = enemy.rect.x
                    bullet.rect.y = enemy.rect.y
                    room4_bullets_top.add(bullet)
            room4_bullets_top.update(0,-5)

            for bullet in room4_bullets_bot: #verificar y borrar bala si choco con jugador
                bullet_hit_list = pygame.sprite.spritecollide(player,room4_bullets_bot,True) 
                for bullet2 in bullet_hit_list:
                    player.collide(bullet_hit_list)
                    
                if bullet.rect.y<0:# borrar bala al salir de pantalla
                    room4_bullets_bot.remove(bullet)

            for bullet in room4_bullets_top:
                bullet_hit_list = pygame.sprite.spritecollide(player,room4_bullets_top,True) 
                for bullet2 in bullet_hit_list:
                    player.collide(bullet_hit_list)
                    
                if bullet.rect.y>600:
                    room4_bullets_top.remove(bullet)

            for bullet in player_bullets:
                if bullet.rect.x>800:
                    player_bullets.remove(bullet)

            for healt_pot in current_room.hp_list:
                if pygame.sprite.spritecollide(player,current_room.hp_list,False):
                    current_room.hp_list.remove(healt_pot)
                    player.hit_points += 25


        elif current_room_no == 4:
            
            boss_room = True #esta bandera es para ver el hp del boss
            boss_sound_timer +=1#timer del sound effec
            if boss_sound_timer == 600:
                if win == False: # mientras la batalla continue, igual el sonido
                    hydra_growls.play()
                    boss_sound_timer =0
            if music == False:
                pygame.mixer.music.stop()#detener musica anterior
                pygame.mixer.music.load("Heroic Demise (New).mp3")#load a la nueva
                pygame.mixer.music.set_volume(0.09)
                pygame.mixer.music.play()
                music = True#bandera para que no se vuelva a poner la musica
            boss_timer +=1#timer de los disparos
            boss.bugFix(current_room.wall_list)#movimiento del boss
            for bullet in player_bullets:
                if pygame.sprite.spritecollide(bullet,current_room.enemy8_sprites,False): #bala choca con enemigo
                    boss.hit_points -= 25
                    if boss.hit_points <= 0:
                        score += 1000
                        if pygame.sprite.spritecollide(bullet,current_room.enemy8_sprites,True):#destruir enemigo
                            boss_alive = False
                            player_bullets.remove(bullet)#borrar bala
                            dead_boss_sound.play()
                            win = True #win screen
                wall_hit_list = pygame.sprite.spritecollide(bullet,current_room.wall_list,False) #verificar si choco con una pared
                for block in wall_hit_list:
                    player_bullets.remove(bullet) #si choca con pared, eliminar bala
                enemy_list = pygame.sprite.spritecollide(bullet,current_room.enemy_list,False)
                for enemy in enemy_list:
                    player_bullets.remove(bullet)
            
            
            for enemy in current_room.enemy_list: # para ver si choque con enemigo
                if pygame.sprite.spritecollide(player,current_room.enemy_list,False):
                        player.enemy_collide(current_room.enemy_list)

            if boss_timer == 100 and boss_alive == True: #creacion de las balas
                bullet1 = Enemy_bullet(fireball2,35,35)
                bullet1.rect.x = boss.rect.x-100
                bullet1.rect.y = boss.rect.y
                bullet2 = Enemy_bullet(fireball2,35,35)
                bullet2.rect.x = boss.rect.x+100
                bullet2.rect.y = boss.rect.y
                bullet3 = Enemy_bullet(fireball2,35,35)
                bullet3.rect.x = boss.rect.x
                bullet3.rect.y = boss.rect.y+100
                boss_bullet1.add(bullet1)
                boss_bullet2.add(bullet2)
                boss_bullet3.add(bullet3)
                boss_timer = 0
                
            boss_bullet1.update(5,-1)
            boss_bullet2.update(5,-1)
            boss_bullet3.update(5,-1)
            for bullet in boss_bullet1: #verificar si choco con pared o jugador
                bullet_hit_list = pygame.sprite.spritecollide(player,boss_bullet1,True)
                wall_hit_list = pygame.sprite.spritecollide(bullet1,current_room.wall_list,False)
##                
            
                for bullet2 in bullet_hit_list:
                    player.collide(bullet_hit_list)

                for block in wall_hit_list:
                    boss_bullet1.remove(bullet)
                

            for bullet in boss_bullet2:
                bullet_hit_list = pygame.sprite.spritecollide(player,boss_bullet2,True)
                wall_hit_list = pygame.sprite.spritecollide(bullet2,current_room.wall_list,False)
                
                
                for bullet2 in bullet_hit_list:
                    player.collide(bullet_hit_list)

                for block in wall_hit_list:
                    boss_bullet2.remove(bullet)

            for bullet in boss_bullet3:
                bullet_hit_list = pygame.sprite.spritecollide(player,boss_bullet3,True)
                wall_hit_list = pygame.sprite.spritecollide(bullet3,current_room.wall_list,False)
##                
               
                for bullet2 in bullet_hit_list:
                    player.collide(bullet_hit_list)

                for block in wall_hit_list:
                    boss_bullet3.remove(bullet)

            for fire_rate in current_room.rate_of_fire_list: 
                if pygame.sprite.spritecollide(player,current_room.rate_of_fire_list,False):
                    current_room.rate_of_fire_list.remove(fire_rate)
                    fire_rate = True


            for healt_pot in current_room.hp_list:#health pot
                if pygame.sprite.spritecollide(player,current_room.hp_list,False):
                    current_room.hp_list.remove(healt_pot)
                    player.hit_points += 25

            
            

                
                    

           
                
            

        
        



                        
         
        if player.rect.x > 801: #al moverme de cuarto cambiar current room no, y vaciar lista de balas
            if current_room_no == 0:
                enemy1_bullets.empty()
                enemy2_bullets.empty()
                current_room_no = 1
                current_room = rooms[current_room_no]
                player.rect.x = 50
                player.rect.y = 250
                player_bullets.empty()
            elif current_room_no == 1:
                current_room_no = 2
                current_room = rooms[current_room_no]
                player.rect.x = 50
                player.rect.y = 250
                enemy3_bullets.empty()
                enemy4_bullets.empty()
                enemy5_bullets.empty()
                enemy6_bullets.empty()
                enemy7_bullets.empty()
                player_bullets.empty()
            elif current_room_no == 2:
                current_room_no = 3
                current_room = rooms[current_room_no]
                player.rect.x = 50
                player.rect.y = 250
                enemy3_bullets.empty()
                enemy4_bullets.empty()
                enemy5_bullets.empty()
                enemy6_bullets.empty()
                enemy7_bullets.empty()
                enemy8_bullets1.empty()
                enemy8_bullets2.empty()
                enemy8_bullets3.empty()
                enemy8_bullets4.empty()
                room4_bullets_bot.empty()
                room4_bullets_top.empty()
                player_bullets.empty()
            elif current_room_no == 3:
                current_room_no = 4
                current_room = rooms[current_room_no]
                player.rect.x = 50
                player.rect.y = 250
                room4_bullets_bot.empty()
                room4_bullets_top.empty()
                enemy8_bullets1.empty()
                enemy8_bullets2.empty()
                enemy8_bullets3.empty()
                enemy8_bullets4.empty()
                player_bullets.empty()
        if player.rect.x < 0 and current_room_no ==1: #retroceder
            current_room_no = 0
            current_room = rooms[current_room_no]
            player.rect.x = 790
            enemy3_bullets.empty()
            enemy4_bullets.empty()
            enemy5_bullets.empty()
            enemy6_bullets.empty()
            enemy7_bullets.empty()
            room4_bullets_bot.empty()
            room4_bullets_top.empty()
            player_bullets.empty()
        if player.rect.x < 0 and current_room_no ==2:
            current_room_no = 1
            current_room = rooms[current_room_no]
            player.rect.x = 790
            enemy3_bullets.empty()
            enemy4_bullets.empty()
            enemy5_bullets.empty()
            enemy6_bullets.empty()
            enemy7_bullets.empty()
            enemy8_bullets1.empty()
            enemy8_bullets2.empty()
            enemy8_bullets3.empty()
            enemy8_bullets4.empty()
            room4_bullets_bot.empty()
            room4_bullets_top.empty()
            player_bullets.empty()
        if player.rect.x < 0 and current_room_no ==3:
            current_room_no = 2
            current_room = rooms[current_room_no]
            player.rect.x = 790
            enemy3_bullets.empty()
            enemy4_bullets.empty()
            enemy5_bullets.empty()
            enemy6_bullets.empty()
            enemy7_bullets.empty()
            room4_bullets_bot.empty()
            room4_bullets_top.empty()
            player_bullets.empty()
        if player.rect.x < 0 and current_room_no ==4:
            current_room_no = 3
            current_room = rooms[current_room_no]
            player.rect.x = 790
            player_bullets.empty()
         
        # --- Drawing ---
        screen.fill(BLACK)
        screen.blit(background,[0,0])
        if begin == False:
            screen.blit(text_start,[150,250])
            screen.blit(text_start2,[150,300])
        elif begin == True and dead == False and win == False:               
            text_HP = font.render("HP: "+ str(player.hit_points),True,GREEN)
            text_boss_health = font3.render("BOSS HP: "+str(boss.hit_points),True, RED)
            text_score = font6.render("Score :"+str(score),True, WHITE)
            player_sprite.draw(screen)
            current_room.wall_list.draw(screen)
            current_room.enemy1_sprites.draw(screen)
            current_room.enemy2_sprites.draw(screen)
            current_room.enemy3_sprites.draw(screen)
            current_room.enemy4_sprites.draw(screen)
            current_room.enemy5_sprites.draw(screen)
            current_room.enemy6_sprites.draw(screen)
            current_room.enemy7_sprites_top.draw(screen)
            current_room.enemy7_sprites_bot.draw(screen)
            current_room.enemy8_sprites.draw(screen)
            current_room.hp_list.draw(screen)
            current_room.rate_of_fire_list.draw(screen)
            player_bullets.draw(screen)
            enemy1_bullets.draw(screen)
            enemy2_bullets.draw(screen)
            enemy3_bullets.draw(screen)
            enemy4_bullets.draw(screen)
            enemy5_bullets.draw(screen)
            enemy6_bullets.draw(screen)
            enemy7_bullets.draw(screen)
            enemy8_bullets1.draw(screen)
            enemy8_bullets2.draw(screen)
            enemy8_bullets3.draw(screen)
            enemy8_bullets4.draw(screen)
            boss_bullet1.draw(screen)
            boss_bullet2.draw(screen)
            boss_bullet3.draw(screen)
            room4_bullets_top.draw(screen)
            room4_bullets_bot.draw(screen)
            screen.blit(text_HP, [0, 0])
            screen.blit(text_score,[200,0])
        elif win == True:
            screen.blit(you_win,[300,300])
            text_score = font6.render("Score :"+str(score),True, WHITE)
            screen.blit(text_score,[300,400])
        if player.hit_points <= 0:
            game_over_sound.play()
            dead = True
        if boss_room == True and win == False:
            screen.blit(text_boss_health,[670,0])
        if dead == True:
            player_sprite.remove(player)
            screen.blit(game_over,[0,0])
        
            
    
        
        
 
        pygame.display.flip()
 
        clock.tick(60)
 
    pygame.quit()
 

main()  
