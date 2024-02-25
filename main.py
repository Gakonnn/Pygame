import pygame
import sys
import random

def load_image(image_path):
    try:
        image = pygame.image.load(image_path)
        return image
    except pygame.error as e:
        print("Error loading image:", e)
        sys.exit(1)

def load_music(music_path):
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print("Error loading music:", e)

def shake_screen(screen, intensity=10, duration=100):
    original_pos = screen.get_rect().topleft  # Сохраняем исходное положение экрана
    shake_time = pygame.time.get_ticks() + duration  # Определяем, как долго длится тряска
    while pygame.time.get_ticks() < shake_time:
        # Случайное смещение экрана в пределах заданной интенсивности
        random_offset = random.randint(-intensity, intensity), random.randint(-intensity, intensity)
        screen.scroll(*random_offset)  # Смещаем содержимое экрана
        pygame.display.flip()  # Обновляем экран
        screen.scroll(-random_offset[0], -random_offset[1])  # Возвращаем экран на исходную позицию перед следующим кадром
        pygame.time.wait(10)  # Небольшая пауза между смещениями для видимости тряски

    # Возвращаем экран на исходное место после тряски
    screen.scroll(-screen.get_rect().left + original_pos[0], -screen.get_rect().top + original_pos[1])
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.image = load_image("bullet.png")
        self.image = pygame.transform.scale(self.image, (20, 20))

    def update(self):
        self.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class AmmoBox:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image("ammobox.png")
        self.image = pygame.transform.scale(self.image, (30, 30))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def collect(self):
        return 10  # Number of bullets added when collecting the ammo box

max_bullets = 1
bullets = []
total_bullets = 10
ammo_boxes = []

show_start_hint = True


def main():
    pygame.init()
    global total_bullets
    global bullets
    global show_start_hint

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("The worst GAME")

    background_image = load_image("background.jpg")
    background_image = pygame.transform.scale(background_image, (width, height))

    spaceship_image = load_image("spaceship.png")
    spaceship_image = pygame.transform.scale(spaceship_image, (80, 80))

    obstacle_image = load_image("obstacle.png")
    obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))

    bonus_image = load_image("bonus.png")
    bonus_image = pygame.transform.scale(bonus_image, (30, 30))

    ammo_box_image = load_image("ammobox.png")
    ammo_box_image = pygame.transform.scale(ammo_box_image, (30, 30))

    load_music("background_music.mp3")

    level_sound_effect = pygame.mixer.Sound('level-up-bonus-sequence-2-186891.mp3')
    bonus_sound_effect = pygame.mixer.Sound('collect-5930.mp3')

    white = (255, 255, 255)

    player_size = 50
    player_x = width // 2 - player_size // 2
    player_y = height - 2 * player_size
    player_speed = 5

    obstacle_size = 50  # Вот здесь добавляем определение размера препятствия
    obstacle_speed = 5
    obstacle_frequency = 25
    obstacles = []

    bonus_frequency = 50
    bonuses = []

    bonus_score = 0
    font = pygame.font.Font(None, 36)

    current_level = 1

    clock = pygame.time.Clock()

    lives = 3

    # Остальная часть функции main() без изменений...


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if show_start_hint:
            hint_text = font.render("Use LEFT/RIGHT to move, SPACE to shoot!", True, white)
            screen.blit(hint_text, (20, height - 40))  # Измени положение по своему усмотрению
            pygame.display.flip()
            pygame.time.wait(3000)  # Показываем подсказку в течение 3 секунд
            show_start_hint = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_size:
            player_x += player_speed
        if keys[pygame.K_SPACE] and len(bullets) < max_bullets and total_bullets > 0:
            bullet = Bullet(player_x + player_size // 2 - 5, player_y)
            bullets.append(bullet)
            total_bullets -= 1

        if random.randint(1, obstacle_frequency) == 1:
            obstacle_x = random.randint(0, width - obstacle_size)
            obstacle_y = -obstacle_size
            obstacles.append([obstacle_x, obstacle_y])

        for obstacle in obstacles:
            obstacle[1] += obstacle_speed
            if obstacle[1] > height:
                obstacles.remove(obstacle)

        if random.randint(1, bonus_frequency) == 1:
            bonus_x = random.randint(0, width - bonus_image.get_width())
            bonus_y = -bonus_image.get_height()
            bonuses.append([bonus_x, bonus_y])

        for bonus in bonuses:
            bonus[1] += obstacle_speed
            if bonus[1] > height:
                bonuses.remove(bonus)

            bonus_rect = pygame.Rect(bonus[0], bonus[1], bonus_image.get_width(), bonus_image.get_height())
            if pygame.Rect(player_x, player_y, player_size, player_size).colliderect(bonus_rect):
                bonuses.remove(bonus)
                bonus_score += 1
                bonus_sound_effect.play()

        if random.randint(1, 200) == 1:
            ammo_box_x = random.randint(0, width - 30)
            ammo_box_y = -30
            ammo_box = AmmoBox(ammo_box_x, ammo_box_y)
            ammo_boxes.append(ammo_box)

        for ammo_box in ammo_boxes:
            ammo_box.y += obstacle_speed
            if ammo_box.y > height:
                ammo_boxes.remove(ammo_box)

            ammo_box_rect = pygame.Rect(ammo_box.x, ammo_box.y, 30, 30)
            if pygame.Rect(player_x, player_y, player_size, player_size).colliderect(ammo_box_rect):
                ammo_boxes.remove(ammo_box)
                total_bullets += ammo_box.collect()
                bonus_sound_effect.play()

        for bullet in bullets:
            bullet.update()
            if bullet.y < 0:
                bullets.remove(bullet)

            for obstacle in obstacles:
                if pygame.Rect(bullet.x, bullet.y, 10, 10).colliderect(
                        pygame.Rect(obstacle[0], obstacle[1], obstacle_size, obstacle_size)):
                    bullets.remove(bullet)
                    obstacles.remove(obstacle)

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_size, obstacle_size)
            if player_rect.colliderect(obstacle_rect):
                lives -= 1
                shake_screen(screen)

                hint_text = font.render("Be careful! Watch out for obstacles!", True, white)
                screen.blit(hint_text, (20, height - 40))  # Меняй положение подсказки по своему усмотрению
                pygame.display.flip()
                pygame.time.wait(2000)
                if lives == 0:
                    print("Game Over! Bonus Score:", bonus_score)
                    pygame.quit()
                    sys.exit()
                else:
                    print("Lost a life! Lives left:", lives)
                player_x = width // 2 - player_size // 2
                player_y = height - 2 * player_size
                obstacles.clear()
                bonus_score = 0


        screen.blit(background_image, (0, 0))
        screen.blit(spaceship_image, (player_x, player_y))
        for obstacle in obstacles:
            screen.blit(obstacle_image, (obstacle[0], obstacle[1]))
        for bonus in bonuses:
            screen.blit(bonus_image, (bonus[0], bonus[1]))
        for bullet in bullets:
            bullet.draw(screen)
        for ammo_box in ammo_boxes:
            ammo_box.draw(screen)

        score_text = font.render("Bonus Score: " + str(bonus_score), True, white)
        screen.blit(score_text, (10, 10))

        if bonus_score >= current_level * 10:
            current_level += 1
            obstacle_frequency -= 2
            bonus_frequency -= 5
            print("Level Up! Current Level:", current_level)
            level_sound_effect.play()

        level_text = font.render("Level: " + str(current_level), True, white)
        screen.blit(level_text, (width - 120, 10))

        # Отображение общего количества пуль
        bullets_text = font.render("Bullets: " + str(total_bullets), True, white)
        screen.blit(bullets_text, (width - 130, 45))  # Поменяй координаты, если нужно

        # Новая строка для отображения жизней
        lives_text = font.render("Lives: " + str(lives), True, white)
        screen.blit(lives_text, (10, 50))  # Меняй здесь позицию, если нужно

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
