import tkinter as tk
import model as mod
from random import getrandbits
from random import randint


def start():
    field = []
    attempt = True
    attempt_count = 0
    players = []
    # определение маркера в зависимости от bool-попытки
    marker = lambda x: 'X' if x else '0'
    # определение цвета в зависимости от bool-попытки
    color = lambda x: 'blue' if x else 'green'

    # ход ai
    def ai_move():
        global attempt_count
        global attempt
        attempt_count += 1
        # если бот с интеллектом
        if aq.get():
            row, col = mod.iq_move(field)
        # иначе бот ходит случайно
        else:
            # random ищем пустую ячейку на поле и ставим marker
            while True:
                row = randint(0, 2)
                col = randint(0, 2)
                # если поле свободно, ставим маркер бота
                if field[row][col]['text'] == '':
                    break
        field[row][col]['foreground'] = color(attempt)
        field[row][col]['text'] = marker(attempt)

    # проверяем статус игры победу
    def check_status():
        global attempt_count
        global attempt
        global players
        var_win = mod.check_winner(field)
        if len(var_win):
            r0, c0, r1, c1, r2, c2 = var_win
            field[r0][c0]['background'] = color(not attempt)
            field[r1][c1]['background'] = color(not attempt)
            field[r2][c2]['background'] = color(not attempt)
            lbl_progress['foreground'] = color(attempt)
            lbl_progress['text'] = f'attempt_count {attempt_count} attempt {attempt} '
            lbl_progress['text'] = f'Выиграл {players[attempt]} ({marker(attempt)})'
            attempt_count = 9
        else:
            if attempt_count == 9:
                lbl_progress['foreground'] = 'black'
                lbl_progress['text'] = 'Боевая ничья!'
            else:
                lbl_progress['foreground'] = color(not attempt)
                lbl_progress['text'] = f'Очередь {players[not attempt]} ({marker(not attempt)})'
                attempt = not attempt

    # нажатие кнопок поля
    def click(row, col):
        global attempt
        global attempt_count
        global players
        # если пользователь начнёт нажимать кнопки на поле до инициализации глобальных переменных
        try:
            if field[row][col]['text'] == '' and attempt_count < 9:
                field[row][col]['foreground'] = color(attempt)
                field[row][col]['text'] = marker(attempt)
                attempt_count += 1
                # проверка статуса
                check_status()
                # если играет ai и его ход
                if ai.get() and attempt:
                    ai_move()
                    check_status()
        except:
            pass

    # новая игра
    def new_game():
        global players
        if ai.get():
            ent_player_1.delete(0, tk.END)
            ent_player_1.insert(0, 'Компьютер')
            ent_player_0.delete(0, tk.END)
            ent_player_0.insert(0, 'Человек')
        else:
            ent_player_1.delete(0, tk.END)
            ent_player_1.insert(0, 'Второй игрок')
        players = [ent_player_0.get(), ent_player_1.get()]
        for row in range(3):
            for col in range(3):
                field[row][col]['background'] = 'light gray'
                field[row][col]['text'] = ''
        global attempt
        attempt = bool(getrandbits(1))
        global attempt_count
        attempt_count = 0
        if ai.get() and attempt:
            ai_move()
            attempt = not attempt
        lbl_progress['foreground'] = color(attempt)
        lbl_progress['text'] = f'Очередь {players[attempt]} ({marker(attempt)})'

    # задание игрового поля. 3 списка 3 списков Button
    def make_field():
        for row in range(3):
            line = []
            for col in range(3):
                button = tk.Button(master=frame_field, text='', width=6, height=3,
                                   font=('Arial', 20, 'bold'), background='light gray',
                                   command=lambda row=row, col=col: click(row, col))
                button.grid(row=row, column=col, padx=1, pady=1, sticky='nsew')
                line.append(button)
            field.append(line)

    ttt = tk.Tk()
    ttt.title("Игра крестики-нолики")
    ttt.geometry('350x500')

    # для checkbutton (выбор AI)
    ai = tk.BooleanVar()
    # для checkbutton (выбор IQ)
    aq = tk.BooleanVar()

    # описание виджетов и рамок
    frame_players = tk.Frame(ttt)
    frame_players.grid(row=0, column=0)

    lbl_player_0 = tk.Label(master=frame_players, text='Первый игрок')
    ent_player_0 = tk.Entry(master=frame_players)
    ent_player_0.insert(0, 'Первый игрок')
    lbl_player_0.grid(row=0, column=0, sticky='w')
    ent_player_0.grid(row=1, column=0)
    lbl_player_1 = tk.Label(master=frame_players, text='Второй игрок')
    ent_player_1 = tk.Entry(master=frame_players)
    ent_player_1.insert(0, 'Второй игрок')
    lbl_player_1.grid(row=0, column=1, sticky='e')
    ent_player_1.grid(row=1, column=1)

    chbtn_ai = tk.Checkbutton(master=frame_players, text='AI', variable=ai)
    chbtn_ai.grid(row=1, column=2)
    chbtn_iq = tk.Checkbutton(master=frame_players, text='IQ', variable=aq)
    chbtn_iq.grid(row=1, column=3)

    frame_field = tk.Frame(ttt)
    frame_progress = tk.Frame(ttt)
    btn_start = tk.Button(master=frame_progress, text='Новая игра', width=20,
                          font=('Arial', 20, 'bold'), background='orange',
                          command=new_game)
    btn_start.grid(row=1, column=0)
    lbl_progress = tk.Label(master=frame_progress, text='Для начала игры нажмите кнопку', image='',
                            font=('Arial', 15, 'bold'))
    lbl_progress.grid(row=0, column=0)

    # размещение виджетов
    frame_field.grid(row=1, column=0)
    frame_progress.grid(row=2, column=0)

    make_field()

    ttt.mainloop()
