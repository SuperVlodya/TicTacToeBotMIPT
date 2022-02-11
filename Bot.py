#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import telebot
import ORMForBot as ORM
from telebot import types
import TicTacToeForBot as TicTacToe
bot = telebot.TeleBot('5243687518:AAEYQJGdmCx86OvyIRTzAjDXwN1lM0dgFXU');
nick = ''
winner = 2
theBoard = [' ']*10
playerLetter, computerLetter = ['X', 'O']
@bot.message_handler(content_types=['text'])

def start_bot(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Hello, welcome to Tic-Tac-Toe! Please, enter your nickname.")
        bot.register_next_step_handler(message, nickname)
        
def nickname(message):
    global nick
    nick = message.text
    if ORM.check_name(nick):
        ORM.write_player(nick)
        bot.send_message(message.from_user.id, "Nice to meet you, "+ nick +"!\nTo play, type /play\nTo review your stats, type /stats\nIf you need help, type /help")
        bot.register_next_step_handler(message, start_game)
    else:
        bot.send_message(message.from_user.id, "This nickname is taken, please enter another one")
        bot.register_next_step_handler(message, nickname)
        
def start_game(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, "/play — Play the game of Tic-Tac-Toe,\n/stats — Review your stats,\n/help — Repeats this message")
        bot.register_next_step_handler(message, start_game)
    elif message.text == "/play":
        bot.send_message(message.from_user.id, '‎  ' + theBoard[7] + ' |  ' + theBoard[8] + ' | ' + theBoard[9] + '\n---+---+---\n‎  ' + theBoard[4] + ' |  ' + theBoard[5] + ' | ' + theBoard[6] + '\n---+---+---\n‎  ' + theBoard[1] + ' |  ' + theBoard[2] + ' | ' + theBoard[3])
        bot.send_message(message.from_user.id, "Choose your move\n/topleft   /top   /topright\n/left   /center   /right\n/bottomleft   /bottom   /bottomright")
        bot.register_next_step_handler(message, player_move)
    elif message.text == "/stats":
        stats_set = ORM.get_stats(nick)
        played = str(int(stats_set[1]))
        won = str(int(stats_set[2]))
        drawn = str(int(stats_set[3]))
        lost = str(int(stats_set[4]))
        bot.send_message(message.from_user.id, 'Stats for '+ nick + ':\n\nGames played: ' + played + '\nGames won: ' + won + '\nGames drawn: ' + drawn+ '\nGames lost: ' + lost)
        bot.register_next_step_handler(message, start_game)
    elif message.text == "/start":
        bot.send_message(message.from_user.id, "We've already started talking!")
        bot.register_next_step_handler(message, start_game)
    else:
        bot.send_message(message.from_user.id, "I don't understand you, please type /help.")
        bot.register_next_step_handler(message, start_game)
        
def player_move(message):
    global theBoard
    global move
    move = 0
    valid_move = True
    if message.text == "/bottomleft":
        move = 1
    elif message.text == "/bottom":
        move = 2
    elif message.text == "/bottomright":
        move = 3
    elif message.text == "/left":
        move = 4
    elif message.text == "/center":
        move = 5
    elif message.text == "/right":
        move = 6
    elif message.text == "/topleft":
        move = 7
    elif message.text == "/top":
        move = 8
    elif message.text == "/topright":
        move = 9
    else:
        valid_move = False
        move = 0
    gameIsPlaying = True
    if not TicTacToe.isSpaceFree(theBoard, move) or move == 0:
        valid_move = False
        bot.send_message(message.from_user.id, "That is not a valid move, please try again (you need to complete the game).")
    else:
        TicTacToe.makeMove(theBoard, playerLetter, move)

    if TicTacToe.isWinner(theBoard, playerLetter):
        gameIsPlaying = False
        ORM.update_stats(1, nick)
        bot.send_message(message.from_user.id, '‎  ' + theBoard[7] + ' |  ' + theBoard[8] + ' | ' + theBoard[9] + '\n---+---+---\n‎  ' + theBoard[4] + ' |  ' + theBoard[5] + ' | ' + theBoard[6] + '\n---+---+---\n‎  ' + theBoard[1] + ' |  ' + theBoard[2] + ' | ' + theBoard[3])
        bot.send_message(message.from_user.id, "Congrats, you win! If you want to play again, type /play\nTo review your stats, type /stats")
    else:
        if TicTacToe.isBoardFull(theBoard):
            ORM.update_stats(0, nick)
            gameIsPlaying = False
            bot.send_message(message.from_user.id, '‎  ' + theBoard[7] + ' |  ' + theBoard[8] + ' | ' + theBoard[9] + '\n---+---+---\n‎  ' + theBoard[4] + ' |  ' + theBoard[5] + ' | ' + theBoard[6] + '\n---+---+---\n‎  ' + theBoard[1] + ' |  ' + theBoard[2] + ' | ' + theBoard[3])
            bot.send_message(message.from_user.id, "Draw! If you want to play again, type /play\nTo review your stats, type /stats")
    if valid_move and gameIsPlaying:
        move = TicTacToe.getComputerMove(theBoard, computerLetter)
        TicTacToe.makeMove(theBoard, computerLetter, move)
    
    if TicTacToe.isWinner(theBoard, computerLetter):
        gameIsPlaying = False
        ORM.update_stats(-1, nick)
        bot.send_message(message.from_user.id, '‎  ' + theBoard[7] + ' |  ' + theBoard[8] + ' | ' + theBoard[9] + '\n---+---+---\n‎  ' + theBoard[4] + ' |  ' + theBoard[5] + ' | ' + theBoard[6] + '\n---+---+---\n‎  ' + theBoard[1] + ' |  ' + theBoard[2] + ' | ' + theBoard[3])
        bot.send_message(message.from_user.id, "I win! If you want to play again, type /play\nTo review your stats, type /stats")
    
    if  gameIsPlaying:
        bot.register_next_step_handler(message, player_move)
        bot.send_message(message.from_user.id, '‎  ' + theBoard[7] + ' |  ' + theBoard[8] + ' | ' + theBoard[9] + '\n---+---+---\n‎  ' + theBoard[4] + ' |  ' + theBoard[5] + ' | ' + theBoard[6] + '\n---+---+---\n‎  ' + theBoard[1] + ' |  ' + theBoard[2] + ' | ' + theBoard[3])
    else:
        theBoard = [' ']*10
        move = 0
        bot.register_next_step_handler(message, start_game)
    
bot.polling(none_stop=True, interval=0)


# In[ ]:





# In[ ]:




