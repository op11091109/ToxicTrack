import turtle, time
import pygame
from random import *

# 배경 설정
scr = turtle.Screen()
scr.setup(1700, 1000)
scr.bgpic("fieldrace.gif")
scr.title("🏇 Horse Racing Game")

# 말 이미지 등록
horses = ["1hor.gif", "2hor.gif", "3hor.gif", "4hor.gif", "5hor.gif", "6hor.gif"]
for h in horses:
    scr.addshape(h)

# 말 객체 생성 및 배치
start_x = -280
start_y = [150, 100, 50, 0, -50, -100]
bets = [2, 5, 8, 16, 18, 23]
colors = ["빨강", "주황", "노랑", "초록", "파랑", "보라"]

horses_turtle = []
for i in range(6):
    t = turtle.Turtle()
    t.up()
    t.goto(start_x, start_y[i])
    t.shape(horses[i])
    horses_turtle.append(t)


# UI 출력용 터틀 생성
ui = turtle.Turtle()
ui.hideturtle()
ui.penup()


def update_ui(money, choice, message):
    ui.clear()
    ui.goto(450, 200)
    ui.write(f"💰 잔액: {money}칩", font=("Arial", 18, "bold"))
    ui.goto(450, 160)
    if choice:
        ui.write(f"📍 베팅: {choice}번 말 ({colors[choice - 1]})", font=("Arial", 16, "normal"))
    else:
        ui.write(f"📍 베팅: 없음", font=("Arial", 16, "normal"))
    ui.goto(450, 120)
    ui.write(message, font=("Arial", 14, "normal"))


# 게임 루프
money = 10000
while True:
    update_ui(money, None, "💬 베팅할 말을 선택해주세요!")

    choice_str = turtle.textinput("베팅하기", "몇 번 말에 베팅하시겠습니까? (1~6)")
    if not choice_str:
        update_ui(money, None, "🛑 게임을 종료합니다.")
        break  # 창을 닫으면 종료

    if not choice_str.isdigit() or int(choice_str) not in range(1, 7):
        update_ui(money, None, "⚠️ 1~6 사이의 숫자를 입력해주세요.")
        continue

    choice = int(choice_str)
    update_ui(money, choice, "🏁 경주를 시작합니다!")

    pygame.mixer.init()
    pygame.mixer.music.load("startcall.mp3")
    pygame.mixer.music.play()

    time.sleep(3)

    # 말 속도 설정
    step_mods = [5,
                 randint(4, 7),
                 randint(3, 9),
                 randint(3, 10),
                 randint(2, 11),
                 randint(1, 12)]

    while all(h.xcor() < 280 for h in horses_turtle):
        horses_turtle[0].forward(5)
        for i in range(1, 6):
            horses_turtle[i].forward(randint(1, step_mods[i]))

    final_positions = [h.xcor() for h in horses_turtle]
    sorted_positions = sorted(final_positions, reverse=True)

    if final_positions[choice - 1] == sorted_positions[0]:
        win_amount = bets[choice - 1] * 1000
        money += win_amount
        update_ui(money, choice, f"🎉 {choice}번 말이 우승! +{win_amount}칩")
    else:
        money -= 1000
        update_ui(money, choice, "😭 베팅 실패! -1000칩")

    time.sleep(1)

    for i, h in enumerate(horses_turtle):
        h.goto(start_x, start_y[i])

    if money <= 0:
        update_ui(0, None, "💀 파산하셨습니다.")
        break

