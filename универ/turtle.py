import turtle

def apply_rules(ch):
    if ch == 'X':
        return 'X+YF+'
    elif ch == 'Y':
        return '-FX-Y'

def expand_rules(s, iterations):
    for _ in range(iterations):
        s = ''.join([apply_rules(ch) for ch in s])
    return s

def draw_dragon_curve(s, length, angle):
    for ch in s:
        if ch == 'F':
            turtle.forward(length)
        elif ch == '-':
            turtle.right(angle)
        elif ch == '+':
            turtle.left(angle)

# Настройки для отображения
turtle.speed(0)
turtle.penup()
turtle.goto(-200, 0)
turtle.pendown()

# Исходная строка и количество итераций
start = "FX"
iterations = 10

# Разворачиваем L-систему
dragon_str = expand_rules(start, iterations)

# Рисуем кривую дракона
draw_dragon_curve(dragon_str, 5, 90)

# Завершение работы
turtle.done()