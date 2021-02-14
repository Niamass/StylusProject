import cv2
import numpy as np
size = 20
X = 200
Y = 100
mode = False
#ищет два вектора цвета в квадратике(это буквально квадрат)
def find_all_colors(img):
    min_color = [255, 255, 255]
    max_color = [0, 0, 0]
    # мне кажется, тут можно написать и короче. Я не знаток питона :(. тогда мб функция не нужна
    for i in range(Y, Y + size):
        for j in range(X, X + size):
            for k in range(3):
                min_color[k] = min(img[i][j][k], min_color[k])
                max_color[k] = max(img[i][j][k], min_color[k])
    return min_color, max_color

#ищет точку(пиксель) на "хитрой" сетке. её как-то сократить надо, видео тормозит или мб __CUDA__ попробовать
def find_point(img):
    for i in range(len(img) // (size // 2)):  # y
        for j in range(len(img[0]) // (size // 2)):  # x
            # может и тут какой-то питоновский трюк можно провернуть, то что ниже в комментах не работает. Я пыталась сравнить два массива по-быстрому
            # ind = np.where(min_color <= img[i][j] <= max_color)
            # k = (min_color <= img[i][j] <= max_color)
            if (min(img[i][j] - min_color) >= 0) and (min(max_color - img[i][j]) >= 0):
                return i,j

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    start_point = (X-1, Y-1)
    end_point = (X + size+1, Y + size+1)
    color = (255, 0, 0)
    thickness = 1
    if mode == False:
        img = cv2.rectangle(img, start_point, end_point, color, thickness)
    cv2.imshow("Cam", img)
    # here something like: "place the item(?) in the circle and qlick "q""//To define a marker//что-то типа калибровки, но как это в КЗ называется - пас
    if cv2.waitKey(10) == ord('q'):#на самом деле я просто других укв не знаю//посмотреть другие буквы//возможно стоит калибровать на нескольких кадрах, там даже так погрешность большая что-то
        #тут надо найти максимальную разность цветов//вернуть 2 RGB
        min_color, max_color = find_all_colors(img)
        mode = True
    if (mode):
        #тут надо найти маркер (квардатик size x size, точку) я думаю на сетке, но хитрой. Там вроде алгоритмы есть, но читать книжку на 700 стр я не собираюсь. да и та бесполезна, если смотреть на содержание
        x,y = find_point(img) #возвращает какую-то точку на сетке, т.е. надо ещё сам квадрат-маркер найти и усреднить координату
        #Ну, наверное, точку сохранить в массив и строить линии в cv2.line()
        #возможно эта штука по шустрее будет (видео не будет подвисать), если добавить "спираль" или что-то похожее, чтобы искать рядом. Мб какойто "звёздочкой"
    if cv2.waitKey(10) == 27: # Клавиша Esc? А как по крестику выходить? Всё ещё актуально
        break
    if not cv2.getWindowProperty('Cam', 0) >= 0:
        break

cap.release()
cv2.destroyAllWindows()
#FindMask - функция получает изображение и цвет который надо найти, строит сетку и возвращает координаты. Тут шум мб проблема. КАК ОКАЗАЛОСЬ это глобальная проблема
#FindAllObj - функция получает цвет и координату пикселя и смотрит есть ли такие же пиксели вокруг, возвращает двумерный массив
#Из этого двумерного массива достать среднее значение координату - сохранить в массив точек(?)// можно не усреднять, а просто переносить
# соеденить точки вектором, напечатать куда-то //нарисовать линию. line(x1,y1,x2,y2)
#Найди рядом пиксели. функция проверяет цвет текущего пикселя или ищет рядом по спирали(...) FindAllObj снова 
