import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self,x,y):
        super().__init__(x,y,PLAYER_RADIUS)
        self.rotation = 0
        self.x = x
        self.y = y
        self.timer = 0
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        surface = screen
        color = "white"
        points = self.triangle()
        width = 2
        return pygame.draw.polygon(surface, color, points, width)
    
    def rotate(self, dt):
        self.rotation += dt*PLAYER_TURN_RADIUS
        return self.rotation

    def update(self, dt):
        
        self.timer -= dt
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LSHIFT]:
            dt = self.speed_boost(dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)          
        if keys[pygame.K_q]:
            self.strafe(dt)
        if keys[pygame.K_e]:
            self.strafe(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def strafe(self, dt):
        strafe_right = pygame.Vector2(1, 0).rotate(self.rotation)
        self.position += strafe_right * PLAYER_SPEED * dt
    
    def speed_boost(self, dt):
        return dt*2
    
    def shoot(self):
        if self.timer > 0:
            return
        self.timer = PLAYER_SHOOT_COOLDOWN
        bullet = Shot(self.position.x, self.position.y)
        bullet.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        