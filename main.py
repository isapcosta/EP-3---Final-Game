<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 00:02:08 2017

@author: isadora
"""

import pygame as pg
import time
import random
from os import path
import sys
from settings import *
from sprites import *

from tilemap import*
import pytmx
from pytmx import load_pygame

def draw_player_health(surf,x,y,pct):

    if pct<0:
        pct=0
    BAR_LENGTH=100
    BAR_HEIGHT=20
    fill=pct*BAR_LENGTH
    outline_rect=pg.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect=pg.Rect(x,y,fill,BAR_HEIGHT)
    if pct > 0.6:
        col=GREEN
    elif pct> 0.3:
        col=YELLOW
    else:
        col=RED
    pg.draw.rect(surf,col,fill_rect)
    pg.draw.rect(surf,WHITE,outline_rect,2)
    
class Game:
    def __init__(self):
        #initialize game window
        pg.font.init()
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock=pg.time.Clock()
        pg.key.set_repeat(500,100)
        self.load_data()
        
    def draw_text(self,text,font_name,size,color,x,y,align="nw"):
        font=pg.font.Font(font_name,size)
        text_surface=font.render(text,True,color)
        text_rect=text_surface.get_rect()
        if align=="nw":
            text_rect.topleft=(x,y)
        if align=="ne":
            text_rect.topright=(x,y)
        if align=="sw":
            text_rect.bottomleft=(x,y)
        if align=="se":
            text_rect.bottomright=(x,y)
        if align=="n":
            text_rect.midtop=(x,y)
        if align=="s":
            text_rect.midbottom=(x,y)
        if align=="e":
            text_rect.midright=(x,y)
        if align=="w":
            text_rect.midleft=(x,y)
        if align=="center":
            text_rect.center=(x,y)
        self.screen.blit(text_surface,text_rect)
        
    def load_data(self):
        game_folder=path.dirname(__file__)
        img_folder=path.join(game_folder,'img')
        self.map_folder=path.join(game_folder,'maps')
        music_folder=path.join(game_folder,'music')
        self.font=path.join(img_folder,"SEASRN__.ttf")
        self.hud_font=path.join(img_folder,"SEASRN__.ttf")
        self.dim_screen=pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0,180))
        
        self.player_img=pg.image.load(path.join(img_folder,PLAYER_IMG)).convert_alpha()
        self.player_img=pg.transform.scale(self.player_img,(80,80))
        self.mob_img=pg.image.load(path.join(img_folder,MOB_IMG)).convert_alpha()
        self.wall_img=pg.image.load(path.join(img_folder,WALL_IMG)).convert_alpha()
        self.wall_img=pg.transform.scale(self.wall_img,(TILESIZE,TILESIZE))
        self.bullet_img=pg.image.load(path.join(img_folder,BULLET_IMG)).convert_alpha()
        self.splat=pg.image.load(path.join(img_folder,SPLAT)).convert_alpha()
        self.splat=pg.transform.scale(self.splat,(64,64))
        self.gun_flashes=[]
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder,img)).convert_alpha())
        self.item_images={}
        for item in ITEM_IMAGES:
            self.item_images[item]=pg.image.load(path.join(img_folder,ITEM_IMAGES[item])).convert_alpha()
        self.fog=pg.Surface((WIDTH,HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask=pg.image.load(path.join(img_folder,LIGHT_MASK)).convert_alpha()
        self.light_mask=pg.transform.scale(self.light_mask,LIGHT_RADIUS)
        self.light_rect=self.light_mask.get_rect()
        
        
        pg.mixer.music.load(path.join(music_folder,BG_MUSIC))
        self.effects_sounds={}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type]=pg.mixer.Sound(path.join(music_folder,EFFECTS_SOUNDS[type]))
        self.weapon_sounds={}
        self.weapon_sounds['gun']=[]
        for music in WEAPON_SOUNDS_GUN:
            self.weapon_sounds['gun'].append(pg.mixer.Sound(path.join(music_folder,music)))
        self.zombie_moan_sounds=[]
        for snd in ZOMBIE_MOAN_SOUNDS:
            s=pg.mixer.Sound(path.join(music_folder,snd))
            s.set_volume(0.8)
            self.zombie_moan_sounds.append(s)
       
        self.player_hit_sounds=[]
        for music in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(music_folder,music)))
        self.zombie_hit_sounds=[]
        for snd in ZOMBIE_HIT_SOUNDS:
            s=pg.mixer.Sound(path.join(music_folder,snd))
            self.zombie_hit_sounds.append(s)
        self.heart_sounds=[]
        for snd in HEART_SOUNDS:
            s=pg.mixer.Sound(path.join(music_folder,snd))
            self.heart_sounds.append(s)
   
    def new (self):
        #start a new self.player_img=pg.image.load(path.join(img_folder,PLAYER_IMG)).convert_alpha()game
        self.all_sprites=pg.sprite.LayeredUpdates()
        self.walls=pg.sprite.Group()
        self.mobs=pg.sprite.Group()
        self.bullets=pg.sprite.Group()
        self.items=pg.sprite.Group()
        self.map=TiledMap(path.join(self.map_folder,'level1.tmx'))
        self.map_img=self.map.make_map()
        self.map_rect=self.map_img.get_rect()
        
        
       # for row,tiles in enumerate(self.map.data):
        #    for col,tile in enumerate(tiles):
         #       if tile=='1':
          #          Wall(self,col,row)
           #     if tile=='M':
            #        Mob(self,col,row)
             #   if tile=='P':
             #       self.player=Player(self,col,row)
        for tile_object in self.map.tmxdata.objects:
            obj_center=vec(tile_object.x+tile_object.width/2,tile_object.y+tile_object.height/2)
            if tile_object.name=='player':
                self.player=Player(self,obj_center.x,obj_center.y)
            if tile_object.name=='zombie':
                Mob(self,obj_center.x,obj_center.y)
            if tile_object.name=='wall':
                Obstacle(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height)
            if tile_object.name in ['health']:
               Item(self,obj_center,tile_object.name)
        
        self.camera=Camera(self.map.width,self.map.height)
        self.draw_debug=False
        self.paused=False
        self.night=False
        self.effects_sounds['level_start'].play()
    def button(self,msg,x,y,w,h,ic,ac,action=None):
        self.mouse=pg.mouse.get_pos()
        self.click=pg.mouse.get_pressed()
        
        if x+w>self.mouse[0]>x and y+h>self.mouse[1]>y:
            pg.draw.rect(self.screen,ac,(x,y,w,h))
            if self.click[0]==1 and action !=None:
                if action=="play":
                    g.new()
                    g.run()
                elif action=="pass":
                    g.start_screen()
                elif action=="menu":
                    g.menu()
                elif action=="quit":
                    self.quit()
                    
        else:
            pg.draw.rect(self.screen,ic,(x,y,w,h))
        self.draw_text(msg,self.font,20,BLACK,x+(w/2),y+(h/2),align="center")
    def menu(self):
        self.intro=True
        while self.intro:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    self.quit()
            #self.screen.fill(WHITE)
            self.background_filename = 'imagemfundo.jpg'
            self.background = pg.image.load(self.background_filename).convert() 
            self.screen.blit(self.background,[0,0])
            self.draw_text("Tech attack",self.font,90,GREEN,WIDTH/2,HEIGHT/5,align="center")
            
            self.button("viver",200,400,100,50,RED,BRIGHT_RED,"pass")
            
            self.button("partir",200,550,100,50,BLUE,BRIGHT_BLUE,"quit")
            
            pg.display.update()
            
            
            
            
        
    def run(self):
        #Game loop
        self.playing=True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt=self.clock.tick(FPS)/1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()
            
    def quit(self):
        pg.quit()
        sys.exit()
                 
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        if len(self.mobs)==0:
            self.playing=False
            g.show_go_screen()
        hits=pg.sprite.spritecollide(self.player,self.items,False)
        for hit in hits:
            if hit.type=="health" and self.player.health<PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
        
        hits=pg.sprite.spritecollide(self.player,self.mobs,False,collide_hit_rect)
        for hit in hits:
            if random () <0.7:
                choice(self.player_hit_sounds).play()
            self.player.health-=MOB_DAMAGE
            hit.vel=vec(0,0)
            if self.player.health<=0:
                self.playing=False
                g.show_go_screen()
        if hits:
            self.player.pos+=vec(MOB_KNOCKBACK,0).rotate(-hits[0].rot)
        hits=pg.sprite.groupcollide(self.mobs,self.bullets,False,True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel=vec(0,0)
        
    def draw_grid(self):
        for x in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen,LIGHTGREY,(x,0),(x,HEIGHT))
        for y in range(0,HEIGHT,TILESIZE):
            pg.draw.line(self.screen,LIGHTGREY,(0,y),(WIDTH,y))
    def render_fog(self):
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center=self.camera.apply(self.player).center
        self.fog.blit(self.light_mask,self.light_rect)
        self.screen.blit(self.fog,(0,0),special_flags=pg.BLEND_MULT)
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img,self.camera.apply_rect(self.map_rect))
       # self.draw_grid()
        for sprite in self.all_sprites:
            
            if isinstance(sprite,Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image,self.camera.apply(sprite))
        #pg.draw.rect(self.screen,WHITE,self.player.hit_rect,2)
            if self.draw_debug:
                pg.draw.rect(self.screen,YELLOW,self.camera.apply_rect(sprite.hit_rect),1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen,YELLOW,self.camera.apply_rect(wall.rect),1)
        
        if self.night:
            self.render_fog()
        draw_player_health(self.screen,WIDTH-120,60,self.player.health/PLAYER_HEALTH)
        #draw_player_food(self.screen,10,10,self.player.health/PLAYER_HEALTH)
        self.draw_text('techs:{}'.format(len(self.mobs)),self.hud_font,30,WHITE,WIDTH-10,10,align="ne")
        self.paper='papel.png'
        self.paper1 = pg.image.load(self.paper).convert()
        self.paper1=pg.transform.scale(self.paper1,(200,250))
        self.screen.blit(self.paper1,[10,10])
        self.draw_text('space- attack'.format(len(self.mobs)),self.hud_font,20,BLACK,110,50,align="center")
        self.draw_text('N- Night'.format(len(self.mobs)),self.hud_font,20,BLACK,100,100,align="center")
        self.draw_text('P- Pause'.format(len(self.mobs)),self.hud_font,20,BLACK,100,150,align="center")
        self.draw_text('M- Menu'.format(len(self.mobs)),self.hud_font,20,BLACK,100,200,align="center")
        if self.paused:
            self.screen.blit(self.dim_screen,(0,0))
            self.draw_text("Estagnado",self.font,105,RED,WIDTH/2,HEIGHT/2,align="center")
            
        pg.display.flip()     
        
        
        
    def events(self):
        for event in pg.event.get():
            if event.type==pg.QUIT:
                self.quit()
                
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_ESCAPE:
                    self.quit()
        
                if event.key==pg.K_h:
                    self.draw_debug=not self.draw_debug
                if event.key==pg.K_p:
                    self.paused=not self.paused
                if event.key==pg.K_n:
                    self.night=not self.night
                if event.key==pg.K_m:
                    self.playing=False
                    g.menu()
    def start_screen(self):
        self.story_game = 'papel.png'
        self.story = pg.image.load(self.story_game).convert() 
        self.story = pg.transform.scale(self.story,(WIDTH,HEIGHT))
        self.screen.blit(self.story,[0,0])
        self.draw_text("''AO ACORDAR UM DIA, PERCEBEU QUE ESTAVA SOZINHO ",self.font,30,BLACK,WIDTH/2,150,align="center")
        self.draw_text("E TODOS OS ELETRÔNICOS TINHAM GANHADO ",self.font,30,BLACK,WIDTH/2,200,align="center")
        self.draw_text("VIDA PRÓPRIA e estavam atacando. Então",self.font,30,BLACK,WIDTH/2,250,align="center")
        self.draw_text("SE AUSENTOU NO CAMPO, LONGE DA tecnologia",self.font,30,BLACK,WIDTH/2,300,align="center")
        self.draw_text("Mas ainda restavam 'techs' ",self.font,30,BLACK,WIDTH/2,350,align="center")
        self.draw_text("o objetivo é sobreviver e derrotar todas as 'techs'",self.font,30,BLACK,WIDTH/2,400,align="center")
        self.draw_text("para que as pessoas aparecam novamente.'' ",self.font,30,BLACK,WIDTH/2,450,align="center")
        self.draw_text("Conte com o seu DIario de bordo e relógio.",self.font,30,BLACK,WIDTH/2,550,align="center")
        start=True
        while start:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    start=False
                    self.quit()
            self.button("Próximo",450,650,150,50,GREEN,BRIGHT_GREEN,"play")   
            pg.display.update()
            pg.display.flip()
        
    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER",self.font,100,RED,WIDTH/2,HEIGHT/4,align="center")
        self.draw_text("Aperte espaco para voltar para o menu",self.font,40,WHITE,WIDTH/2,HEIGHT/2,align="center")
        pg.display.flip()
        self.wait_for_key()
    def wait_for_key(self):
        waiting=True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    waiting=False
                    self.quit()
                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_SPACE:
                        waiting=False
                        g.menu()
g=Game()    
while True:
   g.menu()
pg.quit
=======
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 00:02:08 2017

@author: isadora
"""

import pygame as pg
import time
import random
from os import path
import sys
from settings import *
from sprites import *

from tilemap import*
import pytmx
from pytmx import load_pygame

def draw_player_health(surf,x,y,pct):

    if pct<0:
        pct=0
    BAR_LENGTH=100
    BAR_HEIGHT=20
    fill=pct*BAR_LENGTH
    outline_rect=pg.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect=pg.Rect(x,y,fill,BAR_HEIGHT)
    if pct > 0.6:
        col=GREEN
    elif pct> 0.3:
        col=YELLOW
    else:
        col=RED
    pg.draw.rect(surf,col,fill_rect)
    pg.draw.rect(surf,WHITE,outline_rect,2)
    
class Game:
    def __init__(self):
        #initialize game window
        pg.font.init()
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock=pg.time.Clock()
        pg.key.set_repeat(500,100)
        self.load_data()
        
    def draw_text(self,text,font_name,size,color,x,y,align="nw"):
        font=pg.font.Font(font_name,size)
        text_surface=font.render(text,True,color)
        text_rect=text_surface.get_rect()
        if align=="nw":
            text_rect.topleft=(x,y)
        if align=="ne":
            text_rect.topright=(x,y)
        if align=="sw":
            text_rect.bottomleft=(x,y)
        if align=="se":
            text_rect.bottomright=(x,y)
        if align=="n":
            text_rect.midtop=(x,y)
        if align=="s":
            text_rect.midbottom=(x,y)
        if align=="e":
            text_rect.midright=(x,y)
        if align=="w":
            text_rect.midleft=(x,y)
        if align=="center":
            text_rect.center=(x,y)
        self.screen.blit(text_surface,text_rect)
        
    def load_data(self):
        game_folder=path.dirname(__file__)
        img_folder=path.join(game_folder,'img')
        self.map_folder=path.join(game_folder,'maps')
        music_folder=path.join(game_folder,'music')
        self.font=path.join(img_folder,"SEASRN__.ttf")
        self.hud_font=path.join(img_folder,"SEASRN__.ttf")
        self.dim_screen=pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0,180))
        
        self.player_img=pg.image.load(path.join(img_folder,PLAYER_IMG)).convert_alpha()
        self.player_img=pg.transform.scale(self.player_img,(80,80))
        self.mob_img=pg.image.load(path.join(img_folder,MOB_IMG)).convert_alpha()
        self.wall_img=pg.image.load(path.join(img_folder,WALL_IMG)).convert_alpha()
        self.wall_img=pg.transform.scale(self.wall_img,(TILESIZE,TILESIZE))
        self.bullet_img=pg.image.load(path.join(img_folder,BULLET_IMG)).convert_alpha()
        self.splat=pg.image.load(path.join(img_folder,SPLAT)).convert_alpha()
        self.splat=pg.transform.scale(self.splat,(64,64))
        self.gun_flashes=[]
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder,img)).convert_alpha())
        self.item_images={}
        for item in ITEM_IMAGES:
            self.item_images[item]=pg.image.load(path.join(img_folder,ITEM_IMAGES[item])).convert_alpha()
        self.fog=pg.Surface((WIDTH,HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask=pg.image.load(path.join(img_folder,LIGHT_MASK)).convert_alpha()
        self.light_mask=pg.transform.scale(self.light_mask,LIGHT_RADIUS)
        self.light_rect=self.light_mask.get_rect()
        
        
        pg.mixer.music.load(path.join(music_folder,BG_MUSIC))
        self.effects_sounds={}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type]=pg.mixer.Sound(path.join(music_folder,EFFECTS_SOUNDS[type]))
        self.weapon_sounds={}
        self.weapon_sounds['gun']=[]
        for music in WEAPON_SOUNDS_GUN:
            self.weapon_sounds['gun'].append(pg.mixer.Sound(path.join(music_folder,music)))
        self.zombie_moan_sounds=[]
        for snd in ZOMBIE_MOAN_SOUNDS:
            s=pg.mixer.Sound(path.join(music_folder,snd))
            s.set_volume(0.8)
            self.zombie_moan_sounds.append(s)
       
        self.player_hit_sounds=[]
        for music in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(music_folder,music)))
        self.zombie_hit_sounds=[]
        for snd in ZOMBIE_HIT_SOUNDS:
            s=pg.mixer.Sound(path.join(music_folder,snd))
            self.zombie_hit_sounds.append(s)
        self.heart_sounds=[]
        for snd in HEART_SOUNDS:
            s=pg.mixer.Sound(path.join(music_folder,snd))
            self.heart_sounds.append(s)
   
    def new (self):
        #start a new self.player_img=pg.image.load(path.join(img_folder,PLAYER_IMG)).convert_alpha()game
        self.all_sprites=pg.sprite.LayeredUpdates()
        self.walls=pg.sprite.Group()
        self.mobs=pg.sprite.Group()
        self.bullets=pg.sprite.Group()
        self.items=pg.sprite.Group()
        self.map=TiledMap(path.join(self.map_folder,'level1.tmx'))
        self.map_img=self.map.make_map()
        self.map_rect=self.map_img.get_rect()
        
        
       # for row,tiles in enumerate(self.map.data):
        #    for col,tile in enumerate(tiles):
         #       if tile=='1':
          #          Wall(self,col,row)
           #     if tile=='M':
            #        Mob(self,col,row)
             #   if tile=='P':
             #       self.player=Player(self,col,row)
        for tile_object in self.map.tmxdata.objects:
            obj_center=vec(tile_object.x+tile_object.width/2,tile_object.y+tile_object.height/2)
            if tile_object.name=='player':
                self.player=Player(self,obj_center.x,obj_center.y)
            if tile_object.name=='zombie':
                Mob(self,obj_center.x,obj_center.y)
            if tile_object.name=='wall':
                Obstacle(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height)
            if tile_object.name in ['health']:
               Item(self,obj_center,tile_object.name)
        
        self.camera=Camera(self.map.width,self.map.height)
        self.draw_debug=False
        self.paused=False
        self.night=False
        self.effects_sounds['level_start'].play()
    def button(self,msg,x,y,w,h,ic,ac,action=None):
        self.mouse=pg.mouse.get_pos()
        self.click=pg.mouse.get_pressed()
        
        if x+w>self.mouse[0]>x and y+h>self.mouse[1]>y:
            pg.draw.rect(self.screen,ac,(x,y,w,h))
            if self.click[0]==1 and action !=None:
                if action=="play":
                    g.new()
                    g.run()
                elif action=="pass":
                    g.start_screen()
                elif action=="menu":
                    g.menu()
                elif action=="quit":
                    self.quit()
                    
        else:
            pg.draw.rect(self.screen,ic,(x,y,w,h))
        self.draw_text(msg,self.font,20,BLACK,x+(w/2),y+(h/2),align="center")
    def menu(self):
        self.intro=True
        while self.intro:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    self.quit()
            #self.screen.fill(WHITE)
            self.background_filename = 'imagemfundo.jpg'
            self.background = pg.image.load(self.background_filename).convert() 
            self.screen.blit(self.background,[0,0])
            self.draw_text("Tech attack",self.font,90,GREEN,WIDTH/2,HEIGHT/5,align="center")
            
            self.button("viver",200,400,100,50,RED,BRIGHT_RED,"pass")
            
            self.button("partir",200,550,100,50,BLUE,BRIGHT_BLUE,"quit")
            
            pg.display.update()
            
            
            
            
        
    def run(self):
        #Game loop
        self.playing=True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt=self.clock.tick(FPS)/1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()
            
    def quit(self):
        pg.quit()
        sys.exit()
                 
    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        if len(self.mobs)==0:
            self.playing=False
            g.show_go_screen()
        hits=pg.sprite.spritecollide(self.player,self.items,False)
        for hit in hits:
            if hit.type=="health" and self.player.health<PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
        
        hits=pg.sprite.spritecollide(self.player,self.mobs,False,collide_hit_rect)
        for hit in hits:
            if random () <0.7:
                choice(self.player_hit_sounds).play()
            self.player.health-=MOB_DAMAGE
            hit.vel=vec(0,0)
            if self.player.health<=0:
                self.playing=False
                g.show_go_screen()
        if hits:
            self.player.pos+=vec(MOB_KNOCKBACK,0).rotate(-hits[0].rot)
        hits=pg.sprite.groupcollide(self.mobs,self.bullets,False,True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel=vec(0,0)
        
    def draw_grid(self):
        for x in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen,LIGHTGREY,(x,0),(x,HEIGHT))
        for y in range(0,HEIGHT,TILESIZE):
            pg.draw.line(self.screen,LIGHTGREY,(0,y),(WIDTH,y))
    def render_fog(self):
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center=self.camera.apply(self.player).center
        self.fog.blit(self.light_mask,self.light_rect)
        self.screen.blit(self.fog,(0,0),special_flags=pg.BLEND_MULT)
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img,self.camera.apply_rect(self.map_rect))
       # self.draw_grid()
        for sprite in self.all_sprites:
            
            if isinstance(sprite,Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image,self.camera.apply(sprite))
        #pg.draw.rect(self.screen,WHITE,self.player.hit_rect,2)
            if self.draw_debug:
                pg.draw.rect(self.screen,YELLOW,self.camera.apply_rect(sprite.hit_rect),1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen,YELLOW,self.camera.apply_rect(wall.rect),1)
        
        if self.night:
            self.render_fog()
        draw_player_health(self.screen,WIDTH-120,60,self.player.health/PLAYER_HEALTH)
        #draw_player_food(self.screen,10,10,self.player.health/PLAYER_HEALTH)
        self.draw_text('techs:{}'.format(len(self.mobs)),self.hud_font,30,WHITE,WIDTH-10,10,align="ne")
        self.paper='papel.png'
        self.paper1 = pg.image.load(self.paper).convert()
        self.paper1=pg.transform.scale(self.paper1,(200,250))
        self.screen.blit(self.paper1,[10,10])
        self.draw_text('space- attack'.format(len(self.mobs)),self.hud_font,20,BLACK,110,50,align="center")
        self.draw_text('N- Night'.format(len(self.mobs)),self.hud_font,20,BLACK,100,100,align="center")
        self.draw_text('P- Pause'.format(len(self.mobs)),self.hud_font,20,BLACK,100,150,align="center")
        self.draw_text('M- Menu'.format(len(self.mobs)),self.hud_font,20,BLACK,100,200,align="center")
        if self.paused:
            self.screen.blit(self.dim_screen,(0,0))
            self.draw_text("Estagnado",self.font,105,RED,WIDTH/2,HEIGHT/2,align="center")
            
        pg.display.flip()     
        
        
        
    def events(self):
        for event in pg.event.get():
            if event.type==pg.QUIT:
                self.quit()
                
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_ESCAPE:
                    self.quit()
        
                if event.key==pg.K_h:
                    self.draw_debug=not self.draw_debug
                if event.key==pg.K_p:
                    self.paused=not self.paused
                if event.key==pg.K_n:
                    self.night=not self.night
                if event.key==pg.K_m:
                    self.playing=False
                    g.menu()
    def start_screen(self):
        self.story_game = 'papel.png'
        self.story = pg.image.load(self.story_game).convert() 
        self.story = pg.transform.scale(self.story,(WIDTH,HEIGHT))
        self.screen.blit(self.story,[0,0])
        self.draw_text("''AO ACORDAR UM DIA, PERCEBEU QUE ESTAVA SOZINHO ",self.font,30,BLACK,WIDTH/2,150,align="center")
        self.draw_text("E TODOS OS ELETRÔNICOS TINHAM GANHADO ",self.font,30,BLACK,WIDTH/2,200,align="center")
        self.draw_text("VIDA PRÓPRIA e estavam atacando. Então",self.font,30,BLACK,WIDTH/2,250,align="center")
        self.draw_text("SE AUSENTOU NO CAMPO, LONGE DA tecnologia",self.font,30,BLACK,WIDTH/2,300,align="center")
        self.draw_text("Mas ainda restavam 'techs' ",self.font,30,BLACK,WIDTH/2,350,align="center")
        self.draw_text("o objetivo é sobreviver e derrotar todas as 'techs'",self.font,30,BLACK,WIDTH/2,400,align="center")
        self.draw_text("para que as pessoas aparecam novamente.'' ",self.font,30,BLACK,WIDTH/2,450,align="center")
        self.draw_text("Conte com o seu DIario de bordo e relógio.",self.font,30,BLACK,WIDTH/2,550,align="center")
        start=True
        while start:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    start=False
                    self.quit()
            self.button("Próximo",450,650,150,50,GREEN,BRIGHT_GREEN,"play")   
            pg.display.update()
            pg.display.flip()
        
    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER",self.font,100,RED,WIDTH/2,HEIGHT/4,align="center")
        self.draw_text("Aperte espaco para voltar para o menu",self.font,40,WHITE,WIDTH/2,HEIGHT/2,align="center")
        pg.display.flip()
        self.wait_for_key()
    def wait_for_key(self):
        waiting=True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    waiting=False
                    self.quit()
                if event.type==pg.KEYDOWN:
                    if event.key==pg.K_SPACE:
                        waiting=False
                        g.menu()
g=Game()    
while True:
   g.menu()
pg.quit
>>>>>>> e4dcbda79627f75731d7389c664a1ab5f7af958f
