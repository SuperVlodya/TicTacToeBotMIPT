import telebot
import ORMForBot as ORM
import TicTacToeForBot as TicTacToe
from telebot import types


bot = telebot.TeleBot('5243687518:AAEYQJGdmCx86OvyIRTzAjDXwN1lM0dgFXU');
nick = ''
winner = 2
the_Board = [' ']*10
player_Letter, computer_Letter = ['X', 'O']
answers = ['/bottomleft', '/bottom', '/bottomright', '/left', '/center', '/right', '/topleft', '/top', '/topright']
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
        bot.send_message(message.from_user.id, f'''
            Nice to meet you, {nick}!
            To play, type /play
            To review your stats, type /stats
            If you need help, type /help
            ''')
        bot.register_next_step_handler(message, start_game)
    else:
        bot.send_message(message.from_user.id, "This nickname is taken, please enter another one")
        bot.register_next_step_handler(message, nickname)
      
    
def start_game(message):
    if message.text == "/help":
        bot.send_message(message.from_user.id, f'''
        /play — Play the game of Tic-Tac-Toe,
        /stats — Review your stats,
        /help — Repeats this message
        ''')
        bot.register_next_step_handler(message, start_game)
    elif message.text == "/play":
        bot.send_message(message.from_user.id, f'''
                ‎  {the_Board[7]} |  {the_Board[8]} | {the_Board[9]}
                ---+---+---
                ‎  {the_Board[4]} |  {the_Board[5]} | {the_Board[6]}
                ---+---+---
                ‎  {the_Board[1]} |  {the_Board[2]} | {the_Board[3]}
                ''')
        bot.send_message(message.from_user.id, '''
            Choose your move
            /topleft   /top   /topright
            /left   /center   /right
            /bottomleft   /bottom   /bottomright
            ''')
        bot.register_next_step_handler(message, player_move)
    elif message.text == "/stats":
        stats_set = ORM.get_stats(nick)
        played = str(int(stats_set[1]))
        won = str(int(stats_set[2]))
        drawn = str(int(stats_set[3]))
        lost = str(int(stats_set[4]))
        bot.send_message(message.from_user.id, f'''
            Stats for {nick}:
            Games played: {played} 
            Games won: {won}
            Games drawn: {drawn}
            Games lost: {lost}
            ''')
        bot.register_next_step_handler(message, start_game)
    elif message.text == "/start":
        bot.send_message(message.from_user.id, "We've already started talking!")
        bot.register_next_step_handler(message, start_game)
    else:
        bot.send_message(message.from_user.id, "I don't understand you, please type /help.")
        bot.register_next_step_handler(message, start_game)
    
    
def player_move(message):
    global the_Board
    global move
    move = 0
    valid_move = True
    for i in range(len(answers)):
        if message.text == answers(i):
            move = i+1
    game_Is_Playing = True
    if not TicTacToe.isSpaceFree(the_Board, move) or move == 0:
        valid_move = False
        bot.send_message(message.from_user.id, "That is not a valid move, please try again (you need to complete the game).")
    else:
        TicTacToe.makeMove(the_Board, player_Letter, move)

    if TicTacToe.isWinner(the_Board, player_Letter):
        game_is_playing = False
        ORM.update_stats(1, nick)
        bot.send_message(message.from_user.id, f'''
            ‎  {the_Board[7]} |  {the_Board[8]} | {the_Board[9]}
            ---+---+---
            ‎  {the_Board[4]} |  {the_Board[5]} | {the_Board[6]}
            ---+---+---
            ‎  {the_Board[1]} |  {the_Board[2]} | {the_Board[3]}
            ''')
        bot.send_message(message.from_user.id, '''
            Congrats, you win! If you want to play again, type /play
            To review your stats, type /stats
            ''')
    else:
        if TicTacToe.isBoardFull(the_Board):
            ORM.update_stats(0, nick)
            game_is_playing = False
            bot.send_message(message.from_user.id, f'''
                ‎  {the_Board[7]} |  {the_Board[8]} | {the_Board[9]}
                ---+---+---
                ‎  {the_Board[4]} |  {the_Board[5]} | {the_Board[6]}
                ---+---+---
                ‎  {the_Board[1]} |  {the_Board[2]} | {the_Board[3]}
                ''')
            bot.send_message(message.from_user.id, f'''
                Draw! If you want to play again, type /play
                To review your stats, type /stats
                ''')
    if valid_move and game_is_playing:
        move = TicTacToe.getComputerMove(the_Board, computer_Letter)
        TicTacToe.makeMove(the_Board, computer_Letter, move)
    
    if TicTacToe.isWinner(the_Board, computer_Letter):
        game_is_playing = False
        ORM.update_stats(-1, nick)
        bot.send_message(message.from_user.id, f'''
                ‎  {the_Board[7]} |  {the_Board[8]} | {the_Board[9]}
                ---+---+---
                ‎  {the_Board[4]} |  {the_Board[5]} | {the_Board[6]}
                ---+---+---
                ‎  {the_Board[1]} |  {the_Board[2]} | {the_Board[3]}
                ''')
        bot.send_message(message.from_user.id, '''
            I win! If you want to play again, type /play
            To review your stats, type /stats
            ''')
    
    if  game_is_playing:
        bot.register_next_step_handler(message, player_move)
        bot.send_message(message.from_user.id, f'''
                ‎  {the_Board[7]} |  {the_Board[8]} | {the_Board[9]}
                ---+---+---
                ‎  {the_Board[4]} |  {the_Board[5]} | {the_Board[6]}
                ---+---+---
                ‎  {the_Board[1]} |  {the_Board[2]} | {the_Board[3]}
                ''')
    else:
        the_Board = [' ']*10
        move = 0
        bot.register_next_step_handler(message, start_game)
    
    
bot.polling(none_stop=True, interval=0)
