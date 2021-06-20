from tkinter import *
from tkinter import messagebox
import random, time,  pickle, threading, sys

root = Tk()

table_width=800
table_height=500
card_width=71
card_height=96
between_cards = card_width - 10
card_start_width_p1 = 200
card_start_width_p2 = card_start_width_p1 + between_cards*6
card_start_height_p1 = 330
card_start_height_p2 = 50

root.title("섯다 by 프기 프로젝트 5조")
root.resizable(0,0)
root.wm_iconbitmap("icon.ico")
canvas=Canvas(root, width = table_width, height = table_height,\
              bd=0, highlightthickness=0)
canvas.pack()


class Menu_contents():
    def __init__(self):
        self.im_seottahands = PhotoImage(file='seotta_hands.gif')
        self.im_seottabot = PhotoImage(file='seottabot.gif')
        self.im_Teamfive = PhotoImage(file='Team_5.gif')
        self.nickname = ""
        self.E1 = 0
        self.var = IntVar()
        self.R = []

    # ranking server plan
    # DB에 저장할 자료: nickname, money, level, 저장시간

    def load(self):
        try:
            with open('save.pkl', 'rb') as f:
                self.unpickled_file = pickle.load(f)
                if len(self.unpickled_file) > 30:  # 최근 10개만 남기고 기록 삭제
                    while len(self.unpickled_file) > 30:
                        self.unpickled_file.pop(0)
            self.popup_load = Toplevel()
            self.popup_load.title("불러오기")
            self.popup_load.resizable(0, 0)
            self.popup_load.attributes("-topmost", 1, "-toolwindow", 1)

            # 제목행
            Label(self.popup_load, text="선택") \
                .grid(row=0, column=0, padx=5, pady=5)
            Label(self.popup_load, text="닉네임") \
                .grid(row=0, column=1, padx=5, pady=5)
            Label(self.popup_load, text="소지금") \
                .grid(row=0, column=2, padx=5, pady=5)
            Label(self.popup_load, text="카드 패") \
                .grid(row=0, column=3, padx=5, pady=5)

            # 내용
            num = len(self.unpickled_file)  # number of saved records
            for x in range(0, num, 3):
                self.R.append(Radiobutton(self.popup_load, variable=self.var, value=x))
                self.R[-1].grid(row=num - x - 2, column=0, padx=5, pady=0)
                Label(self.popup_load, text=self.unpickled_file[x]['nickname']) \
                    .grid(row=num - x-2, column=1, padx=5, pady=0)
                Label(self.popup_load, text=self.unpickled_file[x]['p_money']) \
                    .grid(row=num - x-2, column=2, padx=5, pady=0)
                Label(self.popup_load, text=self.unpickled_file[x]['p_rank_name']) \
                    .grid(row=num - x-2, column=3, padx=5, pady=0)
            Button(self.popup_load, text="Load", width=8, height=(num//3) * 2 + 1,
                   command=self.getCheck). \
                grid(row=0, column=4, rowspan=num + 1, padx=5, pady=5)
            self.R[-1].select()
        except:
            messagebox.showinfo("불러오기", "세이브파일이 없습니다.")

    def getCheck(self):
        self.nickname = self.unpickled_file[self.var.get()]['nickname']
        player.money = self.unpickled_file[self.var.get()]['p_money']
        player.card1 = self.unpickled_file[self.var.get()]['card1']
        player.card2 = self.unpickled_file[self.var.get()]['card2']
        game.p_rank_name = self.unpickled_file[self.var.get()]['p_rank_name']
        game.p_rank = self.unpickled_file[self.var.get()]['p_rank']
        com.card1 = self.unpickled_file[self.var.get()]['card_1']
        com.card2 = self.unpickled_file[self.var.get()]['card_2']
        game.side = self.unpickled_file[self.var.get()]['side']
        game.c_rank = self.unpickled_file[self.var.get()]['c_rank']
        game.c_rank_name = self.unpickled_file[self.var.get()]['c_rank_name']
        com.money = self.unpickled_file[self.var.get()]['c_money']
        player.p_betted = self.unpickled_file[self.var.get()]['p_bet']
        player.bet_amount = self.unpickled_file[self.var.get()]['p_bet_amount']
        com.c_betted = self.unpickled_file[self.var.get()]['c_bet']
        com.bet_amount = self.unpickled_file[self.var.get()]['c_bet_amount']
        bet.money_betted = self.unpickled_file[self.var.get()]['money_betted']

        messagebox.showinfo("불러오기", "데이터를 성공적으로 불러왔습니다.")
        self.popup_load.destroy()
        ## 여기부터 판을 다시 그리는 코드
        canvas.delete(bet.bettxt_p1)
        deck.player_cards = [player.card1, player.card2]
        deck.com_cards = [com.card1, com.card2]
        bet.disabling_all()
        delete_photo_txt()
        background = PhotoImage(file='table.gif')
        bg = canvas.create_image(0, 0, anchor=NW, image=background)
        root.update()
        show_deck_image()
        play_deck_sound()
        show_player_cards()
        show_com_cards()
        bet.show_chips()
        if bet.money_betted == 2000000:
            bet.bet_first(game.side)
        else:
            bet.bet_next(game.side)

    def save(self):
        self.popup_save = Toplevel()
        self.popup_save.title("저장")
        self.popup_save.resizable(0, 0)
        self.popup_save.attributes("-topmost", 1, "-toolwindow", 1)
        Label(self.popup_save, text="닉네임"). \
            grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.E1 = Entry(self.popup_save, bd=4)
        self.E1.grid(row=0, column=1, sticky="e", padx=5, pady=5)
        Label(self.popup_save, text="소지금: "). \
            grid(row=1, column=0, sticky="w", padx=5, pady=5)
        Label(self.popup_save, text=player.money). \
            grid(row=1, column=1, sticky="e", padx=5, pady=5)
        Label(self.popup_save, text="카드 패: "). \
            grid(row=2, column=0, sticky="w", padx=5, pady=5)
        Label(self.popup_save, text=game.p_rank_name). \
            grid(row=2, column=1, sticky="e", padx=5, pady=5)
        Button(self.popup_save, text="저장", width=8, height=6, \
               command=self.getText). \
            grid(row=0, column=2, rowspan=2, padx=5, pady=5)
        self.E1.focus()
        self.popup_save.bind("<Return>", lambda event: self.getText())

    def getText(self):
        self.nickname = self.E1.get()
        rank[self.nickname] = player.money
        sorted_rank = sorted(rank, key=lambda k: rank[k], reverse=True)
        if self.nickname == "":
            messagebox.showinfo("Error", "닉네임을 입력해주세요")
        elif self.nickname.count(':') > 0 or self.nickname.count(',') > 0:
            messagebox.showinfo("Error", "닉네임은 \':\' 또는 \',\'.를 포함할 수 없습니다")
        else:
            # local save
            unpickled_file = []
            try:
                with open('save.pkl', 'rb') as f:
                    unpickled_file += pickle.load(f)
            except:
                pass
            with open('save.pkl', 'wb') as f:
                new_data = {'nickname': self.nickname, 'p_money': player.money, 'card1': player.card1,
                            'card2': player.card2, 'p_rank_name': game.p_rank_name, 'card_1': com.card1,
                            'card_2': com.card2, 'side': game.side, 'c_rank': game.c_rank,
                            'c_rank_name': game.c_rank_name, 'p_rank': game.p_rank, 'c_money': com.money,
                            'p_bet': player.p_betted, 'p_bet_amount': player.bet_amount,
                            'c_bet': com.c_betted, 'c_bet_amount': com.bet_amount,
                            'money_betted': bet.money_betted}
                unpickled_file.append(new_data)
                unpickled_file.append(rank)
                unpickled_file.append(sorted_rank)
                pickle.dump(unpickled_file, f)
                messagebox.showinfo("저장", "저장되었습니다.")
                self.popup_save.destroy()

    def rank(self):
        global sorted_rank, rank
        self.rank_list = []
        self.rank_nickname = []
        try:
            with open('save.pkl', 'rb') as f:
                self.unpickled_file = pickle.load(f)
            sorted_rank = self.unpickled_file[-1]
            rank = self.unpickled_file[-2]
            for x in sorted_rank:
                self.rank_list.append(rank[x])
                self.rank_nickname.append(x)
        except:
            pass
        self.popup_rank = Toplevel()
        self.popup_rank.title("랭킹")
        self.popup_rank.resizable(0, 0)
        self.popup_rank.attributes("-topmost", 1, "-toolwindow", 1)

        # show subject line
        Label(self.popup_rank, text="순위") \
            .grid(row=0, column=0, padx=5, pady=5, ipadx=5)
        Label(self.popup_rank,
              text="닉네임").grid(row=0, column=1, padx=5, pady=5, ipadx=5)
        Label(self.popup_rank,
              text="소지금").grid(row=0, column=2, padx=5, pady=5, ipadx=5)

        # show split bar
        Label(self.popup_rank,
              text="------").grid(row=1, column=0, padx=5, pady=0, ipadx=5)
        Label(self.popup_rank,
              text="-------------") \
            .grid(row=1, column=1, padx=5, pady=0, ipadx=5)
        Label(self.popup_rank,
              text="--------------------------").grid(row=1, column=2, padx=5, pady=0, ipadx=5)

        #랭킹 표시
        try:
            self.length = len(sorted_rank)
        except:
            self.length = 0

        if self.length > 20:
            for i in range(20):
                Label(self.popup_rank,
                      text=i + 1).grid(row=i + 2, column=0, padx=5, pady=5, ipadx=5)
            for i in range(20):
                Label(self.popup_rank,
                      text=self.rank_nickname[i]).grid(row=i + 2, column=1, padx=5, pady=5, ipadx=5)
            for i in range(20):
                Label(self.popup_rank,
                      text=self.rank_list[i]).grid(row=i + 2, column=2, padx=5, pady=5, ipadx=5)
        else:
            for i in range(self.length):
                Label(self.popup_rank,
                      text=i + 1).grid(row=i + 2, column=0, padx=5, pady=5, ipadx=5)
            for i in range(self.length):
                Label(self.popup_rank,
                      text=self.rank_nickname[i]).grid(row=i + 2, column=1, padx=5, pady=5, ipadx=5)
            for i in range(self.length):
                Label(self.popup_rank,
                      text=self.rank_list[i]).grid(row=i + 2, column=2, padx=5, pady=5, ipadx=5)

    def seotta_hands(self):  # 완료
        self.popup_seottahands = Toplevel()
        self.popup_seottahands.title("섯다 족보")
        self.popup_seottahands.resizable(0, 0)
        self.popup_seottahands.attributes("-topmost", 1, "-toolwindow", 1)
        self.canvas_seottahands = Canvas(self.popup_seottahands, width=1127, \
                                        height=622, bd=0)
        self.canvas_seottahands.pack()
        self.canvas_seottahands.create_image(0, 0, anchor=NW, image=self.im_seottahands)

    def betting(self):
        self.popup_betting = Toplevel()
        self.popup_betting.title("배팅")
        self.popup_betting.resizable(0, 0)
        self.popup_betting.attributes("-topmost", 1, "-toolwindow", 1)

        # show subject line
        Label(self.popup_betting, text="배팅의 종류") \
            .grid(row=0, column=0, padx=5, pady=5, ipadx=5)
        Label(self.popup_betting, \
              text="Description") \
            .grid(row=0, column=1, padx=5, pady=5, ipadx=5)

        # show split bar
        Label(self.popup_betting, \
              text="---------------------").grid(row=1, column=0, padx=5, pady=0, ipadx=5)
        Label(self.popup_betting, \
              text="----------------------------------------------------------------------------------------") \
            .grid(row=1, column=1, padx=5, pady=0, ipadx=5)

        # Call
        Label(self.popup_betting, \
              text="콜").grid(row=2, column=0, padx=5, pady=5, ipadx=5)
        Label(self.popup_betting, \
              text="상대가 배팅한 금액만큼 배팅한다. 이 경우 해당 판 배팅은 중지된다.") \
            .grid(row=2, column=1, padx=5, pady=5, ipadx=5)

        # Fold
        Label(self.popup_betting, \
              text="다이").grid(row=3, column=0, padx=5, pady=5, ipadx=5)
        Label(self.popup_betting, \
              text="이번 판을 포기한다.") \
            .grid(row=3, column=1, padx=5, pady=5, ipadx=5)

        # Check
        Label(self.popup_betting, \
              text="삥").grid(row=4, column=0, padx=5, pady=5, ipadx=5)
        Label(self.popup_betting, \
              text="기본 배팅 (100 만) *현재 비활성화") \
            .grid(row=4, column=1, padx=5, pady=5, ipadx=5)

        # Double
        Label(self.popup_betting, \
              text="따당").grid(row=8, column=0, padx=5, pady=5, ipadx=5)
        Label(self.popup_betting, \
              text="상대가 배팅한 금액의 2 배를 배팅한다.") \
            .grid(row=8, column=1, padx=5, pady=5, ipadx=5)

        # Half
        Label(self.popup_betting, \
              text="하프").grid(row=6, column=0, padx=5, pady=5, ipadx=5)
        Label(self.popup_betting, \
              text="상대가 배팅한 금액을 받고 현재 판돈의 절반을 추가로 배팅한다.") \
            .grid(row=6, column=1, padx=5, pady=5, ipadx=5)

        # Full
        Label(self.popup_betting, \
              text="풀").grid(row=5, column=0, padx=5, pady=5, ipadx=5)
        Label(self.popup_betting, \
              text="이번 배팅으로 1인 배팅 한도 금액 (10 억)을 초과할 경우 한도까지 배팅한다.") \
            .grid(row=5, column=1, padx=5, pady=5, ipadx=5)

        # All in
        Label(self.popup_betting, \
              text="올 인").grid(row=7, column=0, padx=5, pady=5, ipadx=5)
        Label(self.popup_betting, \
              text="소지금을 전부 배팅한다. 단, 상대가 최소 콜을 선택할 수 있어야 한다.") \
            .grid(row=7, column=1, padx=5, pady=5, ipadx=5)


    def seotta_bot(self):  # 완료
        self.popup_seottabot = Toplevel()
        self.popup_seottabot.title("섯다 COM은...")
        self.popup_seottabot.resizable(0, 0)
        self.popup_seottabot.attributes("-topmost", 1, "-toolwindow", 1)
        self.canvas_seottabot = Canvas(self.popup_seottabot, width=400, height=200, bd=0)
        self.canvas_seottabot.pack()
        self.canvas_seottabot.create_image(10, 10, anchor=NW,
                                          image=self.im_seottabot)
        self.canvas_seottabot.create_text(10, 120, anchor=NW,
                                         text="COM은 플레이어의 패를 알 수 없습니다.")
        self.canvas_seottabot.create_text(10, 140, anchor=NW,
                                         text="COM은 자기 패에 따라 배팅을 결정합니다.")
        self.canvas_seottabot.create_text(10, 160, anchor=NW,
                                         text="프로젝트가 끝나고 나서도 생각이 나면 업그레이드를 시킬 예정입니다.")

    def about(self):  # 완료
        self.popup_about = Toplevel()
        self.popup_about.title("개발자 정보")
        self.popup_about.resizable(0, 0)
        self.popup_about.attributes("-topmost", 1, "-toolwindow", 1)
        self.canvas_about = Canvas(self.popup_about, width=500, height=100, bd=0)
        self.canvas_about.pack()
        self.canvas_about.create_image(10, 30, anchor=NW, \
                                       image=self.im_Teamfive)
        self.canvas_about.create_text(70, 30, anchor=NW, \
                                      text="- Version: 1.0 (by. 박시몬, 홍정민, 김진원)")
        self.canvas_about.create_text(70, 50, anchor=NW, \
                                      text="- 이 프로그램은 GoPoker의 코드를 직접 수정, 개조한 것입니다.")
        self.canvas_about.create_text(70, 70, anchor=NW, \
                                      text="- 버그가 발견된다면 simonida@hanyang.ac.kr로 연락주세요.")


def image_path(number_of_card):
    path=str(number_of_card)
    path=path+'.png'
    return path

def show_deck_image():
    for x in range(20):
        deck_image.append(canvas.create_image(25 + x*2.5, 190, \
                                             anchor=NW, image=b1fv_image))
        deck_place.append(25 + x*2.5)
        root.after(5,root.update())

def play_deck_sound():
    return 0;
def show_player_cards():
    start_x = deck_place[-1]
    delta_xa = ((card_start_width_p1 + between_cards * 0) - start_x) / 10
    delta_xb = ((card_start_width_p1 + between_cards * 1) - start_x) / 10
    delta_y = (card_start_height_p1 - 190) / 10
    deck.player_slot = []
    for x in range(2):
        deck.player_slot.append(canvas.create_image(
        start_x, 190, image=deck.card_images[deck.player_cards[x] - 1], anchor='nw'))

    for i in range(0, 11):
        canvas.move(deck.player_slot[0], delta_xa, delta_y)
        root.after(10, root.update())
    for i in range(0, 11):
        canvas.move(deck.player_slot[1], delta_xb, delta_y)
        root.after(10, root.update())
    bet.show_message(1, game.p_rank_name)

def show_com_cards():
    start_x = deck_place[-1]
    delta_xa = ((card_start_width_p2 - between_cards * 0) - start_x) / 10
    delta_xb = ((card_start_width_p2 + between_cards * 1) - start_x) / 10
    delta_y = (card_start_height_p2 - 190) / 10
    deck.com_slot = []
    for x in range(2):
        deck.com_slot.append(canvas.create_image( \
        start_x, 190, image=b1fv_image, anchor='nw'))
    for i in range(0, 10):
        time.sleep(0.00001)
        canvas.move(deck.com_slot[0], delta_xa, delta_y)
        root.after(10, root.update())
    for i in range(0, 10):
        time.sleep(0.00001)
        canvas.move(deck.com_slot[1], delta_xb, delta_y)
        root.after(10, root.update())

def play_betting_sound():
    return 0;
def play_cash_sound():
    return 0;
def play_win_sound():
     return 0;

def play_lose_sound():
    return 0;

#카드 생성 소스
class Deck:
    def __init__(self):
        self.cards = []
        for i in range(20):
            self.cards.append(i+1)
        self.card_images = []
        self.player_cards = [player.card1, player.card2]
        self.com_cards = [com.card1, com.card2]
        self.com_slot = []
        self.player_slot = []

    def card_pop(self):
        return self.cards.pop(0)##첫 번째 카드 뽑기

    ##게임 소스


class Game:
    def __init__(self):
        self.winner = 1
        self.draw = 0 #무승부 여부 확인 변수
        self.side = 0
        self.p_rank = 28
        self.p_rank_name = "패 이름"
        self.c_rank = 28
        self.c_rank_name = "패 이름"
        self.winner_txt_a = ''
        self.winner_txt_b = ''
        self.winner_txt_c = ''
        self.winner_txt_d = ''


    def set(self):
        if deck.cards == []: ##덱이 다 떨어지면 다시 채운다
            deck.__init__()
            self.set()
        else:
            player.card1 = deck.card_pop() ##카드를 위에부터 하나씩 나눠준다.
            com.card1 = deck.card_pop()
            player.card2 = deck.card_pop()
            com.card2 = deck.card_pop()
            game.get_cards_rank()
            time.sleep(2)


    ##족보에 따른 플레이어 패 랭크 보여주기
    def get_cards_rank(self):
        p_sum = player.card1 + player.card2
        c_sum = com.card1 + com.card2
        game.p_rank = 28
        game.c_rank = 28

        ##삼팔광땡
        if (player.card1 == 13 and player.card2 == 18) or (player.card1 == 18 and player.card2 == 13):
            game.p_rank = 1
            game.p_rank_name = "삼팔광땡"

        ##광땡
        elif (
                (player.card1 == 11 and player.card2 == 18) or (player.card1 == 11 and player.card2 == 13) or
                (player.card1 == 18 and player.card2 == 11) or (player.card1 == 13 and player.card2 == 11)
        ):
            game.p_rank = 2
            game.p_rank_name = "광땡"

        ##장땡~삥땡
        elif player.card1 == player.card2 - 10:
            game.p_rank = 13 - player.card1
            if game.p_rank == 12:
                game.p_rank_name = "삥땡"
            elif game.p_rank == 11:
                game.p_rank_name = "2땡"
            elif game.p_rank == 10:
                game.p_rank_name = "3땡"
            elif game.p_rank == 9:
                game.p_rank_name = "4땡"
            elif game.p_rank == 8:
                game.p_rank_name = "5땡"
            elif game.p_rank == 7:
                game.p_rank_name = "6땡"
            elif game.p_rank == 6:
                game.p_rank_name = "7땡"
            elif game.p_rank == 5:
                game.p_rank_name = "8땡"
            elif game.p_rank == 4:
                game.p_rank_name = "9땡"
            elif game.p_rank == 3:
                game.p_rank_name = "장땡"
        elif player.card2 == player.card1 - 10:
            game.p_rank = 13 - player.card2
            if game.p_rank == 12:
                game.p_rank_name = "삥땡"
            elif game.p_rank == 11:
                game.p_rank_name = "2땡"
            elif game.p_rank == 10:
                game.p_rank_name = "3땡"
            elif game.p_rank == 9:
                game.p_rank_name = "4땡"
            elif game.p_rank == 8:
                game.p_rank_name = "5땡"
            elif game.p_rank == 7:
                game.p_rank_name = "6땡"
            elif game.p_rank == 6:
                game.p_rank_name = "7땡"
            elif game.p_rank == 5:
                game.p_rank_name = "8땡"
            elif game.p_rank == 4:
                game.p_rank_name = "9땡"
            elif game.p_rank == 3:
                game.p_rank_name = "장땡"

        ##알리
        elif (player.card1 == 1 or player.card1 == 11) and (player.card2 == 2 or player.card2 == 12):
            game.p_rank = 13
            game.p_rank_name = "알리"
        elif (player.card1 == 2 or player.card1 == 12) and (player.card2 == 1 or player.card2 == 11):
            game.p_rank = 13
            game.p_rank_name = "알리"

        ##독사
        elif (player.card1 == 1 or player.card1 == 11) and (player.card2 == 4 or player.card2 == 14):
            game.p_rank = 14
            game.p_rank_name = "독사"
        elif (player.card1 == 4 or player.card1 == 14) and (player.card2 == 1 or player.card2 == 11):
            game.p_rank = 14
            game.p_rank_name = "독사"

        ##구삥
        elif (player.card1 == 1 or player.card1 == 11) and (player.card2 == 9 or player.card2 == 19):
            game.p_rank = 15
            game.p_rank_name = "구삥"
        elif (player.card1 == 9 or player.card1 == 19) and (player.card2 == 1 or player.card2 == 11):
            game.p_rank = 15
            game.p_rank_name = "구삥"

        ##장삥
        elif (player.card1 == 1 or player.card1 == 11) and (player.card2 == 10 or player.card2 == 20):
            game.p_rank = 16
            game.p_rank_name = "장삥"
        elif (player.card1 == 10 or player.card1 == 20) and (player.card2 == 1 or player.card2 == 11):
            game.p_rank = 16
            game.p_rank_name = "장삥"

        ##장사
        elif (player.card1 == 10 or player.card1 == 20) and (player.card2 == 4 or player.card2 == 14):
            game.p_rank = 17
            game.p_rank_name = "장사"
        elif (player.card1 == 4 or player.card1 == 14) and (player.card2 == 10 or player.card2 == 20):
            game.p_rank = 17
            game.p_rank_name = "장사"

        ##세륙
        elif (player.card1 == 6 or player.card1 == 16) and (player.card2 == 4 or player.card2 == 14):
            game.p_rank = 18
            game.p_rank_name = "세륙"
        elif (player.card1 == 4 or player.card1 == 14) and (player.card2 == 6 or player.card2 == 16):
            game.p_rank = 18
            game.p_rank_name = "세륙"

        ##갑오~망통
        else:
            for i in range(10):
                if p_sum % 10 == i:
                    game.p_rank = 28 - i
                if game.p_rank == 28:
                    game.p_rank_name = "망통"
                elif game.p_rank == 27:
                    game.p_rank_name = "1끗"
                elif game.p_rank == 26:
                    game.p_rank_name = "2끗"
                elif game.p_rank == 25:
                    game.p_rank_name = "3끗"
                elif game.p_rank == 24:
                    game.p_rank_name = "4끗"
                elif game.p_rank == 23:
                    game.p_rank_name = "5끗"
                elif game.p_rank == 22:
                    game.p_rank_name = "6끗"
                elif game.p_rank == 21:
                    game.p_rank_name = "7끗"
                elif game.p_rank == 20:
                    game.p_rank_name = "8끗"
                elif game.p_rank == 19:
                    game.p_rank_name = "갑오"

        ##컴퓨터 패 랭크
        ##삼팔광땡
        if (com.card1 == 13 and com.card2 == 18) or (com.card1 == 18 and com.card2 == 13):
            game.c_rank = 1
            game.c_rank_name = "삼팔광땡"

        ##광땡
        elif (
                (com.card1 == 11 and com.card2 == 18) or (com.card1 == 11 and com.card2 == 13) or
                (com.card1 == 18 and com.card2 == 11) or (com.card1 == 13 and com.card2 == 11)
        ):
            game.c_rank = 2
            game.c_rank_name = "광땡"

        ##장땡~삥땡
        elif com.card1 == com.card2 - 10:
            game.c_rank = 13 - com.card1
            if game.c_rank == 12:
                game.c_rank_name = "삥땡"
            elif game.c_rank == 11:
                game.c_rank_name = "2땡"
            elif game.c_rank == 10:
                game.c_rank_name = "3땡"
            elif game.c_rank == 9:
                game.c_rank_name = "4땡"
            elif game.c_rank == 8:
                game.c_rank_name = "5땡"
            elif game.c_rank == 7:
                game.c_rank_name = "6땡"
            elif game.c_rank == 6:
                game.c_rank_name = "7땡"
            elif game.c_rank == 5:
                game.c_rank_name = "8땡"
            elif game.c_rank == 4:
                game.c_rank_name = "9땡"
            elif game.c_rank == 3:
                game.c_rank_name = "장땡"
        elif com.card2 == com.card1 - 10:
            game.c_rank = 13 - com.card2
            if game.c_rank == 12:
                game.c_rank_name = "삥땡"
            elif game.c_rank == 11:
                game.c_rank_name = "2땡"
            elif game.c_rank == 10:
                game.c_rank_name = "3땡"
            elif game.c_rank == 9:
                game.c_rank_name = "4땡"
            elif game.c_rank == 8:
                game.c_rank_name = "5땡"
            elif game.c_rank == 7:
                game.c_rank_name = "6땡"
            elif game.c_rank == 6:
                game.c_rank_name = "7땡"
            elif game.c_rank == 5:
                game.c_rank_name = "8땡"
            elif game.c_rank == 4:
                game.c_rank_name = "9땡"
            elif game.c_rank == 3:
                game.c_rank_name = "장땡"

        ##알리
        elif (com.card1 == 1 or com.card1 == 11) and (com.card2 == 2 or com.card2 == 12):
            game.c_rank = 13
            game.c_rank_name = "알리"
        elif (com.card1 == 2 or com.card1 == 12) and (com.card2 == 1 or com.card2 == 11):
            game.c_rank = 13
            game.c_rank_name = "알리"

        ##독사
        elif (com.card1 == 1 or com.card1 == 11) and (com.card2 == 4 or com.card2 == 14):
            game.c_rank = 14
            game.c_rank_name = "독사"
        elif (com.card1 == 4 or com.card1 == 14) and (com.card2 == 1 or com.card2 == 11):
            game.c_rank = 14
            game.c_rank_name = "독사"

        ##구삥
        elif (com.card1 == 1 or com.card1 == 11) and (com.card2 == 9 or com.card2 == 19):
            game.c_rank = 15
            game.c_rank_name = "구삥"
        elif (com.card1 == 9 or com.card1 == 19) and (com.card2 == 1 or com.card2 == 11):
            game.c_rank = 15
            game.c_rank_name = "구삥"

        ##장삥
        elif (com.card1 == 1 or com.card1 == 11) and (com.card2 == 10 or com.card2 == 20):
            game.c_rank = 16
            game.c_rank_name = "장삥"
        elif (com.card1 == 10 or com.card1 == 20) and (com.card2 == 1 or com.card2 == 11):
            game.c_rank = 16
            game.c_rank_name = "장삥"

        ##장사
        elif (com.card1 == 10 or com.card1 == 20) and (com.card2 == 4 or com.card2 == 14):
            game.c_rank = 17
            game.c_rank_name = "장사"
        elif (com.card1 == 4 or com.card1 == 14) and (com.card2 == 10 or com.card2 == 20):
            game.c_rank = 17
            game.c_rank_name = "장사"

        ##세륙
        elif (com.card1 == 6 or com.card1 == 16) and (com.card2 == 4 or com.card2 == 14):
            game.c_rank = 18
            game.c_rank_name = "세륙"
        elif (com.card1 == 4 or com.card1 == 14) and (com.card2 == 6 or com.card2 == 16):
            game.c_rank = 18
            game.c_rank_name = "세륙"

        ##갑오~망통
        else:
            for i in range(10):
                if c_sum % 10 == i:
                    game.c_rank = 28 - i
                if game.c_rank == 28:
                    game.c_rank_name = "망통"
                elif game.c_rank == 27:
                    game.c_rank_name = "1끗"
                elif game.c_rank == 26:
                    game.c_rank_name = "2끗"
                elif game.c_rank == 25:
                    game.c_rank_name = "3끗"
                elif game.c_rank == 24:
                    game.c_rank_name = "4끗"
                elif game.c_rank == 23:
                    game.c_rank_name = "5끗"
                elif game.c_rank == 22:
                    game.c_rank_name = "6끗"
                elif game.c_rank == 21:
                    game.c_rank_name = "7끗"
                elif game.c_rank == 20:
                    game.c_rank_name = "8끗"
                elif game.c_rank == 19:
                    game.c_rank_name = "갑오"


    def get_winner(self):
        canvas.delete(bet.bettxt_p1)
        for x in range(2):  # COM카드 뒤집기
            time.sleep(0.2)
            root.update()
        canvas.delete(bet.bettxt_p1)
        game.winner_txt_a = canvas.create_text(500, 200, anchor='w', fill='yellow', \
                           font=("a시네마B 보통", 15, 'bold'), text='Com    :')
        game.winner_txt_b = canvas.create_text(600, 200, anchor='w', fill='yellow', \
                           font=("a시네마B 보통", 15, 'bold'), text=game.c_rank_name)
        game.winner_txt_c = canvas.create_text(500, 230, anchor='w', fill='yellow', \
                           font=("a시네마B 보통", 15, 'bold'), text='플레이어 :')
        game.winner_txt_d = canvas.create_text(600, 230, anchor='w', fill='yellow', \
                           font=("a시네마B 보통", 15, 'bold'), text=game.p_rank_name)
        root.update()
        time.sleep(1)

        if player.money != 0 and com.money != 0:
            canvas.delete(bet.bettxt_p1)
            if game.p_rank < game.c_rank:
                game.winner = 1
                text = canvas.create_text(500, 270, anchor='w', fill='yellow', \
                                          font=("Times", 20, 'bold'), text='Player 의 승리입니다!!')
            elif game.p_rank == game.c_rank:
                game.winner = random.choice([1, 2])
                game.draw = 1
                text = canvas.create_text(500, 270, anchor='w', fill='yellow', \
                                          font=("Times", 20, 'bold'), text='무승부입니다.')
            else:
                game.winner = 2
                text = canvas.create_text(500, 270, anchor='w', fill='yellow', \
                                          font=("Times", 20, 'bold'), text='Com이 이겼습니다...')
            for x in range(90):
                canvas.move(text, 1, 0)
                root.after(10, root.update())
            canvas.delete(text)
            canvas.delete(bet.bettxt_p1)
            canvas.delete(game.winner_txt_a)
            canvas.delete(game.winner_txt_b)
            canvas.delete(game.winner_txt_c)
            canvas.delete(game.winner_txt_d)
            bet.close_money()

        elif player.money == 0 or com.money == 0:
            canvas.delete(bet.bettxt_p1)
            if game.p_rank < game.c_rank:
                game.winner = 1
                text = canvas.create_text(500, 270, anchor='w', fill='yellow', \
                                          font=("Times", 20, 'bold'), text='Player 의 승리입니다!!')
            elif game.p_rank == game.c_rank:
                game.winner = random.choice([1, 2])
                game.draw = 1
                text = canvas.create_text(500, 270, anchor='w', fill='yellow', \
                                          font=("Times", 20, 'bold'), text='무승부입니다.')
            else:
                game.winner = 2
                text = canvas.create_text(500, 270, anchor='w', fill='yellow', \
                                          font=("Times", 20, 'bold'), text='Com이 이겼습니다...')
            for x in range(90):
                canvas.move(text, 1, 0)
                root.after(10, root.update())
            canvas.delete(text)
            canvas.delete(bet.bettxt_p1)
            canvas.delete(game.winner_txt_a)
            canvas.delete(game.winner_txt_b)
            canvas.delete(game.winner_txt_c)
            canvas.delete(game.winner_txt_d)
            bet.close_money()

game = Game()

##플레이어 및 컴퓨터 돈, 카드, 배팅 금액 등등
class Player:
    def __init__(self):
        self.money = 1000000000
        self.card1 = 0
        self.card2 = 0
        self.bet_amount = 0
        self.bet_after = 0
        self.p_betted = 0
        self.c_betted = 0

##플레이어 돈 + 카드 덱
player = Player()
com = Player()
deck = Deck()


class Bet:
    def __init__(self):
        self.chips = []
        self.chips.append([0, 0, 0, 0, 0])  # betting chips
        self.chips.append([0, 0, 0, 0, 0])  # player's chips
        self.chips.append([0, 0, 0, 0, 0])  # com's chips

        self.bot_betting = 1  ##봇이 배팅할 종류(콜, 따당, 하프 등등)
        self.money_betted = 0
        self.chip_image = []
        self.chips_im = []
        self.chips_txt = []
        self.show_bet_button()


    def show_message(self, side = 0, message = None):
        if side == 0:
            text = canvas.create_text(300, 200, anchor='w', fill='black', \
                                      font=("a시네마B 보통", 18, 'bold'), text = message)
            for x in range(20):
                canvas.move(text, 1, 0)
                root.after(10,root.update())
            root.after(1000,canvas.delete(text))
            root.update()
        elif side == 1: # player
            self.bettxt_p1 = canvas.create_text(650, 350, anchor='w', fill='mint cream', \
                                      font=("a시네마B 보통", 18, 'bold'), text = message)
            root.update()
            root.after(1000,)
            root.update()
        elif side == 2: # computer
            self.bettxt_p2 = canvas.create_text(650, 70, anchor='w', fill='magenta', \
                                      font=("a시네마B 보통", 18, 'bold'), text = message)
            root.update()
            root.after(1000,)
            root.update()


    def bot_ddadang_half(self):
        self.bot_betting = random.choice([3, 4])  ##하프나 따당 중 하나를 랜덤으로 고르도록 함
        if self.bot_betting == 3:
            if player.bet_amount * 2 > com.money:
                self.show_message(0, 'COM이 따당을 선택하였습니다.')
                self.show_message(0, "COM의 소지금이 적어 남은 소지금 전부를 배팅합니다.")
                com.bet_amount = com.money
                self.bet_money(2)
                self.bet_next(1)
            else:
                self.show_message(0, 'COM이 따당을 선택하였습니다.')
                com.bet_amount = player.bet_amount * 2
                self.bet_money(2)
                self.bet_next(1)
        else:
            if (
                (player.bet_amount + (self.money_betted // 2)) -
                ((player.bet_amount + (self.money_betted // 2)) % 10000) > com.money
            ):
                self.show_message(0, 'COM이 하프를 선택하였습니다.')
                self.show_message(0, "COM의 소지금이 적어 남은 소지금 전부를 배팅합니다.")
                com.bet_amount = com.money
                self.bet_money(2)
                self.bet_next(1)
            else:
                self.show_message(0, 'COM이 하프를 선택하였습니다.')
                com.bet_amount = (player.bet_amount + (self.money_betted // 2)) - \
                                 ((player.bet_amount + (self.money_betted // 2)) % 10000)
                self.bet_money(2)
                self.bet_next(1)


    def bot_call(self):
        if player.bet_amount > com.money:
            self.show_message(0, 'COM이 콜을 선택하였습니다.')
            self.show_message(0, "COM의 소지금이 적어 소지금 전부를 배팅합니다.")
            com.bet_amount = com.money
            self.bet_money(2)
            game.get_winner()
        else:
            self.show_message(0, 'COM이 콜을 선택하였습니다.')
            com.bet_amount = player.bet_amount
            self.bet_money(2)
            game.get_winner()


    def bet_money(self, side = 0):
        if side == 1:
            self.money_betted += player.bet_amount
            player.money -= player.bet_amount
            player.p_betted += player.bet_amount
        else:
            self.money_betted += com.bet_amount
            com.money -= com.bet_amount
            com.c_betted += com.bet_amount
        threads = []
        threads.append(threading.Thread(target=self.show_chips()))
        threads.append(threading.Thread(target=play_betting_sound()))
        threads[0].start()
        threads[1].start()
        for th in threads:
            th.join()

    def show_chips(self):
        # 칩표시 관련 위치정보
        btw_chips_x = 30 + 4  # 칩 사이의 가로 간격(안 겹치려면 50 이상)
        btw_chips_y = 3  # 칩 사이의 세로 간격(3~5 픽셀이 적당)
        chip_x = []
        chip_x.append(300)  # 베팅된 칩의 배치가 시작되는 x좌표값
        chip_x.append(40)  # 플레이어의 칩 배치가 시작되는 x좌표값
        chip_x.append(40)  # 컴퓨터의 칩 배치가 시작되는 x좌표값
        chip_y = []
        chip_y.append(265)  # 베팅된 칩의 배치가 시작되는 y좌표값
        chip_y.append(card_start_height_p1 + 75)  # 플레이어의 칩 배치가 시작되는 y좌표값
        chip_y.append(card_start_height_p2 + 75)  # 컴퓨터의 칩 배치가 시작되는 y좌표값

        self.chip_image.append(PhotoImage(file='chip_gold_30.gif'))
        self.chip_image.append(PhotoImage(file='chip_black_30.gif'))
        self.chip_image.append(PhotoImage(file='chip_red_30.gif'))
        self.chip_image.append(PhotoImage(file='chip_blue_30.gif'))
        self.chip_image.append(PhotoImage(file='chip_green_30.gif'))

        for x in range(3):
            if x == 0:
                amount = bet.money_betted
            elif x == 1:
                amount = player.money
            else:
                amount = com.money
            temp_10000 = divmod(amount, 100000000)[0]
            self.chips[x][0] = temp_10000
            rest = amount - temp_10000*100000000
            temp_1000 = divmod(rest, 10000000)[0]
            self.chips[x][1] = temp_1000
            rest = rest - temp_1000*10000000
            temp_100 = divmod(rest, 1000000)[0]
            self.chips[x][2] = temp_100
            rest = rest - temp_100*1000000
            temp_10 = divmod(rest, 100000)[0]
            self.chips[x][3] = temp_10
            rest = rest - temp_10*100000
            self.chips[x][4] = divmod(rest, 10000)[0]

            # 기존에 그렸던 이미지와 텍스트를 삭제
            temp1 = len(self.chips_im)
            temp2 = len(self.chips_txt)
            if temp1 > 0:
                for x in range(0, temp1):
                    canvas.delete(self.chips_im[temp1 - 1 - x])
                    self.chips_im.pop()
                for x in range(0, temp2):
                    canvas.delete(self.chips_txt[temp2 - 1 - x])
                    self.chips_txt.pop()

        # 칩 이미지 및 갯수 텍스트 그리기
        for i in range(0, 3):  # side 순서대로 반복
            for j in range(0, 5):  # 비싼 칩 순서로 반복
                for k in range(0, self.chips[i][j]):  # 칩 이미지 그리기
                    self.chips_im.append(canvas.create_image( \
                        chip_x[i] + btw_chips_x * j + random.randint(-2, 2), \
                        chip_y[i] - btw_chips_y * k, image=self.chip_image[j]))
                if self.chips[i][j] != 0:  # 칩 색깔별 갯수
                    self.chips_txt.append(canvas.create_text( \
                        chip_x[i] + btw_chips_x * j + 1, \
                        chip_y[i] - btw_chips_y * self.chips[i][j] - 15, \
                        anchor='center', fill='black', font=("a시네마B 보통", 15), \
                        text=self.chips[i][j]), )
                    self.chips_txt.append(canvas.create_text( \
                        chip_x[i] + btw_chips_x * j - 1, \
                        chip_y[i] - btw_chips_y * self.chips[i][j] - 15, \
                        anchor='center', fill='black', font=("a시네마B 보통", 15), \
                        text=self.chips[i][j]), )
                    self.chips_txt.append(canvas.create_text( \
                        chip_x[i] + btw_chips_x * j, \
                        chip_y[i] - btw_chips_y * self.chips[i][j] - 15 + 1, \
                        anchor='center', fill='black', font=("a시네마B 보통", 15), \
                        text=self.chips[i][j]), )
                    self.chips_txt.append(canvas.create_text( \
                        chip_x[i] + btw_chips_x * j, \
                        chip_y[i] - btw_chips_y * self.chips[i][j] - 15 - 1, \
                        anchor='center', fill='black', font=("a시네마B 보통", 15), \
                        text=self.chips[i][j]), )
                    self.chips_txt.append(canvas.create_text( \
                        chip_x[i] + btw_chips_x * j, \
                        chip_y[i] - btw_chips_y * self.chips[i][j] - 15, \
                        anchor='center', fill='white', font=("a시네마B 보통", 15), \
                        text=self.chips[i][j]), )


            if i == 0:
                if bet.money_betted > 9: # 총 포커칩 포인트
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40 + 1 , chip_y[i] + 40, \
                        anchor='w', fill='black', font=("a시네마B 보통", 15), \
                        text=bet.money_betted))
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40 - 1, chip_y[i] + 40, \
                        anchor='w', fill='black', font=("a시네마B 보통", 15), \
                        text=bet.money_betted))
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40, chip_y[i] + 40 + 1, \
                        anchor='w', fill='black', font=("a시네마B 보통", 15), \
                        text=bet.money_betted))
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40, chip_y[i] + 40 - 1, \
                        anchor='w', fill='black', font=("a시네마B 보통", 15), \
                        text=bet.money_betted))
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40, chip_y[i] + 40, \
                        anchor='w', fill='white', font=("a시네마B 보통", 15), \
                        text=bet.money_betted))
            elif i == 1:
                if player.money > 9: # 총 포커칩 포인트
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40 + 1 , chip_y[i] + 40, \
                        anchor='w', fill='black', font=("a시네마B 보통", 15), \
                        text=player.money))
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40 - 1, chip_y[i] + 40, \
                        anchor='w', fill='black', font=("a시네마B 보통", 15), \
                        text=player.money))
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40, chip_y[i] + 40 + 1, \
                        anchor='w', fill='black', font=("a시네마B 보통", 15), \
                        text=player.money))
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40, chip_y[i] + 40 - 1, \
                        anchor='w', fill='black', font=("a시네마B 보통", 15), \
                        text=player.money))
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40, chip_y[i] + 40, \
                        anchor='w', fill='white', font=("a시네마B 보통", 15), \
                        text=player.money))
            else:
                if com.money > 9: # 총 포커칩 포인트
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40 + 1 , chip_y[i] + 40, \
                        anchor='w', fill='black', font=("a시네마B 보통", 15), \
                        text=com.money))
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40 - 1, chip_y[i] + 40, \
                        anchor='w', fill='black', font=("a시네마B 보통", 15), \
                        text=com.money))
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40, chip_y[i] + 40 + 1, \
                        anchor='w', fill='black', font=("a시네마B 보통", 15), \
                        text=com.money))
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40, chip_y[i] + 40 - 1, \
                        anchor='w', fill='black', font=("a시네마B 보통", 15), \
                        text=com.money))
                    self.chips_txt.append(canvas.create_text(\
                        chip_x[i] + 40, chip_y[i] + 40, \
                        anchor='w', fill='white', font=("a시네마B 보통", 15), \
                        text=com.money))
        root.update()

    def ai_bot(self, side):
        if side == 3:
            canvas.delete(self.bettxt_p1)
            self.show_message(0, 'COM이 선 배팅을 진행합니다.')
            time.sleep(1)
            self.show_message(0, 'COM이 배팅금을 결정하고 있습니다...')
            time.sleep(3)
            if 0 < com.money < 1000000:
                self.show_message(0, 'COM의 소지금이 기본 배팅금보다 적어 전부 배팅합니다.')
                com.bet_amount = com.money
                self.bet_money(2)
                bet.bet_next(1)
            elif 1000000 <= com.money < 5000000:
                com.bet_amount = random.randrange(1000000, 5000000, 100000)
                self.bet_money(2)
                bet.bet_next(1)
            else:
                if 1 <= game.c_rank <= 8:
                    com.bet_amount = random.randrange(5000000, 50000001, 100000)
                    self.bet_money(2)
                    bet.bet_next(1)
                elif 9 <= game.c_rank <= 12:
                    com.bet_amount = random.randrange(4000000, 30000001, 100000)
                    self.bet_money(2)
                    bet.bet_next(1)
                elif 13 <= game.c_rank <= 18:
                    com.bet_amount = random.randrange(3000000, 10000001, 100000)
                    self.bet_money(2)
                    bet.bet_next(1)
                elif 19 <= game.c_rank <= 22:
                    com.bet_amount = random.randrange(1000000, 5000001, 100000)
                    self.bet_money(2)
                    bet.bet_next(1)
                elif 23 <= game.c_rank <= 25:
                    com.bet_amount = random.randrange(1000000, 3000001, 100000)
                    self.bet_money(2)
                    bet.bet_next(1)
                elif 26 <= game.c_rank <= 28:
                    com.bet_amount = random.randrange(1000000, 1500001, 100000)
                    self.bet_money(2)
                    bet.bet_next(1)
        else:
            if 0 <= player.money <= 1000000:
                if 1 <= game.c_rank <= 20:
                    self.show_message(0, 'COM이 콜을 선택했습니다.')
                    com.bet_amount = player.bet_amount
                    self.bet_money(2)
                    canvas.delete(self.bettxt_p1)
                    game.get_winner()
                else:
                    canvas.delete(self.bettxt_p1)
                    self.show_message(0, 'COM이 다이를 선택했습니다.')
                    game.winner = 1
                    self.close_money()
            elif com.money < 1000000:
                canvas.delete(self.bettxt_p1)
                self.show_message(0, 'COM의 소지금이 부족해 소지금을 전부 배팅합니다.')
                com.bet_amount = com.money
                self.bet_money(2)
                self.bet_next(1)
            else:
                canvas.delete(self.bettxt_p1)
                if 1 <= game.c_rank <= 8:  ##컴퓨터의 패가 족보 상위 1~8순위일 경우
                    if self.money_betted <= 400000000:  ##배팅된 금액이 4억 이하일 경우
                        self.bot_ddadang_half()
                    elif self.money_betted > 400000000:
                        self.bot_betting = random.choice([0, 5, 6])
                        if self.bot_betting == 0:
                            self.bot_call()
                        elif self.bot_betting == 5:
                            if com.c_betted + com.money >= 1000000000:
                                com.bet_amount = 1000000000 - com.c_betted
                                self.show_message(0, 'COM이 풀을 선택했습니다.')
                                self.bet_money(2)
                                self.bet_next(1)
                            else:
                                self.ai_bot(1)
                        else:
                            if player.money > com.money:
                                com.bet_amount = com.money
                                self.show_message(0, 'COM이 올 인을 선택했습니다.')
                                self.bet_money(2)
                                self.bet_next(1)
                            else:
                                self.ai_bot(1)
                elif 9 <= game.c_rank <= 12:
                    if self.money_betted <= 280000000:
                        self.bot_ddadang_half()
                    elif self.money_betted > 280000000:
                        self.bot_call()
                elif 13 <= game.c_rank <= 18:
                    if self.money_betted <= 160000000:
                        self.bot_ddadang_half()
                    elif self.money_betted > 160000000:
                        self.bot_call()
                elif 19 <= game.c_rank <= 22:
                    if self.money_betted <= 100000000:
                        self.bot_ddadang_half()
                    elif self.money_betted > 100000000:
                        self.bot_betting = random.choice([0, 2])
                        if self.bot_betting == 0:
                            self.bot_call()
                        else:
                            self.show_message(0, 'COM이 다이를 선택했습니다.')
                            game.winner = 1
                            self.close_money()
                elif 23 <= game.c_rank <= 24:
                    if self.money_betted <= 70000000:
                        self.bot_ddadang_half()
                    else:
                        self.bot_betting = random.choice([0, 2])
                        if self.bot_betting == 0:
                            self.bot_call()
                        else:
                            self.show_message(0, 'COM이 다이를 선택했습니다.')
                            game.winner = 1
                            self.close_money()
                elif 25 <= game.c_rank <= 28:
                    if self.money_betted <= 50000000:
                        self.bot_ddadang_half()
                    else:
                        self.show_message(0, 'COM이 다이를 선택했습니다.')
                        game.winner = 1
                        self.close_money()


    def bet_first(self, side):
        canvas.delete(self.bettxt_p1)
        if side == 1:  # 플레이어가 베팅하는 경우
            game.side = 1
            btcolor = 'orange'
            if 0 < player.money < 100000:
                canvas.delete(self.bettxt_p1)
                self.show_message(0, "소지금이 기본 배팅금보다 적어 전부 배팅합니다.")
                player.bet_amount = player.money
                self.bet_money()
                bet.bet_next(2)
            canvas.delete(self.bettxt_p1)
            self.show_message(0, "Player가 선 배팅을 진행합니다.")
            self.scale.config(bg=btcolor, troughcolor='Dark Orange')
            self.bt_manual.config(state='active', bg=btcolor)
            self.show_message(1, game.p_rank_name)
        else:
            game.side = 2
            self.disabling_all()
            self.ai_bot(3)

    def bet_next(self, side):
        btcolor = 'orange'
        self.disabling_all()
        if side == 1:
            game.side = 1
            if self.bot_betting == 5:
                self.show_message(0, "COM이 풀을 하여 콜 혹은 다이만 가능합니다.")
                self.bt_die.config(state='active', bg = btcolor)
                self.bt_call.config(state='active', bg = 'green')
            elif self.bot_betting == 6:
                self.show_message(0, "COM이 올 인을 하여 콜 혹은 다이만 가능합니다.")
                self.bt_die.config(state='active', bg=btcolor)
                self.bt_call.config(state='active', bg='green')
            elif 0 <= com.money < 1000000:
                self.show_message(0, "COM의 소지금이 적어 콜 혹은 다이만 가능합니다.")
                self.bt_die.config(state='active', bg=btcolor)
                self.bt_call.config(state='active', bg='green')
            else:
                self.show_message(0, '배팅을 진행합니다.')
                self.show_message(1, game.p_rank_name)
                self.bt_die.config(state='active', bg=btcolor)
                self.bt_call.config(state='active', bg='green')
                self.bt_ddadang.config(state='active', bg=btcolor)
                self.bt_half.config(state='active', bg=btcolor)
                self.bt_full.config(state='active', bg=btcolor)
                self.bt_all_in.config(state='active', bg=btcolor)
        elif side == 2: ##봇이 배팅하는 경우 봇 함수를 실행시킨다
            game.side = 2
            time.sleep(1)
            self.show_message(0, 'COM이 배팅을 시작합니다.')
            time.sleep(1)
            self.show_message(0, 'COM이 선택 중입니다...')
            time.sleep(3)
            bet.ai_bot(1)


    def die(self):
        self.disabling_all()
        canvas.delete(self.bettxt_p1)
        game.winner = 2
        self.show_message(0, '다이를 선택하셨습니다.')
        self.close_money()

    def check(self):
        if player.money < 1000000:
            self.show_message(0, '플레이어의 소지금이 부족하여 기본배팅 없이 진행합니다.')
        elif com.money < 1000000:
            self.show_message(0, 'COM의 소지금이 적어 기본배팅 없이 진행합니다.')
        else:
            player.bet_amount = 1000000
            self.money_betted += player.bet_amount
            player.money -= player.bet_amount
            com.bet_amount = 1000000
            self.money_betted += player.bet_amount
            com.money -= com.bet_amount

    def call(self):
        canvas.delete(self.bettxt_p1)
        if player.money < com.bet_amount:
            self.disabling_all()
            self.show_message(0, '소지금이 부족하여 올 인합니다.')
            player.bet_amount = player.money
            self.bet_money(1)
        else:
            self.disabling_all()
            self.show_message(0, "콜을 선택하셨습니다.")
            player.bet_amount = com.bet_amount
            self.bet_money(1)
        canvas.delete(self.bettxt_p1)
        game.get_winner()

    def ddadang(self):
        canvas.delete(self.bettxt_p1)
        btcolor = 'Dim Gray'
        if player.money < com.bet_amount*2:
            self.show_message(0, '소지금이 부족합니다.')
            self.bt_ddadang.config(state='disable', bg=btcolor)
        else:
            self.disabling_all()
            self.show_message(0, '따당을 선택하셨습니다.')
            player.bet_amount = com.bet_amount * 2
            self.bet_money(1)
            self.bet_next(2)

    def half(self):
        canvas.delete(self.bettxt_p1)
        btcolor = 'Dim Gray'
        if (
                (com.bet_amount + (self.money_betted // 2)) -
                ((com.bet_amount + (self.money_betted // 2)) % 10000) > player.money
        ):
            self.show_message(0, '소지금이 부족합니다.')
            self.bt_half.config(state='disable', bg=btcolor)
        else:
            self.disabling_all()
            self.show_message(0, '하프를 선택하셨습니다.')
            player.bet_amount = (com.bet_amount + (self.money_betted // 2)) - \
                                ((com.bet_amount + (self.money_betted // 2)) % 10000)
            self.bet_money(1)
            self.bet_next(2)

    def full(self):
        canvas.delete(self.bettxt_p1)
        btcolor = 'Dim Gray'
        if player.p_betted + player.money >= 1000000000:
            player.bet_amount = 1000000000 - player.p_betted
            self.disabling_all()
            self.show_message(0, '풀을 선택하셨습니다.')
            self.bet_money(1)
            self.bet_next(2)
        else:
            self.show_message(0, '배팅 총액이 10억 이하입니다.')
            self.bt_full.config(state='disable', bg=btcolor)

    def all_in(self):
        canvas.delete(self.bettxt_p1)
        btcolor = 'Dim Gray'
        if player.money > com.money:
            self.show_message(0, 'COM의 소지금이 부족합니다.')
            self.bt_all_in.config(state='disable', bg=btcolor)
        else:
            self.disabling_all()
            self.show_message(0, '올 인을 선택하셨습니다.')
            player.bet_amount = player.money
            self.bet_money(1)
            self.bet_next(2)

    def manual(self):
        player.bet_amount = self.var_manual.get()
        if player.money - player.bet_amount < 0:
            self.show_message(0, '소지금이 부족합니다.')
            self.show_message(0, '다시 선택해주세요.')
        else:
            self.disabling_all()
            canvas.delete(self.bettxt_p1)
            self.bet_money(1)
            self.bet_next(2)


    def show_bet_button(self):
        # 베팅버튼 공통좌표
        bet_b_x = 200
        bet_b_y = 435
        btw_bet_b = 50
        btcolor1 = 'Dim Gray'
        btcolor2 = 'orange'

        # fold button
        self.bt_die = Button(root, text="다이", state='disabled', \
          command=lambda: self.die(), width = 5, height = 3, bd = 3, \
          bg=btcolor1, activebackground=btcolor2)
        self.bt_die.pack()
        self.bt_die.place(relx=(bet_b_x + btw_bet_b*0) / table_width, \
          rely=bet_b_y / table_height)

        # call button
        self.bt_call = Button(root, text="콜", state='disabled', \
          command=lambda: self.call(), width = 5, height = 3, bd = 3, \
          bg=btcolor1, activebackground='green')
        self.bt_call.pack()
        self.bt_call.place(relx=(bet_b_x + btw_bet_b*1) / table_width, \
          rely=bet_b_y / table_height)

        # ddadang button
        self.bt_ddadang = Button(root, text="따당", state='disabled', \
          command=lambda: self.ddadang(), width=5, height=3, bd=3, \
          bg=btcolor1, activebackground=btcolor2)
        self.bt_ddadang.pack()
        self.bt_ddadang.place(relx=(bet_b_x + btw_bet_b*3) / table_width, \
          rely=bet_b_y / table_height)

        # half button
        self.bt_half = Button(root, text="하프", state='disabled', \
          command=lambda: self.half(), width=5, height=3, bd=3, \
          bg=btcolor1, activebackground=btcolor2)
        self.bt_half.pack()
        self.bt_half.place(relx=(bet_b_x + btw_bet_b*4) / table_width, \
          rely=bet_b_y / table_height)

        # all in button
        self.bt_all_in = Button(root, text="올 인", state='disabled', \
          command=lambda: self.all_in(), width=5, height=3, bd=3, \
          bg=btcolor1, activebackground=btcolor2)
        self.bt_all_in.pack()
        self.bt_all_in.place(relx=(bet_b_x + btw_bet_b * 6) / table_width, \
                           rely=bet_b_y / table_height)

        # full button
        self.bt_full = Button(root, text="풀", state='disabled', \
          command=lambda: self.full(), width=5, height=3, bd=3, \
          bg=btcolor1, activebackground=btcolor2)
        self.bt_full.pack()
        self.bt_full.place(relx=(bet_b_x + btw_bet_b*5) / table_width, \
          rely=bet_b_y / table_height)



        # first betting
        self.var_manual = IntVar()
        self.scale = Scale(root, from_=1000000, to=30000000,
                           resolution=100000,\
                           variable=self.var_manual, orient=HORIZONTAL, \
                           length=110, bd=0, relief='groove', bg=btcolor1, \
                           troughcolor=btcolor1)
        self.scale.pack()
        self.scale.place(relx=(bet_b_x + btw_bet_b * 7.2) / table_width, \
                         rely=bet_b_y / table_height)
        self.bt_manual = Button(root, text="선 배팅", state='disabled', \
                                command=lambda: self.manual(), width=6, height=3, bd=3, \
                                bg=btcolor1, activebackground=btcolor2)
        self.bt_manual.pack()
        self.bt_manual.place(relx=(bet_b_x + btw_bet_b * 9.6) / table_width, \
                             rely=bet_b_y / table_height)

    def disabling_all(self):
        btcolor = 'Dim Gray'
        self.bt_die.config(state = 'disabled', bg = btcolor)
        self.bt_call.config(state = 'disabled', bg = btcolor)
        self.bt_half.config(state = 'disabled', bg = btcolor)
        self.bt_full.config(state = 'disabled', bg = btcolor)
        self.bt_ddadang.config(state = 'disabled', bg = btcolor)
        self.bt_all_in.config(state='disabled', bg=btcolor)
        self.scale.config(bg = btcolor, troughcolor = btcolor)
        self.bt_manual.config(state = 'disabled', bg = btcolor)


    def close_money(self):
        canvas.delete(self.bettxt_p1)
        if game.winner == 1 and game.draw == 0:
            player.money += self.money_betted
        elif game.winner == 2 and game.draw == 0:
            com.money += self.money_betted
        canvas.delete(self.bettxt_p1)
        if game.draw == 1:
            player.p_betted = 0
            com.c_betted = 0
            game.draw = 0
            self.show_chips()
            delete_photo_txt()
            root.after(1500, setNextGame())
        else:
            self.money_betted = 0
            player.p_betted = 0
            com.c_betted = 0
            game.draw = 0
            threads = []
            threads.append(threading.Thread(target=self.show_chips()))
            threads.append(threading.Thread(target=play_cash_sound))
            threads[0].start()
            threads[1].start()
            for th in threads:
                th.join()
            delete_photo_txt()
            root.after(1500, setNextGame())


bet = Bet()

def setNextGame():
    global next_game
    next_game = True

def getNextGame():
    if not next_game:
        return True
    else:
        return False

def updating_root():
    root.update_idletasks()
    root.update()

def delete_photo_txt():
    for x in range(2):
        canvas.delete(deck.player_slot[x])
        canvas.delete(deck.com_slot[x])


# 메뉴바
menubar = Menu(root)
contents = Menu_contents()
gamemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="파일", menu=gamemenu)
gamemenu.add_command(label="불러오기", command=contents.load)
gamemenu.add_command(label="저장", command=contents.save)
gamemenu.add_command(label='랭킹', command=contents.rank)
gamemenu.add_separator()
gamemenu.add_command(label="나가기", command=root.destroy)

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="도움말", menu=helpmenu)
helpmenu.add_command(label="섯다 족보", command=contents.seotta_hands)
helpmenu.add_command(label="배팅", command=contents.betting)

infomenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="정보", menu=infomenu)
infomenu.add_command(label="섯다 COM은...", command=contents.seotta_bot)
infomenu.add_command(label="5조에 대해...", command=contents.about)

root.config(menu=menubar)

background = PhotoImage(file='table.gif')
bg = canvas.create_image(0, 0, anchor=NW, image=background)
root.update()

try:
    with open('save.pkl', 'rb') as f:
        unpickled_file = pickle.load(f)
    sorted_rank = unpickled_file[-1]
    rank = unpickled_file[-2]
except:
    rank = {}
    sorted_rank = {}

deck.__init__()

for x in deck.cards:
    deck.card_images.append(PhotoImage(file=image_path(x)))
random.shuffle(deck.cards)  ##카드 1~20 (광은 11~20 에 포함)
b1fv_image = PhotoImage(file='b1fv.png')

deck_image = []  # 덱표시(뒷장)에 사용될 전역변수 생성
deck_place = []  # 덱 이미지(뒷장)의 x좌표값을 기록하는 전역변수 생성

show_deck_image()
play_deck_sound()

while True:
    next_game = False

    # 덱이 비었을 경우 다시 카드를 채워준다.
    if deck.cards == []:
        for i in range(20):
            deck.cards.append(i+1)
        random.shuffle(deck.cards)

    #둘 중 한 쪽의 소지금이 0원이 되었을 때 게임을 완전히 종료한다.
    if player.money == 0:
        play_lose_sound()
        bet.show_message(0, '패배하였습니다.')
        bet.show_message(0, '플레이 해 주셔서 감사합니다.')
        bet.show_message(0, '3초 후 창이 닫힙니다.')
        time.sleep(2)
        sys.exit()
    elif com.money == 0:
        play_win_sound()
        bet.show_message(0, '승리하였습니다!')
        bet.show_message(0, '플레이 해 주셔서 감사합니다.')
        bet.show_message(0, '3초 후 창이 닫힙니다.')
        time.sleep(2)
        sys.exit()

    game.set()

    deck.player_cards = [player.card1, player.card2]
    deck.com_cards = [com.card1, com.card2]

    show_player_cards()
    show_com_cards()

    bet.check()
    bet.show_chips()

    bet.bet_first(game.winner)

    # 화면을 계속해서 업데이트 해주는 sub loop
    while getNextGame():
        try:
            root.after(5, updating_root())
        except:
            quit()

    continue  # 다시 main loop의 처음으로 돌아감