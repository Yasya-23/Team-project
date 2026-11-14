import pygame

pygame.init()
WIDTH = 1000
HEIGHT=850
FPS = 60


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Подобие платформера")

#Частота кадров, если не понятно
clock = pygame.time.Clock()

running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((100, 0, 0))
    pygame.display.flip()

pygame.quit()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((224,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms):
        if not self.on_ground:
            self.vel_y += 0.5  #гравитация
        else:
            self.vel_y = 0

        self.rect.x += self.vel_x

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:  # движется вправо
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:  # движется влево
                    self.rect.left = platform.rect.right
        self.rect.y += int(self.vel_y)
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # падает вниз
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                elif self.vel_y < 0:  # прыгает вверх
                    self.rect.top = platform.rect.bottom
                self.vel_y = 0
                if self.rect.x < 0:
                    self.rect.x = 0
                if self.rect.right >  WIDTH:
                    self.rect.right = WIDTH
                if self.rect.top < 0:
                    self.rect.top = 0
                if self.rect.bottom  > HEIGHT:
                    self.rect.bottom = HEIGHT

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((139,54,38))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Платформер")
    clock = pygame.time.Clock()

    player = Player(100, HEIGHT - 100)
    platforms = pygame.sprite.Group()

    platforms.add(Platform(0, HEIGHT - 20, WIDTH, 10))  # земля
    platforms.add(Platform(200, 700, 50, 15))
    platforms.add(Platform(300, 599, 175, 20))
    platforms.add(Platform(500, 475, 90, 35))
    platforms.add(Platform(230, 375, 90, 20))
    platforms.add(Platform(130, 275, 90, 20))
    platforms.add(Platform(90, 175, 600, 20))


    all_sprites = pygame.sprite.Group()

    all_sprites.add(player)
    all_sprites.add(*platforms)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.on_ground:
                    player.vel_y = -10

        keys = pygame.key.get_pressed()  #Клавиши
        if keys[pygame.K_a]:
            player.vel_x = -5
        if keys[pygame.K_d]:
            player.vel_x = 5
        if keys[pygame.K_s]:
            player.vel_x = 0
        if keys[pygame.K_SPACE]:
            player.vel_y = -10

        player.update(platforms)

        screen.fill((30,30,30))
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()

