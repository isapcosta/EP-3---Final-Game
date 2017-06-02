<<<<<<< HEAD
import pygame as pg

vec=pg.math.Vector2
#Cores em geral
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(200,0,0)
BRIGHT_RED=(255,0,0)
GREEN=(0,200,0)
BRIGHT_GREEN=(0,255,0)
BLUE=(0,0,200)
BRIGHT_BLUE=(0,0,255)
YELLOW=(255,255,0)
DARKGREY=(40,40,40)
LIGHTGREY=(100,100,100)
BROWN=(106,55,5)
# Caracteristicas do plano de fundo e mapa
MENU__BG=""
WIDTH = 1024
HEIGHT = 768
FPS=60
TITLE="Survival diary"
#BGCOLOR=BROWN
TILESIZE=64
GRIDWIDTH=WIDTH/TILESIZE
GRIDHEIGHT=HEIGHT/TILESIZE
WALL_IMG="tile_01.png"
#Jogador
PLAYER_HEALTH=100
PLAYER_SPEED=300
PLAYER_ROT_SPEED=250
PLAYER_IMG='teste1.png'
PLAYER_HIT_RECT=pg.Rect(0,0,35,35)
BARREL_OFFSET=vec(30,10)
#Bala, dano, vida e movimento
BULLET_IMG='bullet.png'
BULLET_SPEED=500
BULLET_LIFETIME=1000
BULLET_RATE=150
KICKBACK= 200
GUN_SPREAD=5
BULLET_DAMAGE= 10
MUZZLE_FLASHES=['whitePuff15.png','whitePuff16.png','whitePuff17.png','whitePuff18.png']
SPLAT="fart01.png"
FLASH_DURATION=40
#Inimigo
MOB_IMG='robot1_hold.png'
MOB_SPEEDS=[150,100,75,125]
MOB_HIT_RECT=pg.Rect(0,0,30,30)
MOB_HEALTH=100
MOB_DAMAGE=10
MOB_KNOCKBACK=20
AVOID_RADIUS=50
DETECT_RADIUS=400 #limite para o inimigo te perseguir
#Camadas de progessao
WALL_LAYER=1
PLAYER_LAYER=2
BULLET_LAYER=3
MOB_LAYER=2
EFFECTS_LAYER=4
ITEMS_LAYER=1
#Parte das barrinhas
HEALTH_PACK_AMOUNT=20
#Itens 
ITEM_IMAGES={'health':'medicine.png'} #pretendo fazer comida, plantas venenosas, 
#Musica e sons
BG_MUSIC='birdsongloop16s.ogg'
PLAYER_HIT_SOUNDS=['gruntsound.wav']
ZOMBIE_MOAN_SOUNDS=['brains.wav','groan.wav','creepy_mouth_breathing.wav','rar.wav']
ZOMBIE_HIT_SOUNDS=['thud.wav']
WEAPON_SOUNDS_GUN=['gun1.wav','gun2.wav']
EFFECTS_SOUNDS={'level_start':'levelup.wav','health_up':'levelup.wav'}

NIGHT_COLOR=(20,20,20)
LIGHT_RADIUS=(500,500)
LIGHT_MASK="light_350_med.png"

HEART_SOUNDS=["heart.wav"]



















=======
import pygame as pg

vec=pg.math.Vector2
#Cores em geral
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(200,0,0)
BRIGHT_RED=(255,0,0)
GREEN=(0,200,0)
BRIGHT_GREEN=(0,255,0)
BLUE=(0,0,200)
BRIGHT_BLUE=(0,0,255)
YELLOW=(255,255,0)
DARKGREY=(40,40,40)
LIGHTGREY=(100,100,100)
BROWN=(106,55,5)
# Caracteristicas do plano de fundo e mapa
MENU__BG=""
WIDTH = 1024
HEIGHT = 768
FPS=60
TITLE="Survival diary"
#BGCOLOR=BROWN
TILESIZE=64
GRIDWIDTH=WIDTH/TILESIZE
GRIDHEIGHT=HEIGHT/TILESIZE
WALL_IMG="tile_01.png"
#Jogador
PLAYER_HEALTH=100
PLAYER_SPEED=300
PLAYER_ROT_SPEED=250
PLAYER_IMG='teste1.png'
PLAYER_HIT_RECT=pg.Rect(0,0,35,35)
BARREL_OFFSET=vec(30,10)
#Bala, dano, vida e movimento
BULLET_IMG='bullet.png'
BULLET_SPEED=500
BULLET_LIFETIME=1000
BULLET_RATE=150
KICKBACK= 200
GUN_SPREAD=5
BULLET_DAMAGE= 10
MUZZLE_FLASHES=['whitePuff15.png','whitePuff16.png','whitePuff17.png','whitePuff18.png']
SPLAT="fart01.png"
FLASH_DURATION=40
#Inimigo
MOB_IMG='robot1_hold.png'
MOB_SPEEDS=[150,100,75,125]
MOB_HIT_RECT=pg.Rect(0,0,30,30)
MOB_HEALTH=100
MOB_DAMAGE=10
MOB_KNOCKBACK=20
AVOID_RADIUS=50
DETECT_RADIUS=400 #limite para o inimigo te perseguir
#Camadas de progessao
WALL_LAYER=1
PLAYER_LAYER=2
BULLET_LAYER=3
MOB_LAYER=2
EFFECTS_LAYER=4
ITEMS_LAYER=1
#Parte das barrinhas
HEALTH_PACK_AMOUNT=20
#Itens 
ITEM_IMAGES={'health':'medicine.png'} #pretendo fazer comida, plantas venenosas, 
#Musica e sons
BG_MUSIC='birdsongloop16s.ogg'
PLAYER_HIT_SOUNDS=['gruntsound.wav']
ZOMBIE_MOAN_SOUNDS=['brains.wav','groan.wav','creepy_mouth_breathing.wav','rar.wav']
ZOMBIE_HIT_SOUNDS=['thud.wav']
WEAPON_SOUNDS_GUN=['gun1.wav','gun2.wav']
EFFECTS_SOUNDS={'level_start':'levelup.wav','health_up':'levelup.wav'}

NIGHT_COLOR=(20,20,20)
LIGHT_RADIUS=(500,500)
LIGHT_MASK="light_350_med.png"

HEART_SOUNDS=["heart.wav"]



















>>>>>>> e4dcbda79627f75731d7389c664a1ab5f7af958f
