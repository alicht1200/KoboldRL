from source.components.ai import HostileEnemy
from source.components.fighter import Fighter
from source.entity import Actor

"""
Color library
"""
color_white = (255,255,255)
color_dark_gray =  (60, 80, 85)

"""
Player Character
"""
player = Actor(
    char='@',
    color=color_white,
    walks=True,
    name='Kobold',
    ai_cls= HostileEnemy,
    fighter=Fighter(hp=30, dodge= 15, resistance=0, accuracy=1, damage=(1,4))
)



"""
Monsters and Enemies
"""

rat = Actor(
    char='r',
    color=color_dark_gray,
    walks=True,
    name='Rat',
    ai_cls= HostileEnemy,
    fighter=Fighter(hp=4, dodge= 8, resistance=0, accuracy=0, damage=(1,3))
)

wererat = Actor(
    char='W',
    color=color_dark_gray,
    walks=True,
    name='Wererat',
    ai_cls= HostileEnemy,
    fighter=Fighter(hp=16, dodge= 10, resistance=1, accuracy=5, damage=(2,12))
)

slime = Actor(
    char='s',
    color=(163,255,106),
    swims=True,
    walks=True,
    name='Slime',
    ai_cls = HostileEnemy,
    fighter = Fighter(hp=4, dodge=5, resistance=2, accuracy=0, damage=(1, 3))
)

crocodile = Actor(
    char='C',
    color=(50,69,5),
    swims=True,
    name='Crocodile',
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=20, dodge=6, resistance=2, accuracy=5, damage=(1, 8))
)

goblin_patrol = Actor(
    char='g',
    color=(200, 150, 30),
    walks=True,
    name='Goblin patrol',
    ai_cls = HostileEnemy,
    fighter = Fighter(hp=6, dodge=10, resistance=1, accuracy=1, damage=(1, 6))
)

gnome = Actor(
    char='g',
    color=(150,128,255),
    walks=True,
    name='Gnome',
    ai_cls = HostileEnemy,
    fighter = Fighter(hp=6, dodge=17, resistance=0, accuracy=0, damage=(1, 2))
)

rogue = Actor(
    char='t',
    color=(30, 80, 160),
    walks=True,
    name='Rogue',
    ai_cls = HostileEnemy,
    fighter = Fighter(hp=6, dodge=12, resistance=0, accuracy=2, damage=(1, 6))
)

dog = Actor(
    char='d',
    color=(130,130,100),
    walks=True,
    name='Dog',
    ai_cls = HostileEnemy,
    fighter = Fighter(hp=6, dodge=14, resistance=0, accuracy=2, damage=(1, 4))
)
