import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
GRAY = (128, 128, 128)

pygame.init()
screen = pygame.display.set_mode([800, 600])
player_img = pygame.image.load("deep_elf.png").convert()
player_img.set_colorkey(BLACK)
fireball =  pygame.image.load("fireball2.png").convert()
fireball.set_colorkey(BLACK)
fireball2 =  pygame.image.load("fireball3.png").convert()
fireball2.set_colorkey(BLACK)
boulder =  pygame.image.load("boulder.png").convert()
boulder.set_colorkey(RED)
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
pygame.mixer.music.load("The Dark Amulet.mp3")
pygame.mixer.music.set_volume(0.09)

class Wall(pygame.sprite.Sprite):
    """Paredes"""
    
    def __init__(self, x, y, width, height):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(wall_img,(width,height))
        #self.image.fill(GRAY)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
class Player(pygame.sprite.Sprite):
    
    # velocidad
    change_x = 0
    change_y = 0
    hit_points = 100
    
    def __init__(self, x, y):
        
        pygame.sprite.Sprite.__init__(self)
 
        # loads sprite
        self.image = player_img
        #self.image.fill(WHITE)
 
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
                
    def collide(self,bullets):
          bullet_list = pygame.sprite.spritecollide(self, bullets, False)
    
          for bullet in bullet_list:
              if pygame.sprite.spritecollide(self, bullets, False):
                  self.hit_points -= 25

    def enemy_collide(self, enemies):
         enemy_list = pygame.sprite.spritecollide(self, enemies,False)
         for enemy in enemy_list:
             if pygame.sprite.spritecollide(self, enemies, False):
                 self.hit_points = 0

class Restore_health(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(hp_img,(60,60))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


          
class Enemy_bullet(pygame.sprite.Sprite):
    def __init__(self,pic,w,h):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pic,(w,h))
        #self.image.fill(PURPLE)

        self.rect = self.image.get_rect()


    def update(self):
        self.rect.x -= 5
        
class Enemy1(pygame.sprite.Sprite):
    def __init__(self, x, y,img,w,h):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(img,(w,h))
       # self.image.fill(RED)
 
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Enemy2(pygame.sprite.Sprite):
    hit_points = 0

    change_x = 3
    change_y = 3
    
    def __init__(self, x, y,img,w,h,health):
        pygame.sprite.Sprite.__init__(self)
        self.hit_points = health

        self.image = pygame.transform.scale(img,(w,h))
        #self.image.fill(RED)
        
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        
    def update(self,walls):

        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)

        for block in block_hit_list:

          if self.change_x > 0:#si me muevo hacia la derecha
                self.rect.right = block.rect.left #las cordenadas del lado derecho del rectangulo(player) seran igual al lado izquierdo de la pared que chocamos
                self.change_x *= -1
          else:
                self.rect.left = block.rect.right #lo mismo pero para la izquierda
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
            
class Room():
    """Cada cuarto tiene su propia lista de objetos/enemigos"""
    wall_list = None
    enemy1_sprites = None
    enemy2_sprites = None
    enemy3_sprites = None
    hp_list = None
    enemy_list = None
    rate_of_fire_list = None
    def __init__(self):
        self.wall_list=pygame.sprite.Group()
        self.enemy1_sprites = pygame.sprite.Group()
        self.enemy2_sprites = pygame.sprite.Group()
        self.enemy3_sprites = pygame.sprite.Group()
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
        
##        for i in range(0,600,20):
##            wall = Wall(0,i,20,20)
##            self.wall_list.add(wall)
##
##        for i in range(0,250,20):
##            wall = Wall(780,i,20,20)
##            self.wall_list.add(wall)
##
##        for i in range(0,780,20):
##            wall = Wall(i,0,20,20)
##            self.wall_list.add(wall)
##
##        for i in range(0,450,20):
##            wall = Wall(100,i,20,20)
##            self.wall_list.add(wall)
##
##        for i in range(0,378,20):
##            wall = Wall(300,i,20,20)
##            self.wall_list.add(wall)
##
##        for i in range(0,800,20):
##            wall = Wall(i,580,20,20)
##            self.wall_list.add(wall)
##
##        for i in range(340,780,20):
##            wall = Wall(780,i,20,20)
##            self.wall_list.add(wall)   
            
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
        
        

            
class Player_Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(fireball,(15,15))
        #self.image.fill(RED)

        self.rect = self.image.get_rect()


    def update(self):
        self.rect.x += 5

class Fire_rate(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(rate_of_fire,(30,30))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
 
def main():

   # pygame.init()
   
    background = pygame.image.load("topwall2.png").convert()
    pygame.display.set_caption('Maze Runner')
    font = pygame.font.SysFont('Calibri', 20, True, False)
    font2 = pygame.font.SysFont('Calibri', 100, True, False)
    
    player = Player(50, 50) # Crear jugador
    
    text_GAME_OVER = font2.render("GAME OVER",True,RED)
    
    player_sprite = pygame.sprite.Group() # lista del sprite del jugador
    player_bullets = pygame.sprite.Group()#lista de balas del jugador
    player_sprite.add(player)
   
    enemy1_bullets = pygame.sprite.Group()#lista de balas
    enemy2_bullets = pygame.sprite.Group()
    enemy3_bullets = pygame.sprite.Group()
    enemy4_bullets = pygame.sprite.Group()
    
    
 
    rooms = [] #lista de cuartos
 
    room = Room1()
    rooms.append(room)
    room = Room2()
    rooms.append(room)
    current_room_no = 0 
    current_room = rooms[current_room_no] #cuarto donde esta el juador
    
    enemy2 = Enemy2(500,500,enemy_img2,70,70,50)# Crear enemigo2 del room 1
    
    enemy3 =Enemy2(300,350,enemy_img3,90,90,200) #primer enemigo del room 2
    enemy4 =Enemy2(300,450,enemy_img3,90,90,200) #segundo enemigo del room 2
    enemy5 =Enemy2(380,40,enemy_img4,30,30,25) #tercer enemigo del room 2
    
    rooms[0].enemy2_sprites.add(enemy2)#a~adir enemigo 2 a la lista de enemigo2
    rooms[0].enemy_list.add(enemy2)# y a la lista de todos los enemigos

    rooms[1].enemy_list.add(enemy3)
    rooms[1].enemy_list.add(enemy4)
    rooms[1].enemy_list.add(enemy5)
    rooms[1].enemy1_sprites.add(enemy3)
    rooms[1].enemy2_sprites.add(enemy4)
    rooms[1].enemy3_sprites.add(enemy5)
    
    clock = pygame.time.Clock()
    
    done = False
    
    enemy1_bullet_timer = 0
    enemy2_bullet_timer = 0
    enemy3_bullet_timer = 0
    enemy4_bullet_timer = 0
    player_bullet_timer = 0
    fire_rate_timer = 0
    player_shoot_flag = False # para controlar el Rate of fire
    fire_rate = False
    enemy1_alive = True 
    enemy2_alive = True
    enemy3_alive = True
    enemy4_alive = True
    pygame.mixer.music.play(loops=-1)
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
                    if player_shoot_flag == True:
                        bullet = Player_Bullet()
                        bullet.rect.x = player.rect.x + 10
                        bullet.rect.y = player.rect.y
                        player_bullets.add(bullet)
                        player_shoot_flag = False
                        player_bullet_timer =0
                    elif fire_rate == True and fire_rate_timer <= 400:
                        bullet = Player_Bullet()
                        bullet.rect.x = player.rect.x + 10
                        bullet.rect.y = player.rect.y
                        player_bullets.add(bullet)
                        
                        
 
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
    
        player.move(current_room.wall_list) #le paso la lista de paredes
        player_bullets.update() #lista de balas de jugador
        if player_bullet_timer == 60:
            player_shoot_flag = True
            
        
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

            enemy1_bullets.update()#update de la bala del primer enemigo
            if enemy2_bullet_timer == 60 and enemy2_alive == True:
                enemy_bullet2 = Enemy_bullet(boulder,30,30) #creacion y posicion del disparo
                enemy_bullet2.rect.x = enemy2.rect.x
                enemy_bullet2.rect.y = enemy2.rect.y
                enemy2_bullets.add(enemy_bullet2)
                enemy2_bullet_timer = 0
            enemy2_bullets.update()#update de la bala del segundo enemigo
            
            for bullet in player_bullets:#por cada bala en lista de balas de jugador
                wall_hit_list = pygame.sprite.spritecollide(bullet,current_room.wall_list,False) #verificar si choco con una pared
                enemy1_hit_list = pygame.sprite.spritecollide(bullet,current_room.enemy1_sprites,False)#verifica si la bala le dio al primer enemigo NO lo borra
                enemy2_hit_list = pygame.sprite.spritecollide(bullet,current_room.enemy2_sprites,False)#verifica si la bala le dio al primer enemigo NO lo borra
                if pygame.sprite.spritecollide(bullet,current_room.enemy1_sprites,True): #bala choca con enemigo, esto SI elimina enemigo
                    enemy1_alive = False
                if pygame.sprite.spritecollide(bullet,current_room.enemy2_sprites,False): #bala choca con enemigo, esto SI elimina enemigo
                    enemy2.hit_points -= 25
                    if enemy2.hit_points <= 0:
                        if pygame.sprite.spritecollide(bullet,current_room.enemy2_sprites,True):
                            enemy2_alive = False
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
                if pygame.sprite.spritecollide(player,enemy1_bullets,False):
                    player.collide(enemy1_bullets)
                    enemy1_bullets.remove(bullet)
            for bullet in enemy2_bullets:
                wall_hit_list = pygame.sprite.spritecollide(enemy_bullet2,current_room.wall_list,False)
                
                for block in wall_hit_list:
                    enemy2_bullets.remove(bullet) #si choca con pared, eliminar bala
                if pygame.sprite.spritecollide(player,enemy2_bullets,False):
                    player.collide(enemy2_bullets)
                    enemy2_bullets.remove(bullet)
            #pude usar las listas de la clase todo este tiempo...
            #cura a player cuando choca con un sprite de vida
            for healt_pot in current_room.hp_list:
                if pygame.sprite.spritecollide(player,current_room.hp_list,False):
                    current_room.hp_list.remove(healt_pot)
                    player.hit_points += 25

            for enemy in current_room.enemy_list: # para ver si choque con enemigo
                if pygame.sprite.spritecollide(player,current_room.enemy_list,False):
                        player.enemy_collide(current_room.enemy_list)






                        
        #Logica del segundo cuarto        
        elif current_room_no == 1:
            enemy3_bullet_timer +=1
            enemy4_bullet_timer +=1
            if enemy3_bullet_timer == 80 and enemy3_alive == True:
                enemy_bullet3 = Enemy_bullet(fireball2,50,50) #creacion y posicion del disparo
                enemy_bullet3.rect.x = enemy3.rect.x
                enemy_bullet3.rect.y = enemy3.rect.y
                enemy3_bullets.add(enemy_bullet3)
                enemy3_bullet_timer = 0
            enemy3_bullets.update()

            if enemy4_bullet_timer == 60 and enemy4_alive == True:
                enemy_bullet4 = Enemy_bullet(fireball2,50,50) #creacion y posicion del disparo
                enemy_bullet4.rect.x = enemy4.rect.x
                enemy_bullet4.rect.y = enemy4.rect.y
                enemy4_bullets.add(enemy_bullet4)
                enemy4_bullet_timer = 0
            enemy4_bullets.update()

            
            for bullet in player_bullets:#por cada bala en lista de balas de jugador
                wall_hit_list = pygame.sprite.spritecollide(bullet,current_room.wall_list,False) #verificar si choco con una pared
                enemy_list = pygame.sprite.spritecollide(bullet,current_room.enemy_list,False)
                for block in wall_hit_list:
                    player_bullets.remove(bullet) #si choca con pared, eliminar bala

                for enemy in enemy_list:
                    player_bullets.remove(bullet)

                if pygame.sprite.spritecollide(bullet,current_room.enemy1_sprites,False): #bala choca con enemigo, esto SI elimina enemigo
                    enemy3.hit_points -= 25
                    if enemy3.hit_points <= 0:
                        if pygame.sprite.spritecollide(bullet,current_room.enemy1_sprites,True):
                            enemy3_alive = False
                            
                if pygame.sprite.spritecollide(bullet,current_room.enemy2_sprites,False): #bala choca con enemigo, esto SI elimina enemigo
                    enemy4.hit_points -= 25
                    if enemy4.hit_points <= 0:
                        if pygame.sprite.spritecollide(bullet,current_room.enemy2_sprites,True):
                            enemy4_alive = False
            
                    if bullet.rect.x > 800:
                        player_bullets.remove(bullet)


            for healt_pot in current_room.hp_list:#health pot
                if pygame.sprite.spritecollide(player,current_room.hp_list,False):
                    current_room.hp_list.remove(healt_pot)
                    player.hit_points += 25

            for enemy in current_room.enemy_list: # para ver si choque con enemigo
                if pygame.sprite.spritecollide(player,current_room.enemy_list,False):
                        player.enemy_collide(current_room.enemy_list)

            for fire_rate in current_room.rate_of_fire_list:
                if pygame.sprite.spritecollide(player,current_room.rate_of_fire_list,False):
                    current_room.rate_of_fire_list.remove(fire_rate)
                    fire_rate = True

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
                    







                        
         
        if player.rect.x > 801:
            if current_room_no == 0:
                enemy1_bullets.empty()
                enemy2_bullets.empty()
                current_room_no = 1
                current_room = rooms[current_room_no]
                player.rect.x = 50
                player.rect.y = 250
            elif current_room_no == 1:
                current_room_no = 2
                current_room = rooms[current_room_no]
                player.rect.x = 0
            else:
                current_room_no = 0
                current_room = rooms[current_room_no]
                player.rect.x = 0
        if player.rect.x < 0 and current_room_no ==1:
            current_room_no = 0
            current_room = rooms[current_room_no]
            player.rect.x = 790
         
        # --- Drawing ---
        screen.fill(BLACK)
        screen.blit(background,[0,0])
        text_HP = font.render("HitPoints: "+ str(player.hit_points),True,GREEN)
        player_sprite.draw(screen)
        current_room.wall_list.draw(screen)
        current_room.enemy1_sprites.draw(screen)
        current_room.enemy2_sprites.draw(screen)
        current_room.enemy3_sprites.draw(screen)
        current_room.hp_list.draw(screen)
        current_room.rate_of_fire_list.draw(screen)
        #current_room.enemy_list.draw(screen)
        player_bullets.draw(screen)
        enemy1_bullets.draw(screen)
        enemy2_bullets.draw(screen)
        enemy3_bullets.draw(screen)
        enemy4_bullets.draw(screen)
        screen.blit(text_HP, [0, 0])
        if player.hit_points <= 0:
            player_sprite.remove(player)
            screen.blit(text_GAME_OVER,[150,250])
            
            
    
        
        
 
        pygame.display.flip()
 
        clock.tick(60)
 
    pygame.quit()
 

main()  
