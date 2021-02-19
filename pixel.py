import cv2
import numpy as np
size = 20
X = 200
Y = 100
mode = False


def find_min_coomp(vec1, vec2):
    for i in range(len(vec1)):
        vec1[i] = min(vec1[i], vec2[i])
    return vec1
def find_max_coomp(vec1, vec2):
    for i in range(len(vec1)):
        vec1[i] = max(vec1[i], vec2[i])
    return vec1
def subtract_vectors(v, w):
    res =3*255
    for i in range(len(v)):
        res = min(res, int(v[i])-int(w[i]))
    return res

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

#ищет точку(пиксель)
def find_point(img, min_color, max_color):
    for i in range(len(img) // (size // 15)):  # y
        for j in range(len(img[0]) // (size // 15)):  # x
            # может и тут какой-то питоновский трюк можно провернуть, то что ниже в комментах не работает. Я пыталась сравнить два массива по-быстрому
            # ind = np.where(min_color <= img[i][j] <= max_color)
            # k = (min_color <= img[i][j] <= max_color)

            if ((subtract_vectors(img[i][j], min_color)) >= 0) and ((subtract_vectors(max_color, img[i][j])) >= -100):

                return i,j
    return -1,-1

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
x_vec = []
y_vec = []
min_color = [255, 255, 255]
max_color = [0, 0, 0]
f = 0
while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    start_point = (X-1, Y-1)
    end_point = (X + size+1, Y + size+1)
    color = (255, 0, 0)
    thickness = 1
    if mode == False:
        img = cv2.rectangle(img, start_point, end_point, color, thickness)

    # here something like: "place the item(?) in the circle and qlick "q""//To define a marker//что-то типа калибровки, но как это в КЗ называется - пас
    if cv2.waitKey(10) == ord('a'):#на самом деле я просто других укв не знаю//посмотреть другие буквы//возможно стоит калибровать на нескольких кадрах, там даже так погрешность большая что-то
        #тут надо найти максимальную разность цветов//вернуть 2 RGB
        min_color1, max_color1 = find_all_colors(img)
        min_color = find_min_coomp(min_color,min_color1)
        max_color = find_max_coomp(max_color,max_color1)
        f+=1
        if f== 1:
            mode = True
    if (mode):
        #тут надо найти маркер (квардатик size x size, точку) я думаю на сетке
        x,y = find_point(img,min_color, max_color) #возвращает какую-то точку на сетке, т.е. надо ещё сам квадрат-маркер найти и усреднить координату
        print(x,y)
        x_vec.append(x)
        y_vec.append(y)
        for i in range(1,len(x_vec)):
            if (len(x_vec) == 1):
                break
            img = cv2.line(img, (x_vec[i-1], y_vec[i-1]), (x_vec[i], y_vec[i]), [255, 0, 0], 2)
        #Ну, наверное, точку сохранить в массив и строить линии в cv2.line()
        #возможно эта штука по шустрее будет (видео не будет подвисать), если добавить "спираль" или что-то похожее, чтобы искать рядом. Мб какойто "звёздочкой"
    cv2.imshow("Cam", img)
    if cv2.waitKey(10) == 27: # Клавиша Esc
        break
    if  not cv2.getWindowProperty('Cam', 0) >= 0:
        break

cap.release()
cv2.destroyAllWindows()
#FindMask - функция получает изображение и цвет который надо найти, строит сетку и возвращает координаты. Тут шум мб проблема. КАК ОКАЗАЛОСЬ это глобальная проблема
#FindAllObj - функция получает цвет и координату пикселя и смотрит есть ли такие же пиксели вокруг, возвращает двумерный массив
#Из этого двумерного массива достать среднее значение координату - сохранить в массив точек(?)// можно не усреднять, а просто переносить
# соеденить точки вектором, напечатать куда-то //нарисовать линию. line(x1,y1,x2,y2)
#Найди рядом пиксели. функция проверяет цвет текущего пикселя или ищет рядом по спирали(...) FindAllObj снова 
