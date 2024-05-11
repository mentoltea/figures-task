import pygame
from random import randint as rnd
import math
import webbrowser

#ДОКУМЕНТАЦИЯ МОДУЛЯ graph
#для инициализации или реинициализации (сброса) используется init(). он обязателен, поскольку определяет размер окна. размер окна можно задать вручную, по умолчанию определяется автоматически
#graph() - отрисовывает график задаваемой функции, обязательный аргумент - функция
#sequense() - отрисовывает последовательность точек, обязательный аргумент - список из точек вида (x,y)
#done() - возвращает отрисовываемую поверхность класса pygame.Surface
#set_background_color() - изменяет цвет фона. влияет на цвет всех текстов
#show() - открывает окно с отрисованной поверхностью
#hide() - закрывает окно с отрисованной поверхностью
#
# init() -> graph()/sequense() -> [graph()/sequense() -> ... ] -> done() -> [init() -> ... ]
#
#ДОПОЛНИТЕЛЬНЫЕ ПАРАМЕТРЫ ФУНКЦИЙ graph() И sequense()
#accuranse - точность. количество кусочков, на который делится каждый единичный отрезок оси X. по умолчанию 10. только для функции graph() 
#x_left, x_right - соответственно левая и правая границы оси X. по умолчанию равны -10 и 10. только для функции graph() 
#lines - соединяются ли точки при отображении между собой. для graph() по умолчанию True, для sequense() - False
#radius - радиус точек при точечном отображении (lines = False). для graph() по умолчанию 1, для sequense() - 3
#color - цвет точек/линий
#name - имя графика. по умолчанию отсутствует
#name_legend - отображение имени графика в левом нижнем углу. иначе отображение у правой границы. автоматически работает, если значение в правой границе отсутствует. по умолчанию False
#proportions - сохраняются ли пропорции осей X и Y. если включено, то 1 единичному отрезку на одной оси соответствует отрезок той же длины на второй. по умолчанию False
#x_legend - отображение значений левой и правой границ на оси. по умолчанию False
#y_legend - отображение максимального и минимального значания графика на оси. по умолчанию False
#legend - отображение данных двух предыдущих пунктов в левом верхнем углу. по умолчанию False
#
#
#
#
#P.S.: это просто небольшой проект автора для тренировки или любительского баловства. для серьёзного подхода рекомендую использовать matplotlib или иные библиотеки


KOEF = 0.6
RES_FORMAT = None
window = None
centre = None
back_color = (255,255,255)
back_opp_color = (0,0,0)
pygame.init()

def draw_text(text, x, y, size, surf = window, font = 'timesnewroman', color=(0,0,0)):
    window.blit(pygame.font.Font(pygame.font.match_font('timesnewroman'), size).render(text,True,color), (x,y))

def init(RES_FORM = [min(pygame.display.get_desktop_sizes()[0])*KOEF]*2 ):
    global window, RES_FORMAT, centre, back_color, back_opp_color
    
    window = pygame.Surface((RES_FORM[0], RES_FORM[1]))
    window.fill((255, 255, 255))
    centre = list(map(lambda val: val//2, RES_FORM))
    RES_FORMAT = RES_FORM
    pygame.draw.line(window, back_opp_color, (centre[0],0), (centre[0],RES_FORMAT[1]))
    pygame.draw.line(window, back_opp_color, (0, centre[1]), (RES_FORMAT[0], centre[1]))
    draw_text("x", RES_FORMAT[0]-10, centre[1], 15, window, color=back_opp_color)
    draw_text("y", centre[0]+10, 10, 15, window, color=back_opp_color)

def set_background_color(color):
    global window, RES_FORMAT, centre, back_color, back_opp_color
    window.fill(color)
    opp_color = list(map(lambda x: 255-x, color))
    pygame.draw.line(window, opp_color, (centre[0],0), (centre[0],RES_FORMAT[1]))
    pygame.draw.line(window, opp_color, (0, centre[1]), (RES_FORMAT[0], centre[1]))

    draw_text("x", RES_FORMAT[0]-10, centre[1], 15, window, color=opp_color)
    draw_text("y", centre[0]+10, 10, 15, window, color=opp_color)

    back_opp_color = opp_color
    back_color = color

def graph(function,
          accuranse=10,
          x_left=-10, x_right=10,
          lines=True,
          radius=1,
          color=(rnd(2,255),rnd(2,255),rnd(2,255)),
          name=None,
          name_legend=0,
          proportions=0,
          x_legend=0,
          y_legend=0,
          legend=0):
    global window, RES_FORMAT, centre, back_color, back_opp_color

    if window==None or RES_FORMAT==None or centre == None:
        raise Exception("Модуль не инициализирован - попробуйте добавить init()")
    
    if x_left>x_right:
        x_left, x_right = x_right, x_left
        
    fin_points = []
    max_y = -float('inf')
    min_y = float('inf')
    
    for x in range(x_left*accuranse, (x_right+1)*accuranse):
        try:
            func_value = function(x/accuranse)

            max_y = max(max_y, func_value)
            min_y = min(min_y, func_value)
            
            fin_points.append( (x/accuranse, func_value) ) #точка (х,у)
        except:
            fin_points.append( (x/accuranse, None) )

    
    
    if max_y == -float('inf') or min_y == float('inf'):
        raise Exception("Функция не имеет смысла - не существует каких-либо значений")

    max_x = x_right
    min_x = x_left
    
    delta_x = x_right - x_left
    delta_y = max_y - min_y
    
    if delta_y==0:
        delta_y=abs(max_y)
    if delta_y<abs(max_y):
        delta_y=abs(max_y)

    if delta_x==0:
        delta_x=abs(max_x)
    if delta_x<abs(max_x):
        delta_x=abs(max_x)

    delta_max = max(delta_x, delta_y)

    
    if proportions:
        RES_FORM = [int(min(RES_FORMAT)*0.8)]*2
        delta_x, delta_y = delta_max, delta_max
    else:
        #RES_FORM = RES_FORMAT
        RES_FORM = list(map(lambda val: int(val*0.8), RES_FORMAT))
    

    last_point = None
    for point in fin_points:
        if lines:
            #для гладких графиков
            if point == None or point[1] == None:
                last_point=None
                continue
            
            real_x = int(centre[0] + point[0]/delta_x *RES_FORM[0]/2)
            real_y = int(centre[1] - point[1]/delta_y *RES_FORM[1]/2)

            real_point = (real_x, real_y)
            
            if last_point!= None:
                pygame.draw.line(window, color, last_point, real_point)

            last_point = real_point

        else:
            #для точечных графов
            if point == None or point[1] == None:
                last_point=None
                continue
            
            real_x = int(centre[0] + point[0]/delta_x *RES_FORM[0]/2)
            real_y = int(centre[1] - point[1]/delta_y *RES_FORM[1]/2)

            real_point = (real_x, real_y)
            
            pygame.draw.circle(window, color, real_point, radius)
            
    
    
    if x_legend:
        draw_text(str(round(x_right,2)), int(centre[0] + x_right/delta_x *RES_FORM[0]/2), centre[1], 15, window, color=back_opp_color)
        draw_text(str(round(x_left,2)), int(centre[0] + x_left/delta_x *RES_FORM[0]/2), centre[1], 15, window, color=back_opp_color)

    if y_legend:    
        draw_text(str(round(max_y,2)), centre[0], int(centre[1] - max_y/delta_y *RES_FORM[1]/2) - 15, 15, window, color=back_opp_color)
        draw_text(str(round(min_y,2)), centre[0], int(centre[1] - min_y/delta_y *RES_FORM[1]/2), 15, window, color=back_opp_color)

    if legend:
        draw_text("x min= {}".format(round(x_left,4)), 10, 10, 15, window, color=back_opp_color)
        draw_text("x max= {}".format(round(x_right,4)), 10, 25, 15, window, color=back_opp_color)
        draw_text("y min= {}".format(round(min_y,4)), 10, 55, 15, window, color=back_opp_color)
        draw_text("y max= {}".format(round(max_y,4)), 10, 70, 15, window, color=back_opp_color)

    if name!=None:
        if name_legend:
            pygame.draw.rect(window, color, (10, RES_FORMAT[1]-20, 10, 10))
            draw_text(name, 30, RES_FORMAT[1]-25 , 15, window, color=color)
        else:
            try:
                draw_text(name, int(centre[0] + x_right/delta_x *RES_FORM[0]/2), int(centre[1] - function(x_right)/delta_y *RES_FORM[1]/2), 15, window, color=color)
            except:
                pygame.draw.rect(window, color, (10, RES_FORMAT[1]-20, 10, 10))
                draw_text(name, 30, RES_FORMAT[1]-25 , 15, window, color=color)
    
def sequense(seq,
             lines=False,
             radius=3,
             color=(rnd(2,255),rnd(2,255),rnd(2,255)),
             name=None,
             proportions=0,
             x_legend=0,
             y_legend=0,
             legend=0):
    global window, RES_FORMAT, centre, back_color, back_opp_color

    if window==None or RES_FORMAT==None or centre == None:
        raise Exception("Модуль не инициализирован - попробуйте добавить init()")

    max_x = -float('inf')
    max_y = -float('inf')
    min_x = float('inf')
    min_y = float('inf')
    for element in seq:
        if 1:#try:
            if len(element)==2:
                if None not in element:
                    max_x = max(max_x, element[0])
                    min_x = min(min_x, element[0])
                    
                    max_y = max(max_y, element[1])
                    min_y = min(min_y, element[1])
                    
        else:#except:
            text = "Последовательность содержит невозможные для отображения элементы - {0}. Все элементы должны представлять собой списки/кортежы длиной 2 (x, y)".format(str(element))
            raise Exception(text)

    if float('inf') in [abs(max_x), min_x, abs(max_y), min_y]:
        raise Exception("Последовательность не имеет смысла - не существует каких-либо значений")
    x_right, x_left = max_x, min_x
    
    delta_x = max_x - min_x
    delta_y = max_y - min_y

    if delta_y==0:
        delta_y=abs(max_y)
    if delta_y<abs(max_y):
        delta_y=abs(max_y)

    if delta_x==0:
        delta_x=abs(max_x)
    if delta_x<abs(max_x):
        delta_x=abs(max_x)
    
    delta_max = max(delta_x, delta_y)

    
    if proportions:
        RES_FORM = [int(min(RES_FORMAT)*0.8)]*2
        delta_x, delta_y = delta_max, delta_max
    else:
        RES_FORM = list(map(lambda val: int(val*0.8), RES_FORMAT))
    

    last_point = None
    for point in seq:
        if lines:
            #для гладких графиков
            if point == None or point[1] == None:
                last_point=None
                continue
            
            real_x = int(centre[0] + point[0]/delta_x *RES_FORM[0]/2)
            real_y = int(centre[1] - point[1]/delta_y *RES_FORM[1]/2)

            real_point = (real_x, real_y)
            
            if last_point!= None:
                pygame.draw.line(window, color, last_point, real_point)

            last_point = real_point

        else:
            #для точечных графов
            if point == None or point[1] == None:
                last_point=None
                continue
            
            real_x = int(centre[0] + point[0]/delta_x *RES_FORM[0]/2)
            real_y = int(centre[1] - point[1]/delta_y *RES_FORM[1]/2)

            real_point = (real_x, real_y)
            
            pygame.draw.circle(window, color, real_point, radius)
            
    if x_legend:
        draw_text(str(round(x_right,2)), int(centre[0] + x_right/delta_x *RES_FORM[0]/2), centre[1], 15, window, color=back_opp_color)
        draw_text(str(round(x_left,2)), int(centre[0] + x_left/delta_x *RES_FORM[0]/2), centre[1], 15, window, color=back_opp_color)

    if y_legend:    
        draw_text(str(round(max_y,2)), centre[0], int(centre[1] - max_y/delta_y *RES_FORM[1]/2) - 15, 15, window, color=back_opp_color)
        draw_text(str(round(min_y,2)), centre[0], int(centre[1] - min_y/delta_y *RES_FORM[1]/2), 15, window, color=back_opp_color)

    if legend:
        draw_text("x min= {}".format(round(x_left,4)), 10, 10, 15, window, color=back_opp_color)
        draw_text("x max= {}".format(round(x_right,4)), 10, 25, 15, window, color=back_opp_color)
        draw_text("y min= {}".format(round(min_y,4)), 10, 55, 15, window, color=back_opp_color)
        draw_text("y max= {}".format(round(max_y,4)), 10, 70, 15, window, color=back_opp_color)

    if name!=None:
        pygame.draw.rect(window, color, (10, RES_FORMAT[1]-20, 10, 10))
        draw_text(name, 30, RES_FORMAT[1]-25 , 15, window, color=color)


def done(): 
    global window
    return window

def save(filename="out"):
    global window
    pygame.image.save(window, f"{filename}.png")
    #webbrowser.open(f"{filename}.png")

def show():
    global window, RES_FORMAT
    
    win = pygame.display.set_mode(RES_FORMAT)
    win.blit(window, (0,0))
    pygame.display.update()


def hide():
    pygame.display.quit()
