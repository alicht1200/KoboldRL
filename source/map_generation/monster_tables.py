from source.entity import Entity
import source.map_generation.entity_factories as entity_list
from numpy import random as np_random

def sewer_water_table_1() -> Entity:
    return np_random.choice(
    a=[entity_list.slime, entity_list.crocodile],
    p=[0.8, 0.2]
    )

def sewer_sidewalk_table_1() -> Entity:
    return np_random.choice(
    a=[entity_list.rat, entity_list.goblin_patrol, entity_list.gnome, entity_list.wererat],
    p=[0.45, 0.35, 0.1, 0.1,]
    )

def sewer_room_table1() -> Entity:
    return np_random.choice(
    a=[entity_list.rat, entity_list.goblin_patrol, entity_list.gnome, entity_list.wererat, entity_list.rogue],
    p=[0.3, 0.2, 0.1, 0.1, 0.3,]
    )

def sewer_thief_hideout_table1() -> Entity:
    return np_random.choice(
    a=[entity_list.rogue, entity_list.dog],
    p=[0.8, 0.2]
    )