import pygame
import random
import os
import sys


pygame.init()
# Константы для игры
WIDTH, HEIGHT = 1300, 800  # Размер окна
FPS = 60  # Частота кадров
PLANTSIMAGES = [f"frame-{i}.png" for i in range(1, len(os.listdir("PBoardImages")) + 1)]
DARKPLANTSIMAGES = [
    f"frame-{i}.png" for i in range(1, len(os.listdir("DarkPBoardImages")) + 1)
]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plants vs Zombies")


def load_image(name, colorkey=None, papka="data"):
    fullname = os.path.join(papka, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Класс для отображения количества солнц (ресурсов)
class SunAmount:
    def __init__(self):
        self.cell_s = 110  # Размер ячейки для отображения солнц
        self.sunam = 10000  # Изначальное количество солнц

    def renderrr(self, scr):
        """
        Отображает панель с количеством солнц на экране.
        :param scr: Поверхность для отрисовки.
        """
        # Рисуем черный прямоугольник
        pygame.draw.rect(
            scr, pygame.Color("black"), (5, 10, self.cell_s, self.cell_s), 1
        )
        # Рисуем большое желтое солнце
        pygame.draw.circle(
            scr,
            pygame.Color((255, 236, 20)),
            (5 + (self.cell_s // 2), 10 + (self.cell_s // 3)),
            self.cell_s // 3,
        )
        # Рисуем малое оранжевое солнце
        pygame.draw.circle(
            scr,
            pygame.Color((255, 186, 0)),
            (5 + (self.cell_s // 2), 10 + (self.cell_s // 3)),
            self.cell_s // 4,
        )
        # Отображаем текст с количеством солнц
        font = pygame.font.Font(None, 40)
        text = font.render(str(self.sunam), True, (0, 0, 0))
        if self.sunam < 10:
            scr.blit(text, (53, self.cell_s + 10 - (self.cell_s // 3)))
        elif 10 <= self.sunam < 100:
            scr.blit(text, (46, self.cell_s + 10 - (self.cell_s // 3)))
        elif 100 <= self.sunam < 1000:
            scr.blit(text, (38, self.cell_s + 10 - (self.cell_s // 3)))
        else:
            scr.blit(text, (30, self.cell_s + 10 - (self.cell_s // 3)))


# Класс для панели выбора растений
class PlantBoard:
    def __init__(self):
        self.width = 4  # Количество ячеек
        self.cell_size = 100  # Размер ячейки
        self.left = 150
        self.top = 10
        self.selected_plant = None
        self.numcol = None
        self.prices = [50, 100, 50, 150]

    def renderr(self, scr):
        """
        Отрисовывает панель выбора растений.
        :param scr: Поверхность для отрисовки.
        """
        for row in range(self.width):
            if self.numcol == row:
                im = load_image(PLANTSIMAGES[row], papka="DarkPBoardImages")
            else:
                im = load_image(PLANTSIMAGES[row], papka="PBoardImages")
            im = pygame.transform.scale(im, (self.cell_size, self.cell_size))
            scr.blit(im, (row * self.cell_size + self.left, self.top))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        height = (x - self.left) // self.cell_size
        width = (y - self.top) // self.cell_size
        if 0 <= width < 1 and 0 <= height < self.width:
            if self.selected_plant == height:
                self.selected_plant = None
                self.numcol = None
            else:
                self.selected_plant = height
                self.numcol = height
            return True
        return False


# Класс для игрового поля
class Board:
    def __init__(self, width, height):
        self.width = width  # Ширина (количество столбцов)
        self.height = height  # Высота (количество строк)
        self.board = [[0] * width for _ in range(height)]  # Создаем пустое поле
        self.left = 210  # Отступ слева
        self.top = 125  # Отступ сверху
        self.cell_width = 105  # Ширина ячейки
        self.cell_hight = 125  # Высота ячейки

    def render(self, scr):
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(
                    scr,
                    pygame.Color("black"),
                    (
                        self.left + row * self.cell_width,
                        self.top + col * self.cell_hight,
                        self.cell_width,
                        self.cell_hight,
                    ),
                    1,
                )

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        height = (x - self.left) // self.cell_width
        width = (y - self.top) // self.cell_hight
        if 0 <= width < self.width and 1 <= height < self.height - 1:
            return height, width
        return None


class Sun(pygame.sprite.Sprite):
    image = load_image("sun.png")

    def __init__(self, bysun=False, xcell=0, ycell=0):
        super().__init__()
        self.image = pygame.transform.scale(Sun.image, (75, 75))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(Sun.image)
        if not bysun:
            self.rect.x = random.randint(315, 1260)
            self.rect.y = 0
            self.last_y = random.randint(225, 675)
        else:
            self.rect.x = xcell + random.randint(5, 30)
            self.rect.y = ycell
            self.last_y = ycell + 50
        self.speed = 1

    def on_click(self, pos):
        flag = False
        if self.rect.collidepoint(pos):
            flag = True
            Sam.sunam += 25
            self.kill()
        return flag

    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= self.last_y:
            self.speed = 0


class Plant(pygame.sprite.Sprite):

    def __init__(self, xcell, ycell, frames, animation_speed=35):
        super().__init__()
        self.frames = frames
        self.current_frame = 0
        self.image = pygame.transform.scale(self.frames[self.current_frame], (128, 128))
        self.rect = self.image.get_rect()
        self.rect.x = (xcell * board.cell_hight + board.left) - (22 * xcell)
        self.rect.y = (ycell * board.cell_width + board.top - 2) + (20 * ycell)
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = animation_speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(
                self.frames[self.current_frame], (128, 128)
            )


class Sunflower(Plant):
    global clock

    def __init__(self, xcell, ycell, frames):
        super().__init__(xcell, ycell, frames)
        self.last_sun = 0
        self.health = 100

    def update(self):
        super().update()
        self.last_sun += clock.get_time()
        if self.last_sun >= 10000:
            self.last_sun = 0
            sungroup.add(Sun(True, self.rect.x, self.rect.y))


class WallNut(Plant):

    def __init__(self, xcell, ycell, frames):
        super().__init__(xcell, ycell, frames)
        self.health = 500
        self.rect.x = xcell * board.cell_hight + board.left + 10 - (20 * xcell)
        self.rect.y = (ycell * board.cell_width + board.top + 14) + (22 * ycell)
        self.image = pygame.transform.scale(self.frames[self.current_frame], (95, 90))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        super().update()
        self.image = pygame.transform.scale(self.frames[self.current_frame], (95, 90))


# Класс для зомби
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, frames, speed=1, animation_speed=35):
        """
        Инициализация зомби.
        :param x: Начальная координата по оси X.
        :param y: Начальная координата по оси Y.
        :param frames: Список кадров для анимации зомби.
        :param speed: Скорость движения.
        :param animation_speed: Скорость смены кадров (в миллисекундах).
        """
        super().__init__()
        self.frames = frames  # Кадры анимации
        self.current_frame = 0  # Текущий кадр
        self.image = self.frames[self.current_frame]  # Устанавливаем начальный кадр
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.x_pos = float(x)  # Используем float для плавного движения
        self.rect.y = y
        self.speed = speed  # Скорость движения
        self.animation_speed = animation_speed  # Скорость анимации
        self.last_update = pygame.time.get_ticks()  # Последнее обновление кадра

    def update(self):
        """
        Обновление состояния зомби.
        """
        # Смена кадров анимации
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

        # Движение зомби
        self.x_pos -= self.speed
        self.rect.x = int(self.x_pos)
        # Удаление зомби, если он ушел за пределы экрана
        if self.rect.x < -self.rect.width:
            self.kill()


# Функция для загрузки кадров анимации зомби
def load_zombie_frames():
    """
    Загружает кадры для анимации зомби.
    :return: Список кадров.
    """
    frames = []
    for i in range(1, 43):
        frame = pygame.image.load(f"assets/zombies/frame ({i}).gif").convert_alpha()
        frames.append(frame)
    return frames


def load_plants_frames(plant):
    frames = []
    for i in range(1, len(os.listdir(plant)) + 1):
        frame = pygame.image.load(f"{plant}/frame-{i}.gif").convert_alpha()
        frames.append(frame)
    return frames


# Функция для создания зомби
def spawn_zombie(frames):
    """
    Создает зомби и добавляет его в группу.
    :param frames: Список кадров анимации.
    """
    lane = random.randint(0, board.width - 1)  # Выбираем случайную линию
    y_position = lane * board.cell_hight + (board.cell_hight // 2) + 25  # Позиция по Y
    zombie = Zombie(WIDTH, y_position, frames)  # Создаем зомби
    zombies.add(zombie)  # Добавляем в группу


def spawn_plant(plnt):
    plant = None
    coords = board.get_cell(pygame.mouse.get_pos())
    if coords == None:
        return None
    else:
        x = coords[0] * board.cell_hight + board.left - 22 * coords[0]
        y = coords[1] * board.cell_width + board.top + 20 * coords[1]
        if plnt == 0:
            plant = Sunflower(coords[0], coords[1], sunflower_frames)
        elif plnt == 1:
            pass

        elif plnt == 2:
            plant = WallNut(coords[0], coords[1], nut_frames)
        elif plnt == 3:
            pass
        if plant:
            for el in plants:
                if pygame.sprite.collide_mask(plant, el):
                    return None
            if Pboard.prices[plnt] <= Sam.sunam:
                Sam.sunam -= Pboard.prices[plnt]
                plants.add(plant)


# Основной игровой цикл
def main():
    global clock
    background = pygame.image.load("jardin.png")  # Загружаем фон
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Масштабируем фон

    spawn_timer = 0  # Таймер спавна зомби
    spawn_interval = 5000  # Интервал появления зомби (в миллисекундах)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Если нажата кнопка закрытия
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag = True
                for elem in sungroup:
                    if elem.on_click(event.pos):
                        flag = False
                if flag:
                    if Pboard.get_cell(event.pos):
                        continue
                    spawn_plant(Pboard.selected_plant)

        # Обновляем таймер спавна
        spawn_timer += clock.get_time()
        if spawn_timer >= spawn_interval:
            sungroup.add(Sun())
            spawn_timer = 0
            spawn_zombie(zombie_frames)  # Создаем нового зомби

        zombies.update()  # Обновляем зомби
        sungroup.update()
        plants.update()

        # Отрисовка всех элементов
        screen.blit(background, (0, 0))  # Фон
        board.render(screen)  # Игровое поле
        Pboard.renderr(screen)  # Панель выбора растений
        Sam.renderrr(screen)  # Панель с солнцами
        zombies.draw(screen)  # Зомби
        plants.draw(screen)
        sungroup.draw(screen)

        pygame.display.flip()  # Обновляем экран
        clock.tick(FPS)  # Ограничиваем FPS

    pygame.quit()  # Завершаем игру


if __name__ == "__main__":
    clock = pygame.time.Clock()
    Sam = SunAmount()  # Создаем панель солнц
    board = Board(5, 11)  # Создаем игровое поле
    Pboard = PlantBoard()  # Создаем панель выбора растений

    zombies = pygame.sprite.Group()  # Группа для зомби
    sungroup = pygame.sprite.Group()
    plants = pygame.sprite.Group()

    zombie_frames = load_zombie_frames()  # Загружаем кадры зомби
    sunflower_frames = load_plants_frames("sunflower")
    nut_frames = load_plants_frames("wallnut")

    main()  # Запускаем игру
