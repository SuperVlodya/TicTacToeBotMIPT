#!/usr/bin/env python
# coding: utf-8

# In[52]:


import random

def drawBoard(board):
    #Эта функция рисует игровую доску с выполненными ходами

     #"Доска" является списком из 10 строк которые рисуют доску в 
#символьной графике
    print(' | |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print(' | |')
    print('---+---+---')
    print(' | |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print(' | |')
    print('---+---+---')
    print(' | |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print(' | |')

def inputPlayerLetter():
     #Позволяет игроку выбрать символ, которым он хочет играть
     #Возвращает список с буквой игрока в качестве первого элемента и 
#буквой компьютера в качестве второго элемента
     letter = ''
     while not (letter == 'Х' or letter == 'О'):
        print('Каким знаком вы будете играть? (Х или О)')
        letter = input().upper()

     #Первым элементом возвращаемого списка всегда должен быть знак игрока.
     if letter == 'Х':
        return ['Х', 'О']
     else:
        return ['О', 'Х']

def whoGoesFirst():
     #Случайно определяется, кто будет ходить первым
    if random.randint(0, 1) == 0:
         return 'компьютер'
    else:
         return 'игрок'

def playAgain():
     #Эта функция возвращает True, если игрок хочет сыграть еще раз. 
#Иначе False.
     print('Вы хотите сыграть еще раз? (да или нет)')
     return input().lower().startswith('д')

def makeMove(board, letter, move):
     board[move] = letter

def isWinner(bo, le):
     #Функция учитывает позицию на доске и текщий ход игрока. Возвращает 
#True, если игрок выиграл
     #Мы используем bo вместо доски и le вместо полных имен переменных
     return ((bo[7] == le and bo[8] == le and bo[9] == le) or #Верхняя линия
     (bo[4] == le and bo[5] == le and bo[6] == le) or #Средняя линия
     (bo[1] == le and bo[2] == le and bo[3] == le) or #Нижняя линия
     (bo[7] == le and bo[4] == le and bo[1] == le) or #Левая вертикальная линия
     (bo[8] == le and bo[5] == le and bo[2] == le) or #Центральная вертикаль
     (bo[9] == le and bo[6] == le and bo[3] == le) or #Верхняя линия
     (bo[7] == le and bo[5] == le and bo[3] == le) or #Диагональ
     (bo[9] == le and bo[5] == le and bo[1] == le)) #Диагональ

def getBoardCopy(board):
     #Сделаем копию игровой доски и вернем её
    dupeBoard = []
 
    for i in board:
         dupeBoard.append(i)

    return dupeBoard
 
def isSpaceFree(board, move):
     #Возвращает True если ход возможен
    return board[move] == ' '
 
def getPlayerMove(board):
     #Позволяет игроку выполнить ход
    move = ''
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
         print('Ваш ход (1-9):')
         move = input()
    return int(move)
 
def chooseRandomMoveFromList(board, movesList):
     #Возвращает случайный ход из полученного списка возможных ходов
     #Возвращает None если ходов нет
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)
 
    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None

def getComputerMove(board, computerLetter):
     #Получает копию содержимого доски и букву, которой ходит компьютер. 
#Исходя из этого определяет куда двигаться и возвращает ход
    if computerLetter == 'Х':
         playerLetter = 'О'
    else:
        playerLetter = 'Х'
 
    #Здесь начинается алгоритм ИИ "Крестики-Нолики"
    #Первым шагом будет определение возможности победы на следующем ходу
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, computerLetter, i)
            if isWinner(copy, computerLetter):
                return i

    #Проверяем, может ли игрок выиграть на следющем ходу, чтобы 
#заблокировать его
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, playerLetter, i)
            if isWinner(copy, playerLetter):
                return i
 
     #Попытаемся занять один из углов, если они свободны
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move
 
     #Занимаем центр, если он свободен
    if isSpaceFree(board, 5):
        return 5
 
     #Занимаем одну из боковых клеток
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
     #Возвращаем True, если все клетки на доске были заняты. Иначе 
#возвращаем False
    for i in range(1, 10):
         if isSpaceFree(board, i):
            return False
    return True


# In[ ]:





# In[ ]:




