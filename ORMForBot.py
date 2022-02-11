#!/usr/bin/env python
# coding: utf-8

# In[82]:


import peewee
from peewee import *

db = SqliteDatabase('TicTacToeDatabase.db')

class Stat(Model):
    name = CharField(unique=True)
    games_played = FloatField()
    games_won = FloatField()
    games_drawn = FloatField()
    games_lost = FloatField()
    
    class Meta:
        database = db
        order_by = 'name'
        db_table = 'stats'

def write_player(nick):    
    with db:
        player = {'name':nick, 'games_played':0, 'games_won':0, 'games_drawn':0, 'games_lost':0}
        Stat.insert(player).execute()
        
def check_name(nick):
    with db:
        unique_name = True
        query = Stat.select(Stat.name)
        for stat in query:
            if stat.name.lower() == nick.lower():
                unique_name = False
                break
        return unique_name
        
def get_stats(nick):
    with db:
        player_stats = Stat.get(Stat.name == nick)
        return [player_stats.name, player_stats.games_played, player_stats.games_won, player_stats.games_drawn, player_stats.games_lost]

def update_stats(result, nick):
    with db:
        player_stats = get_stats(nick)
        if (result == -1) or (result == 0) or (result == 1):
            player_stats[1]+=1.0
        if result == 1:
            player_stats[2]+=1.0
            player_stats[3]+=0.0
            player_stats[4]+=0.0
        elif result == 0:
            player_stats[2]+=0.0
            player_stats[3]+=1.0
            player_stats[4]+=0.0
        elif result == -1:
            player_stats[2]+=0.0
            player_stats[3]+=1.0
            player_stats[4]+=1.0
        query=Stat.update({Stat.games_played:player_stats[1], Stat.games_won:player_stats[2], Stat.games_drawn:player_stats[3], Stat.games_lost:player_stats[4]}).where(Stat.name == nick)
        query.execute()


# In[ ]:




