import pygame, random


class VirusNode(pygame.sprite.Sprite):

    def __init__(self, pos, split_time):
        super().__init__()
        self.image = pygame.image.load('virus.png')
        self.image = pygame.transform.smoothscale(self.image, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = pygame.math.Vector2(0, 5)
        self.speed.rotate_ip(random.randint(0, 360))
        self.time = 0
        self.split_time = split_time

    def update(self):
        self.time += 1
        self.rect.move_ip(self.speed)
        if random.randint(0, 20) == 0:
            rotation = random.choice([-15, 15])
            self.speed.rotate_ip(rotation)
        if self.rect.left < 0 or self.rect.right > 850:
            self.speed[0] *= -1
            self.rect.move_ip(self.speed[0], 0)
        if self.rect.top < 0 or self.rect.bottom > 480:
            self.speed[1] *= -1
            self.rect.move_ip(0, self.speed[1])
        if self.time % self.split_time == 0:
            self.groups()[0].add(VirusNode(self.rect.center, self.split_time))
