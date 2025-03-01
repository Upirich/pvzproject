import pygame
import random
import os
import sys
import pygame.draw


pygame.init()
WIDTH, HEIGHT = 1300, 800
FPS = 60
PLANTSIMAGES = [f"frame-{i}.png" for i in range(1, len(os.listdir("PBoardImages")) + 1)]
DARKPLANTSIMAGES = [
    f"frame-{i}.png" for i in range(1, len(os.listdir("DarkPBoardImages")) + 1)
]
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Plants vs Zombies")
pygame.mixer.init()
pygame.mixer.music.load("data/plants_vs_zombies.mp3")
sound_effect = pygame.mixer.Sound("data/awooga.mp3")
kill_effect = pygame.mixer.Sound("data/zombie_falling.mp3")
shoot_effect = pygame.mixer.Sound("data/throw.mp3")
chomp = pygame.mixer.Sound("data/chomp.mp3")
chomp.set_volume(0.1)
hit = pygame.mixer.Sound("data/hit.mp3")
hit.set_volume(0.8)
sound_interval = 10
last_sound_time = 0


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


def isclicked(point, polygon):
    x, y = point
    n = len(polygon)
    flag = False
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        if y > min(y1, y2):
            if y <= max(y1, y2):
                if x <= max(x1, x2):
                    if y1 != y2:
                        xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                    if y1 == y2 or x <= xinters:
                        flag = not flag
    return flag


class MainMenu:
    def __init__(self):
        self.background = load_image("main_menu.png", papka="menu")
        self.backgroundPlay = load_image("menuPlay.png", papka="menu")
        self.backgroundExit = load_image("menuExit.png", papka="menu")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.backgroundPlay = pygame.transform.scale(
            self.backgroundPlay, (WIDTH, HEIGHT)
        )
        self.backgroundExit = pygame.transform.scale(
            self.backgroundExit, (WIDTH, HEIGHT)
        )
        self.selected = 0
        self.playButtonPoints = [
            (666, 130),
            (662, 216),
            (1039, 277),
            (1056, 160),
            (957, 143),
            (913, 94),
            (774, 93),
            (733, 124),
        ]
        self.resPlay = [(i[0], i[1]) for i in self.playButtonPoints]
        self.exitButtonPoints = [
            (1023, 703),
            (1054, 731),
            (1085, 732),
            (1111, 713),
            (1106, 605),
            (1037, 606),
        ]

    def draw(self, scr):
        if not self.selected:
            scr.blit(self.background, (0, 0))
        elif self.selected == 1:
            scr.blit(self.backgroundPlay, (0, 0))
        elif self.selected == 2:
            scr.blit(self.backgroundExit, (0, 0))

    def handle_click(self, pos):
        if isclicked(pos, self.resPlay):
            return "play"
        elif isclicked(pos, self.exitButtonPoints):
            return "exit"

    def update(self):
        pos = pygame.mouse.get_pos()
        if isclicked(pos, self.playButtonPoints):
            self.selected = 1
        elif isclicked(pos, self.exitButtonPoints):
            self.selected = 2
        else:
            self.selected = 0


class Map_select:
    def __init__(self):
        self.background = pygame.transform.scale(
            load_image("menu_background.png", papka="menu"), (WIDTH, HEIGHT)
        )
        self.day = pygame.transform.scale(
            load_image("day.png", papka="menu"), (300, 200)
        )
        self.night = pygame.transform.scale(
            load_image("night.png", papka="menu"), (300, 200)
        )
        self.select_map = pygame.transform.scale(
            load_image("map_select_menu.png", papka="menu"), (700, 500)
        )
        self.smRect = self.select_map.get_rect()
        self.dayRect = pygame.rect.Rect(
            WIDTH // 2 - self.smRect[2] // 2 + self.smRect[2] // 22,
            HEIGHT // 2 - self.smRect[3] // 2 + self.smRect[3] // 3,
            300,
            200,
        )
        self.nightRect = pygame.rect.Rect(
            WIDTH // 2
            + (self.smRect[2] // 2 - self.night.get_rect()[2])
            - self.smRect[2] // 22,
            HEIGHT // 2 - self.smRect[3] // 2 + self.smRect[3] // 3,
            300,
            200,
        )
        self.exitRect = pygame.rect.Rect(405, 588, 215, 42)
        self.font = pygame.font.SysFont("arial", 40)
        self.text = self.font.render("Choose a level", True, pygame.Color((3, 192, 60)))

    def draw(self, scr):
        scr.blit(self.background, (0, 0))
        scr.blit(
            self.select_map,
            (
                WIDTH // 2 - self.smRect[2] // 2,
                HEIGHT // 2 - self.smRect[3] // 2,
            ),
        )
        scr.blit(
            self.day,
            (
                WIDTH // 2 - self.smRect[2] // 2 + self.smRect[2] // 22,
                HEIGHT // 2 - self.smRect[3] // 2 + self.smRect[3] // 3,
            ),
        )
        scr.blit(
            self.night,
            (
                WIDTH // 2
                + (self.smRect[2] // 2 - self.night.get_rect()[2])
                - self.smRect[2] // 22,
                HEIGHT // 2 - self.smRect[3] // 2 + self.smRect[3] // 3,
            ),
        )
        scr.blit(
            self.text,
            (
                WIDTH // 2 - self.text.get_rect()[2] // 2,
                HEIGHT // 2 - self.smRect[3] // 3,
            ),
        )

    def on_click(self, pos):
        if self.exitRect.collidepoint(pos):
            return -1
        elif self.dayRect.collidepoint(pos):
            return 1
        elif self.nightRect.collidepoint(pos):
            return 2


class SunAmount:
    def __init__(self):
        self.cell_s = 110
        self.sunam = 50
        self.sun_timer = 0
        self.sun_interval = 12000
        self.sun_image = pygame.image.load("data/sun.png").convert_alpha()
        self.sun_image = pygame.transform.scale(
            self.sun_image, (self.cell_s, self.cell_s)
        )

    def renderrr(self, scr):
        scr.blit(self.sun_image, (5, 5))
        font = pygame.font.Font(None, 40)
        text = font.render(str(self.sunam), True, (0, 0, 0))
        if self.sunam < 10:
            scr.blit(text, (53, self.cell_s + 10 - (self.cell_s // 3) + 30))
        elif 10 <= self.sunam < 100:
            scr.blit(text, (46, self.cell_s + 10 - (self.cell_s // 3) + 30))
        elif 100 <= self.sunam < 1000:
            scr.blit(text, (38, self.cell_s + 10 - (self.cell_s // 3)))
        else:
            scr.blit(text, (30, self.cell_s + 10 - (self.cell_s // 3)))

    def update(self):
        self.sun_timer += clock.get_time()
        if self.sun_timer >= self.sun_interval:
            self.sun_timer = 0
            sungroup.add(Sun())


class PlantBoard:
    def __init__(self):
        self.width = 4
        self.cell_size = 110
        self.left = 150
        self.top = 10
        self.selected_plant = None
        self.numcol = None
        self.prices = [50, 100, 50]

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
        self.cell_width = 105
        self.cell_hight = 125

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        col = (x - self.left) // self.cell_width
        row = (y - self.top) // self.cell_hight
        if 1 <= col < self.height - 1 and 0 <= row < self.width:
            return col, row
        return None


class LawnMower(pygame.sprite.Sprite):
    im = load_image("LawnMower.png")

    def __init__(self, ycell):
        super().__init__()
        self.image = pygame.transform.scale(LawnMower.im, (int(80), int(80)))
        self.rect = self.image.get_rect()
        self.rect.x = int((board.left + board.cell_hight // 3))
        self.rect.y = int((ycell * board.cell_width + board.top - 2) + (24 * ycell))
        self.ycell = ycell
        self.mask = pygame.mask.from_surface(self.image)
        self.ismoving = False

    def update(self):
        if not self.ismoving:
            for el in zombies:
                if el.rect.x < board.left and el.ycell == self.ycell:
                    self.ismoving = True
                    break
        elif self.rect.x > 1380:
            self.kill()
        else:
            self.rect.x += 5
            for el in zombies:
                if pygame.sprite.collide_mask(self, el) and self.ycell == el.ycell:
                    el.kill()


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
    def __init__(self, xcell, ycell, frames, animation_speed=30):
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
        self.ycell = ycell
        self.xcell = xcell

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(
                self.frames[self.current_frame], (128, 128)
            )
        if self.health <= 0:
            self.kill()


class Sunflower(Plant):
    def __init__(self, xcell, ycell, frames):
        super().__init__(xcell, ycell, frames)
        self.last_sun = 0
        self.interval = 13000
        self.health = 300

    def update(self):
        super().update()
        self.last_sun += clock.get_time()
        if self.last_sun >= self.interval:
            self.last_sun = 0
            sungroup.add(Sun(True, self.rect.x, self.rect.y))
            shoot_effect.play()


class WallNut(Plant):
    def __init__(self, xcell, ycell, frames):
        super().__init__(xcell, ycell, frames)
        self.health = 900
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
        self.health = 300
        self.image = pygame.transform.scale(self.frames[self.current_frame], (95, 90))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = xcell * board.cell_hight + board.left + 10 - (20 * xcell)
        self.rect.y = (ycell * board.cell_width + board.top + 14) + (22 * ycell)
        self.shoot_timer = 0
        self.shoot_interval = 1500

    def update(self):
        self.shoot_timer += clock.get_time()
        super().update()
        for el in zombies:
            if el.ycell == self.ycell:
                if self.shoot_timer >= self.shoot_interval:
                    bullets.add(Pea(self.xcell, self.ycell))
                    self.shoot_timer = 0
                    shoot_effect.play()
        self.image = pygame.transform.scale(self.frames[self.current_frame], (95, 90))


class Pea(pygame.sprite.Sprite):
    im = load_image("pea.png")

    def __init__(self, xcell, ycell):
        super().__init__()
        self.image = Pea.im
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 6
        self.xcell = xcell
        self.ycell = ycell
        self.rect = self.image.get_rect()
        self.rect.x = (xcell * board.cell_hight + board.left + 70) - (20 * xcell)
        self.rect.y = (ycell * board.cell_width + board.top + 22) + (22 * ycell)
        self.damage = 25

    def update(self):
        self.rect.x += self.speed
        for el in zombies:
            if pygame.sprite.collide_mask(self, el):
                el.health -= self.damage
                hit.play()
                self.kill()
                break
        if self.xcell >= 11:
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
        self.ycell = (y - board.top) // board.cell_hight + 1
        self.animation_speed = animation_speed
        self.last_update = pygame.time.get_ticks()
        self.speed_update = pygame.time.get_ticks()
        self.is_attacking = False
        self.health = 200
        self.timer = 0
        self.chomp_len = round(chomp.get_length(), 2) * 1000
        self.sound_timer = 0

    def update(self):
        self.timer += 1
        if self.health <= 0:
            kill_effect.play()
            self.kill()
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            if self.is_attacking:
                self.current_frame = (self.current_frame + 1) % len(self.attack_frames)
                self.image = self.attack_frames[self.current_frame]
            else:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
        for plant in plants:
            if pygame.sprite.collide_mask(self, plant) and (self.ycell == plant.ycell):
                self.is_attacking = True
                self.speed = 0
                plant.health -= 1
                if self.sound_timer >= self.chomp_len:
                    self.sound_timer = 0
                    chomp.play()
                else:
                    self.sound_timer += clock.get_time()
                break
        else:
            self.is_attacking = False
            self.speed = 1

        if not self.is_attacking and self.timer >= 2:
            self.timer = 0
            self.x_pos -= self.speed
            self.rect.x = self.x_pos

        if self.rect.x < board.left - board.cell_hight:
            game_over_animation(screen, "Game Over")
            pygame.quit()
            sys.exit()


class ConeZombie(Zombie):
    def __init__(self, x, y, frames, attack_frames, speed=1, animation_speed=90):
        super().__init__(x, y, frames, attack_frames, speed, animation_speed)
        self.health = 540

    def update(self):
        self.timer += 1
        if self.health <= 0:
            kill_effect.play()
            self.kill()
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            if self.is_attacking:
                self.current_frame = (self.current_frame + 1) % len(self.attack_frames)
                self.image = self.attack_frames[self.current_frame]
            else:
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
            self.mask = pygame.mask.from_surface(self.image)

        for plant in plants:
            if pygame.sprite.collide_mask(self, plant) and (self.ycell == plant.ycell):
                self.is_attacking = True
                self.speed = 0
                plant.health -= 1
                if self.sound_timer >= self.chomp_len:
                    self.sound_timer = 0
                    chomp.play()
                else:
                    self.sound_timer += clock.get_time()
                break
        else:
            self.is_attacking = False
            self.speed = 1

        if not self.is_attacking and self.timer >= 2:
            self.timer = 0
            self.x_pos -= self.speed
            self.rect.x = self.x_pos

        if self.rect.x < board.left - board.cell_hight:
            game_over_animation(screen, "Game Over")
            pygame.quit()
            sys.exit()


def load_zombie_frames():
    frames = []
    for i in range(1, 43):
        gif_path = f"assets/zombies/walk/frame-{i}.gif"
        png_path = f"assets/zombies/walk/frame-{i}.png"
        if os.path.exists(gif_path):
            frame = pygame.image.load(gif_path).convert_alpha()
        elif os.path.exists(png_path):
            frame = pygame.image.load(png_path).convert_alpha()
        else:
            raise FileNotFoundError(f"No frame-{i} found in assets/zombies/walk/")
        frames.append(frame)
    return frames


def load_zombie_attack_frames():
    frames = []
    for i in range(1, 40):
        gif_path = f"assets/zombies/attack/frame-{i}.gif"
        png_path = f"assets/zombies/attack/frame-{i}.png"
        if os.path.exists(gif_path):
            frame = pygame.image.load(gif_path).convert_alpha()
        elif os.path.exists(png_path):
            frame = pygame.image.load(png_path).convert_alpha()
        else:
            raise FileNotFoundError(f"No frame-{i} found in assets/zombies/attack/")
        frames.append(frame)
    return frames


def load_cone_zombie_frames():
    frames = []
    for i in range(0, 21):
        frame = pygame.image.load(
            f"assets/cone_zombies/walk/ConeheadZombie_{i}.png"
        ).convert_alpha()
        frames.append(frame)
    return frames


def load_cone_zombie_attack_frames():
    frames = []
    for i in range(0, 10):
        frame = pygame.image.load(
            f"assets/cone_zombies/attack/ConeheadZombieAttack_{i}.png"
        ).convert_alpha()
        frames.append(frame)
    return frames


def load_plants_frames(plant):
    frames = []
    num_frames = len(os.listdir(plant))
    for i in range(1, num_frames + 1):
        gif_path = f"{plant}/frame-{i}.gif"
        png_path = f"{plant}/frame-{i}.png"
        if os.path.exists(gif_path):
            image = pygame.image.load(gif_path).convert_alpha()
        elif os.path.exists(png_path):
            image = pygame.image.load(png_path).convert_alpha()
        else:
            raise FileNotFoundError(f"No frame-{i} found in {plant}/")
        frames.append(image)
    return frames


def spawn_zombie(frames, attack_frames):
    lane = random.randint(0, board.width - 1)
    y_position = lane * board.cell_hight + (board.cell_hight // 2) + 25
    zombie = Zombie(WIDTH, y_position, frames, attack_frames)
    zombies.add(zombie)


def spawn_cone_zombie(frames, attack_frames):
    lane = random.randint(0, board.width - 1)
    y_position = lane * board.cell_hight + (board.cell_hight // 2) + 25
    cone_zombie = ConeZombie(WIDTH, y_position, frames, attack_frames)
    zombies.add(cone_zombie)
    if random.random() < 0.5:
        spawn_cone_zombie(cone_zombie_frames, cone_zombie_attack_frames)
    else:
        spawn_zombie(zombie_frames, zombie_attack_frames)


def spawn_plant(plnt):
    coords = board.get_cell(pygame.mouse.get_pos())
    if coords is None:
        return None
    else:
        plant = None
        if plnt == 0:
            plant = Sunflower(coords[0], coords[1], sunflower_frames)
        elif plnt == 1:
            plant = PeaShooter(coords[0], coords[1], pea_shooter_frames)
        elif plnt == 2:
            plant = WallNut(coords[0], coords[1], nut_frames)
        elif plnt == 3:
            coords = board.get_cell(pygame.mouse.get_pos())
            for el in plants:
                if (el.xcell, el.ycell) == coords:
                    el.kill()
                    return
        if plant:
            for el in plants:
                if pygame.sprite.collide_mask(plant, el):
                    return
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
        alpha += 2
        if alpha > 255:
            alpha = 255
        clock_anim.tick(FPS)


def main(DayOrNight):
    global clock
    clock = pygame.time.Clock()
    if DayOrNight:
        background = pygame.image.load("dayBackground.png")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    else:
        background = pygame.image.load("nightBackground.png")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT + 200))
    spawn_timer = 0
    if DayOrNight:
        spawn_interval = 24000
    else:
        spawn_interval = 30000
    running = True
    sound_flag = True
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.6)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
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
            spawn_timer = 0
            if sound_flag:
                sound_effect.play()
                sound_flag = False
            if spawn_interval > 4000:
                spawn_interval -= 200
            if random.random() <= 0.3:
                spawn_cone_zombie(cone_zombie_frames, cone_zombie_attack_frames)
            else:
                spawn_zombie(zombie_frames, zombie_attack_frames)
        zombies.update()
        sungroup.update()
        plants.update()
        bullets.update()
        lawnmowers.update()
        if not DayOrNight:
            screen.blit(background, (0, -160))
        else:
            screen.blit(background, (0, 0))
        Pboard.renderr(screen)
        if DayOrNight:
            Sam.update()
        Sam.renderrr(screen)
        zombies.draw(screen)
        plants.draw(screen)
        lawnmowers.draw(screen)
        bullets.draw(screen)
        sungroup.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.mixer.music.stop()


def show_main_menu():
    menu = MainMenu()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                result = menu.handle_click(event.pos)
                if result == "play":
                    show_map_select()
                elif result == "exit":
                    pygame.quit()
                    sys.exit()

        menu.update()
        menu.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def show_map_select():
    clock = pygame.time.Clock()
    menu = Map_select()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                res = menu.on_click(event.pos)
                if res == -1:
                    return
                elif res == 1:
                    main(1)
                elif res == 2:
                    main(0)
                pygame.mixer.music.stop()

        menu.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    Sam = SunAmount()
    board = Board(5, 11)
    Pboard = PlantBoard()
    zombies = pygame.sprite.Group()
    sungroup = pygame.sprite.Group()
    plants = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    lawnmowers = pygame.sprite.Group()
    for i in range(5):
        lawnmowers.add(LawnMower(i))
    zombie_frames = load_zombie_frames()
    zombie_attack_frames = load_zombie_attack_frames()
    cone_zombie_frames = load_cone_zombie_frames()
    cone_zombie_attack_frames = load_cone_zombie_attack_frames()
    sunflower_frames = load_plants_frames("sunflower")
    nut_frames = load_plants_frames("wallnut")
    pea_shooter_frames = load_plants_frames("peashooter")
    show_main_menu()
