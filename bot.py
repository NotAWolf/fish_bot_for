from mss import mss
import time
import cv2
import numpy
import pyautogui
import os


class FishBot():

    active = False
    last_catch_time = 0
    fish = 0

    def __init__(self, delay):
        self.sct = mss()
        self.delay = delay

    def long_click(self):
        pyautogui.mouseDown()
        time.sleep(self.delay)
        pyautogui.mouseUp()

    def fast_click(self):
        pyautogui.mouseDown()
        time.sleep(0.1)
        pyautogui.mouseUp()

    # создаём файл настроек
    def create_settings(self):
        print('Наведите курсор на удочку в инветоре, в течении 10 секунд не убирайте его')
        time.sleep(10)
        x_rod, y_rod = pyautogui.position()
        print('Закончили')
        with open('settings.txt', 'w') as add:
            add.write(f'{x_rod},')
            add.write(f'{y_rod},')

    # починка удочки
    def repair(self):
        with open('settings.txt', 'r') as sett:
            line = sett.read()
            list_xy = line.split(',')
            x_rod, y_rod = int(list_xy[0]), int(list_xy[1])

        pyautogui.press('tab')
        pyautogui.moveTo(x_rod, y_rod, duration=1)
        pyautogui.keyDown('r')
        pyautogui.click()
        time.sleep(1)
        pyautogui.keyUp('r')
        time.sleep(1)
        pyautogui.press('e')
        time.sleep(1)
        pyautogui.press('tab')
        time.sleep(1)
        pyautogui.press('f3')
        time.sleep(2)
        self.fish = 0
        self.start_fishing()

    # проверка на наличие файла настроек
    def first_start_bot(self):
        if os.path.exists('settings.txt'):
            self.start_fishing()
        else:
            self.create_settings()

    def start_fishing(self):
        print('Начало...')
        self.long_click()
        self.last_catch_time = time.time()
        self.active = True
        self.in_fishisng()

    def in_fishisng(self):
        pyautogui.keyDown('f5')
        while self.active:
            # если что-то пошло не так, бот закидывает удочку заново
            if time.time() - self.last_catch_time > 45:
                self.start_fishing()
            # область экрана для скриншотов
            mon = {'top': 0, 'left': 720, 'width': 400, 'height': 1000}
            img = numpy.asarray(self.sct.grab(mon))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # маски для обнаружения цветов: зелённый, желтый и голубой соотвтственно
            lower_green = numpy.array([75, 190, 170])
            upper_green = numpy.array([90, 255, 255])
            mask0 = cv2.inRange(hsv, lower_green, upper_green)

            lower_yellow = numpy.array([20, 210, 250])
            upper_yellow = numpy.array([25, 220, 255])
            mask2 = cv2.inRange(hsv, lower_yellow, upper_yellow)

            lower_blue = numpy.array([100, 200, 200])
            upper_blue = numpy.array([110, 255, 255])
            mask1 = cv2.inRange(hsv, lower_blue, upper_blue)

            hasGreen = numpy.sum(mask0)
            hasBlue = numpy.sum(mask1)
            hasYellow = numpy.sum(mask2)

            if hasGreen > 0 or hasYellow > 0:
                pyautogui.mouseDown()

            else:
                pyautogui.mouseUp()
                if hasBlue > 100:
                    self.end_fishing()

    # конец цикла и начло нового
    def end_fishing(self):
        time.sleep(1)
        self.fast_click()
        pyautogui.keyUp('f5')
        self.last_catch_time = time.time()
        self.fish += 1
        if self.fish == 30:
            self.repair()

        self.start_fishing()


def start_bot():
    delay = float(input('Введите время задержки: '))
    print('Старт через 10 секунд, откройте игру и возьмите удочку')
    time.sleep(10)
    my_bot = FishBot(delay)
    my_bot.first_start_bot()
    my_bot.start_fishing()


if __name__ == '__main__':
    start_bot()


