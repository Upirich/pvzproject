import pygame
import random
import os
import sys

pygame.init()

WIDTH, HEIGHT = 1300, 800
FPS = 60

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


class SunAmount:
    def __init__(self):
        self.cell_s = 110
        self.sunam = 10000

    def renderrr(self, scr):
        pygame.draw.rect(
            scr, pygame.Color("black"), (5, 10, self.cell_s, self.cell_s), 1
        )
        pygame.draw.circle(
            scr,
            pygame.Color((255, 236, 20)),
            (5 + (self.cell_s // 2), 10 + (self.cell_s // 3)),
            self.cell_s // 3,
        )
        pygame.draw.circle(
            scr,
            pygame.Color((255, 186, 0)),
            (5 + (self.cell_s // 2), 10 + (self.cell_s // 3)),
            self.cell_s // 4,
        )
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


class PlantBoard:
    def __init__(self):
        self.width = 4
        self.cell_size = 110
        self.left = 150
        self.top = 10
        self.selected_plant = None
        self.numcol = None
        self.prices = [50, 100, 50, 150]

    def renderr(self, scr):
        for row in range(self.width):
            im = (
                load_image(PLANTSIMAGES[row], papka="DarkPBoardImages")
                if self.numcol == row
                else load_image(PLANTSIMAGES[row], papka="PBoardImages")
            )
            im = pygame.transform.scale(im, (self.cell_size, self.cell_size))
            scr.blit(im, (row * self.cell_size + self.left, self.top))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        cell_index = (x - self.left) // self.cell_size
        if self.top <= y <= self.top + self.cell_size and 0 <= cell_index < self.width:
            if self.selected_plant == cell_index:
                self.selected_plant = None
                self.numcol = None
            else:
                self.selected_plant = cell_index
                self.numcol = cell_index
            return True
        return False


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 210
        self.top = 125
        self.cell_width = (WIDTH - self.left) // width  # Рассчитываем ширину ячейки
        self.cell_hight = (HEIGHT - self.top) // height  # Рассчитываем высоту ячейки

    def render(self, scr):
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(
                    scr,
                    pygame.Color("black"),
                    (
                        self.left + col * self.cell_width,  # Правильная формула для X
                        self.top + row * self.cell_hight,  # Правильная формула для Y
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


def spawn_plant(plnt):
    coords = board.get_cell(pygame.mouse.get_pos())
    if coords is None:
        return None
    else:
        col, row = coords
        x = col * board.cell_width + board.left
        y = row * board.cell_hight + board.top
        plant = None
        if plnt == 0:
            plant = Sunflower(col, row, sunflower_frames)
        elif plnt == 1:
            plant = PeaShooter(col, row, pea_shooter_frames)
        elif plnt == 2:
            plant = WallNut(col, row, nut_frames)
        elif plnt == 3:
            plant = CherryBomb(col, row, cherry_bomb_frames)
        if plant:
            for el in plants:
                if pygame.sprite.collide_mask(plant, el):
                    return None
            if Pboard.prices[plnt] <= Sam.sunam:
                Sam.sunam -= Pboard.prices[plnt]
                plants.add(plant)


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
        self.health = 100
        self.last_shot = 0

    def update(self):
        super().update()
        self.last_shot += clock.get_time()
        if self.last_shot >= 2000:  # Стреляет каждые 2 секунды
            self.last_shot = 0
            peas.add(Pea(self.rect.x + 50, self.rect.y + 50))


class CherryBomb(Plant):
    def __init__(self, xcell, ycell, frames):
        super().__init__(xcell, ycell, frames)
        self.health = 50
        self.timer = 0
        self.spawn_time = pygame.time.get_ticks()  # Время спавна вишни

    def update(self):
        super().update()
        self.timer += clock.get_time()
        if self.timer >= 2000:
            for zombie in zombies:
                if pygame.sprite.collide_mask(self, zombie):
                    if (
                        pygame.time.get_ticks() - self.spawn_time >= 8000
                    ):  # Проверяем, прошло ли 8 секунд
                        self.explode()
                        return

    def explode(self):
        explosion_radius = 150  # Радиус взрыва
        for zombie in zombies:
            if (
                abs(zombie.rect.x - self.rect.x) <= explosion_radius
                and abs(zombie.rect.y - self.rect.y) <= explosion_radius
            ):
                zombie.health -= 100
                if zombie.health <= 0:
                    zombie.kill()
        self.kill()


class Pea(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(pygame.Color("green"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH:
            self.kill()


class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, frames, attack_frames, speed=1, animation_speed=35):
        super().__init__()
        self.frames = frames
        self.attack_frames = attack_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.x_pos = float(x)
        self.rect.y = y
        self.speed = speed
        self.animation_speed = animation_speed
        self.last_update = pygame.time.get_ticks()
        self.is_attacking = False
        self.health = 100

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            if self.is_attacking:
                self.current_frame = (self.current_frame + 1) % len(self.attack_frames)
                self.image = self.attack_frames[self.current_frame]
            else:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]

        if not self.is_attacking:
            self.x_pos -= self.speed
            self.rect.x = int(self.x_pos)

        if self.rect.x < board.left:
            game_over_animation(screen, "Game Over")
            pygame.quit()
            sys.exit()


def load_zombie_frames():
    frames = []
    for i in range(1, 43):
        frame = pygame.image.load(f"assets/zombies/walk/frame-{i}.gif").convert_alpha()
        frames.append(frame)
    return frames


def load_zombie_attack_frames():
    frames = []
    for i in range(1, 40):  # Замените на количество кадров атаки
        frame = pygame.image.load(
            f"assets/zombies/attack/frame-{i}.gif"
        ).convert_alpha()
        frames.append(frame)
    return frames


def load_plants_frames(plant):
    frames = []
    num_frames = len(os.listdir(plant))
    for i in range(1, num_frames + 1):
        image = pygame.image.load(f"{plant}/frame-{i}.gif")
        if plant.lower() == "cherrybomb":
            image = image.convert()
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
            image = image.convert_alpha()
        else:
            image = image.convert_alpha()
        frames.append(image)
    return frames


def spawn_zombie(frames, attack_frames):
    lane = random.randint(0, board.width - 1)
    y_position = lane * board.cell_hight + (board.cell_hight // 2) + 25
    zombie = Zombie(WIDTH, y_position, frames, attack_frames)
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


def check_collisions():
    for zombie in zombies:
        for plant in plants:
            if pygame.sprite.collide_mask(zombie, plant):
                zombie.is_attacking = True
                zombie.speed = 0
                plant.health -= 1
                if plant.health <= 0:
                    plant.kill()
                    zombie.is_attacking = False
                    zombie.speed = 1
    for pea in peas:
        for zombie in zombies:
            if pygame.sprite.collide_rect(pea, zombie):
                zombie.health -= 10
                if zombie.health <= 0:
                    zombie.kill()
                pea.kill()


def main():
    global clock
    clock = pygame.time.Clock()
    background = pygame.image.load("jardin.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    spawn_timer = 0
    spawn_interval = 5000
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
            spawn_zombie(zombie_frames, zombie_attack_frames)

        zombies.update()
        sungroup.update()
        plants.update()
        peas.update()
        check_collisions()

        screen.blit(background, (0, 0))
        board.render(screen)
        Pboard.renderr(screen)
        Sam.renderrr(screen)
        zombies.draw(screen)
        plants.draw(screen)
        sungroup.draw(screen)
        peas.draw(screen)

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
    peas = pygame.sprite.Group()
    zombie_frames = load_zombie_frames()
    zombie_attack_frames = load_zombie_attack_frames()
    sunflower_frames = load_plants_frames("sunflower")
    nut_frames = load_plants_frames("wallnut")
    pea_shooter_frames = load_plants_frames("peashooter")
    cherry_bomb_frames = load_plants_frames("cherrybomb")
    main()
