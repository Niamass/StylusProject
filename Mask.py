import cv2
import numpy as np

# обработка изображения с маркером, современная обработка изображений
# ик камера
# обмен симвоолами, первый спринт + документация алгоритмов. как выбирать алг, фильтры
# linka, ,kfujhjlyfz wtkm ? или развлекалово
# user requirement

size = 20  # ребро квадрата-считывателя
# асположение квадрата
X = 200
Y = 100
# режим работы калибровка/рисование (мб и больше будет)
mode = False
# погрешность
eps = 0

# вычисляет min/max комполенты двых цветов-векторов
def find_min_coomp(vec1, vec2):
    for i in range(len(vec1)):
        vec1[i] = min(vec1[i], vec2[i])
    return vec1
def find_max_coomp(vec1, vec2):
    for i in range(len(vec1)):
        vec1[i] = max(vec1[i], vec2[i])
    return vec1

# ищет два вектора цвета на маркере
def find_all_colors(img, X, Y): #картинка и верхрий левый угол квадрата, в котором искать цвета
    min_color = [255, 255, 255]
    max_color = [0, 0, 0]
    # мне кажется, тут можно написать и короче
    for i in range(Y, Y + size):
        for j in range(X, X + size):
            for k in range(3):
                min_color[k] = min(img[i][j][k], min_color[k])
                if min_color[k] >= eps:
                    min_color[k] -= eps
                max_color[k] = max(img[i][j][k], min_color[k])
                if max_color[k] <= 255 - eps:
                    max_color[k] += eps
    return min_color, max_color

def Calibration(wimdow_name, cap):
    min_color = [255, 255, 255]
    max_color = [0, 0, 0]
    i = 0
    j = 0
    count_col = 0
    #for for for|| while while while
    while (i < 2 and j < 2):
        flag, imgtmp = cap.read()
        for k in range(3):
            start_point = (i* len(imgtmp[0]) + ((-1)**i)*(X - 1),j * len(imgtmp) +((-1)**j)*(Y - 1))
            end_point = (start_point[0] + size + 1, start_point[1]  + size + 1)
            color = (255, 0, 0)
            thickness = 1

            img = cv2.rectangle(imgtmp, start_point, end_point, color, thickness)
            cv2.imshow(wimdow_name, imgtmp)

            if cv2.waitKey(10) == ord('a'):
                # найти макaсимальную разность цветов//вернуть 2 RGB//запихнуть в одну функцию-файл
                min_color1, max_color1 = find_all_colors(img, start_point[0]+1, start_point[1]+1)#???
                min_color = find_min_coomp(min_color, min_color1)
                max_color = find_max_coomp(max_color, max_color1)
                #много ифов для i j
                count_col += 1  # количество щёлчков
                if count_col % 3 == 0:
                    j+=1
                if count_col % 6 == 0:
                    i+=1
                    j-=2
    #а может оно само ретурнётся и без ифа
    return min_color, max_color

def Scrolls(cap, min_color, max_color):
    cv2.namedWindow("Main")  # создаем главное окно
    cv2.namedWindow("settings")  # создаем окно настроек

    # создаем 6 бегунков для настройки начального и конечного цвета фильтра
    cv2.createTrackbar('r_min', 'settings', min_color[0], 255, lambda x:x)
    cv2.createTrackbar('g_min', 'settings', min_color[1], 255, lambda x:x)
    cv2.createTrackbar('b_min', 'settings', min_color[2], 255, lambda x:x)
    cv2.createTrackbar('r_max', 'settings', max_color[0], 255, lambda x:x)
    cv2.createTrackbar('g_max', 'settings', max_color[1], 255, lambda x:x)
    cv2.createTrackbar('b_max', 'settings', max_color[2], 255, lambda x:x)

    cv2.createTrackbar('filter_type', 'settings', 1, 3, lambda x: x) # типа без фильтра
    cv2.createTrackbar('blur_coef', 'settings', 7, 50, lambda x: x )

    cv2.createTrackbar('coef_rect_in', 'settings', 15, 50, lambda x: x)
    cv2.createTrackbar('coef_rect_out', 'settings', 21, 50, lambda x: x)
    while True:
        flag, imgtmp = cap.read()
        imgtmp = cv2.flip(imgtmp, 1)
        trash = np.zeros_like(imgtmp)
        # считываем значения бегунков
        h1 = cv2.getTrackbarPos('r_min', 'settings')
        s1 = cv2.getTrackbarPos('g_min', 'settings')
        v1 = cv2.getTrackbarPos('b_min', 'settings')
        h2 = cv2.getTrackbarPos('r_max', 'settings')
        s2 = cv2.getTrackbarPos('g_max', 'settings')
        v2 = cv2.getTrackbarPos('b_max', 'settings')

        filter_type = cv2.getTrackbarPos('filter_type', 'settings') #мб тут что-то вроде енамов добавить или сета
        pixel_size = cv2.getTrackbarPos('blur_coef', 'settings')

        rect_in = cv2.getTrackbarPos('coef_rect_in', 'settings')+1
        rect_out = cv2.getTrackbarPos('coef_rect_out', 'settings')+1
        # формируем начальный и конечный цвет фильтра
        h_min = np.array((h1, s1, v1))
        h_max = np.array((h2, s2, v2))

        # накладываем фильтр на кадр
        filter = cv2.inRange(imgtmp, h_min, h_max)

        # МОРФОЛОГИЧЕСКОЕ ПРЕОБРАЗОВАНИЕ, убирает мелкий шум снаружи и внутри объекта-маркера
        # размывает границы объекта переднего плана (всегда старайтесь, чтобы передний план оставался белым). Так что он делает?
        # Ядро скользит по изображению (как при двумерной свертке). Пиксель в исходном изображении (либо 1, либо 0) будет считаться 1 только в том случае, если все пиксели под ядром равны 1,
        # в противном случае он будет размыт (обнулен).
        # Итак, что происходит, все пиксели около границы будут отброшены в зависимости от размера ядра.
        # Таким образом, толщина или размер объекта переднего плана уменьшается, или просто уменьшается белая область на изображении.
        # Это полезно для удаления небольших белых шумов (как мы видели в главе о цветовом пространстве), отделения двух связанных объектов и т. Д.

#на самом деле я не знаю  помогает оно или нет:D
        st1 = cv2.getStructuringElement(cv2.MORPH_RECT, (rect_in, rect_in), (-1, -1))
        st2 = cv2.getStructuringElement(cv2.MORPH_RECT, (rect_out, rect_out), (-1, -1))
        filter= cv2.morphologyEx(filter, cv2.MORPH_CLOSE, st1)
        filter = cv2.morphologyEx(filter, cv2.MORPH_OPEN, st2)

        if filter_type == 1:
            filter = cv2.medianBlur(filter, 2*pixel_size+1) #cv2.GaussianBlur(filter, (11, 11), 0)#cv2.blur(filter, (11, 11))#cv2.medianBlur(filter, 15)
        if filter_type == 2:
            filter = cv2.GaussianBlur(filter, (2*pixel_size+1, 2*pixel_size+1), 0)
        if filter_type == 3:
            filter = cv2.blur(filter, (2*pixel_size+1, 2*pixel_size+1))
        trash = cv2.add(trash, cv2.bitwise_and(imgtmp, imgtmp, mask=filter))

        cv2.imshow('Main', np.hstack([imgtmp, trash]))

        ch = cv2.waitKey(5)
        if ch == 27:# wait for ESC key to exit|| хорошо бы "OK" найти какой-нибудь
            cv2.destroyWindow("Main")
            cv2.destroyWindow("settings")
            return [h1, s1, v1], [h2, s2, v2], [2*pixel_size+1, filter_type, rect_in, rect_out]

# это хорошо бы в мейн
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# x_vec = []
# y_vec = []
min_color = [255, 255, 255]
max_color = [0, 0, 0]
count_col = 0

ret, img = cap.read()
Marker = np.zeros_like(img)


mask = np.full_like(img, 255)
mask = cv2.flip(mask, 1)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
fgbg = cv2.createBackgroundSubtractorKNN(50, 200.0, False)

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)


    Marker = np.zeros_like(img)
    # режим калибровки
    if not mode:#тут функция котороая возвращает два откалиброванных цвета и потом функция кидающая настройки

      min_color, max_color = Calibration("WM", cap)
      
            # бегунки после калибровки для проверки тцут
      min_color, max_color, filter_opt = Scrolls(cap, min_color, max_color)
      mode = not mode
    # режим рисования
    if mode:

        # поиск в диапазоне цветов, тут можно сократить код
        m1 = cv2.inRange(img, np.array(min_color), np.array(max_color))

        st1 = cv2.getStructuringElement(cv2.MORPH_RECT, (filter_opt[2], filter_opt[2]), (-1, -1))

        m1 = cv2.morphologyEx(m1, cv2.MORPH_CLOSE, st1) #внутри
        st2 = cv2.getStructuringElement(cv2.MORPH_RECT, (filter_opt[3], filter_opt[3]), (-1, -1))
        m1 = cv2.morphologyEx(m1, cv2.MORPH_OPEN, st2) #снаружи

        #Размытие:
        # opencv имеются следующие основные методы размытия: averaging(усреднённое), gaussian(гауссово) и median(медианное)
        # averaging(усреднённое) - это вычисление нового значения пикселя, при котором учитываются значения соседних пикселей.
        # Ядро свёртки — это квадратная матрица, где пиксель в центре этой матрицы затем устанавливается как среднее значение всех других пикселей, окружающих его.

        # Гауссово размытие похоже на предыдущее размытие, за исключением того, что вместо простого среднего мы теперь используем взвешенное среднее,
        # где соседние пиксели, которые ближе к центральному пикселю, вносят больший «вклад» в среднее. Конечным результатом является то, что наше изображение размыто более естественно

        #В медианном размытии центральный пиксель изображения заменяется медианой всех пикселей в области ядра, в результате чего это размытие наиболее эффективно при удалении шума в стиле «соли».

#написать нормально (-_-)
        if filter_opt[1] == 0:
            m1 = cv2.medianBlur(m1, filter_opt[0]) #cv2.GaussianBlur(filter, (11, 11), 0)#cv2.blur(filter, (11, 11))#cv2.medianBlur(filter, 15)
        if filter_opt[1] == 1:
            m1 = cv2.GaussianBlur(m1, (filter_opt[0], filter_opt[0]), 0)
        if filter_opt[1] == 2:
            m1 = cv2.blur(m1, (filter_opt[0], filter_opt[0]))
        #m1 = cv2.medianBlur(m1, filter_opt[0]) #cv2.GaussianBlur(m1, (11, 11), 0)#cv2.blur(m1, (11, 11))#

        Marker = cv2.add(Marker, cv2.bitwise_and(img, img, mask=m1))

        moments = cv2.moments(m1, 1)
        dM01 = moments['m01']
        dM10 = moments['m10']
        dArea = moments['m00']

        if dArea > 5: #тут надо линии нарисовать
            x = int(dM10 / dArea)
            y = int(dM01 / dArea)
            mask = cv2.circle(mask, (x, y), 5, (255, 255, 255), -1)
            

        fgmask = fgbg.apply(Marker)
        #fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

        cv2.imshow("WM", np.hstack([img, Marker, mask]))

    if cv2.waitKey(10) == 27:  # Клавиша Esc
        break
    if not cv2.getWindowProperty('WM', 0) >= 0:  # крестик
        break

cap.release()
cv2.destroyAllWindows()
