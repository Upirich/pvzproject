import pygame
import random
import os
import sys

pygame.init()
WIDTH, HEIGHT = 1300, 800  # Размер окна
FPS = 60  # Частота кадров

# Для панели выбора растений: список изображений для активного и неактивного состояния
PLANTSIMAGES = [f"frame-{i}.png" for i in range(1, len(os.listdir("PBoardImages")) + 1)]
DARKPLANTSIMAGES = [
    f"frame-{i}.png" for i in range(1, len(os.listdir("DarkPBoardImages")) + 1)
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plants vs Zombies")


def load_image(name, colorkey=None, papka="data"):
    """
    Загружает изображение из папки.
    :param name: Имя файла.
    :param colorkey: Если не None, устанавливает прозрачность.
    :param papka: Папка, где искать изображение.
    :return: Загруженное изображение.
    """
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
        self.cell_size = 110  # Размер ячейки
        self.left = 150
        self.top = 10
        self.selected_plant = None
        self.numcol = None
        self.prices = [50, 100, 50, 150]

    def renderr(self, scr):
        for row in range(self.width):
            if self.numcol == row:
                im = load_image(PLANTSIMAGES[row], papka="DarkPBoardImages")
            else:
                im = load_image(PLANTSIMAGES[row], papka="PBoardImages")
            im = pygame.transform.scale(im, (self.cell_size, self.cell_size))
            scr.blit(im, (row * self.cell_size + self.left, self.top))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        # Предполагается, что панель состоит из одной строки ячеек
        cell_index = (x - self.left) // self.cell_size
        # Проверяем, что клик находится внутри панели
        if self.top <= y <= self.top + self.cell_size and 0 <= cell_index < self.width:
            if self.selected_plant == cell_index:
                self.selected_plant = None
                self.numcol = None
            else:
                self.selected_plant = cell_index
                self.numcol = cell_index
            return True
        return False


# Класс для игрового поля
class Board:
    def __init__(self, width, height):
        self.width = width  # Количество столбцов
        self.height = height  # Количество строк
        self.board = [[0] * width for _ in range(height)]
        self.left = 210
        self.top = 125
        self.cell_width = 105
        self.cell_hight = 125

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
        col = (x - self.left) // self.cell_width
        row = (y - self.top) // self.cell_hight
        if 0 <= col < self.width and 0 <= row < self.height:
            return col, row
        return None


class Sun(pygame.sprite.Sprite):
    image = load_image("sun.png")

    def __init__(self, bysun=False, xcell=0, ycell=0):
        super().__init__()
        self.image = pygame.transform.scale(Sun.image, (75, 75))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
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
        if self.rect.collidepoint(pos):
            Sam.sunam += 25
            self.kill()
            return True
        return False

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


class PeaShooter(Plant):
    def __init__(self, xcell, ycell, frames):
        super().__init__(xcell, ycell, frames)
        self.health = 100  # Примерное значение здоровья для горохострела

    def update(self):
        super().update()
        # Здесь можно добавить логику стрельбы горошинами


class CherryBomb(Plant):
    def __init__(self, xcell, ycell, frames):
        super().__init__(xcell, ycell, frames)
        self.health = 50  # Примерное значение здоровья для вишенки
        self.timer = 0  # Таймер до взрыва

    def update(self):
        super().update()
        self.timer += clock.get_time()
        if self.timer >= 2000:  # Через 2 секунды вишенка "взрывается"
            # Здесь можно добавить логику нанесения урона зомби в радиусе взрыва
            self.kill()


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
        self.frames = frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.x_pos = float(x)
        self.rect.y = y
        self.speed = speed
        self.animation_speed = animation_speed
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
        self.x_pos -= self.speed
        self.rect.x = int(self.x_pos)
        if self.rect.x < board.left:
            game_over_animation(screen, "Game Over")
            pygame.quit()
            sys.exit()


def load_zombie_frames():
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


def spawn_zombie(frames):
    lane = random.randint(0, board.width - 1)
    y_position = lane * board.cell_hight + (board.cell_hight // 2) + 25
    zombie = Zombie(WIDTH, y_position, frames)
    zombies.add(zombie)


def spawn_plant(plnt):
    coords = board.get_cell(pygame.mouse.get_pos())
    if coords is None:
        return None
    else:
        x = coords[0] * board.cell_hight + board.left - 22 * coords[0]
        y = coords[1] * board.cell_width + board.top + 20 * coords[1]
        plant = None
        if plnt == 0:
            plant = Sunflower(coords[0], coords[1], sunflower_frames)
        elif plnt == 1:
            plant = PeaShooter(coords[0], coords[1], pea_shooter_frames)
        elif plnt == 2:
            plant = WallNut(coords[0], coords[1], nut_frames)
        elif plnt == 3:
            plant = CherryBomb(coords[0], coords[1], cherry_bomb_frames)
        if plant:
            for el in plants:
                if pygame.sprite.collide_mask(plant, el):
                    return None
            if Pboard.prices[plnt] <= Sam.sunam:
                Sam.sunam -= Pboard.prices[plnt]
                plants.add(plant)


def game_over_animation(scr, message, duration=3000):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill((0, 0, 0))
    alpha = 0
    font = pygame.font.Font(None, 100)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    clock_anim = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration:
        scr.blit(text, text_rect)
        overlay.set_alpha(alpha)
        scr.blit(overlay, (0, 0))
        pygame.display.flip()
        alpha += 5
        if alpha > 255:
            alpha = 255
        clock_anim.tick(FPS)


def main():
    global clock
    clock = pygame.time.Clock()
    background = pygame.image.load("jardin.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    spawn_timer = 0
    spawn_interval = 5000  # Интервал спавна зомби в мс
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                flag = True
                for elem in sungroup:
                    if elem.on_click(event.pos):
                        flag = False
                if flag:
                    if Pboard.get_cell(event.pos):
                        continue
                    if Pboard.selected_plant is not None:
                        spawn_plant(Pboard.selected_plant)
        spawn_timer += clock.get_time()
        if spawn_timer >= spawn_interval:
            sungroup.add(Sun())
            spawn_timer = 0
            spawn_zombie(zombie_frames)
        zombies.update()
        sungroup.update()
        plants.update()
        screen.blit(background, (0, 0))
        board.render(screen)
        Pboard.renderr(screen)
        Sam.renderrr(screen)
        zombies.draw(screen)
        plants.draw(screen)
        sungroup.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    Sam = SunAmount()
    board = Board(5, 11)
    Pboard = PlantBoard()
    zombies = pygame.sprite.Group()
    sungroup = pygame.sprite.Group()
    plants = pygame.sprite.Group()
    zombie_frames = load_zombie_frames()
    sunflower_frames = load_plants_frames("sunflower")
    nut_frames = load_plants_frames("wallnut")
    pea_shooter_frames = load_plants_frames("peashooter")
    cherry_bomb_frames = load_plants_frames("cherrybomb")
    main()
