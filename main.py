import pygame
import player
import asteroid
from constants import *
from logger import log_state
from circleshape import *
import asteroidfield
from logger import log_event
import sys
import shot


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    clock = pygame.time.Clock()
    dt = 0.0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    player.Player.containers = (updatable, drawable)
    ship = player.Player(x, y)
    asteroids = pygame.sprite.Group()
    asteroid.Asteroid.containers = (asteroids, updatable, drawable)
    asteroidfield.AsteroidField.containers = updatable
    asteroidfield.AsteroidField()
    shots = pygame.sprite.Group()
    shot.Shot.containers = (shots, drawable, updatable)
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 
        screen.fill("black")
        for obj in drawable:
            obj.draw(screen)
        updatable.update(dt)
        for asteroid_obj in asteroids:
            if asteroid_obj.collides_with(ship):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
        for asteroid_obj in asteroids:
            for shot_obj in shots:
                if asteroid_obj.collides_with(shot_obj):
                    log_event("asteroid_shot")
                    asteroid.Asteroid.split(asteroid_obj)
                    pygame.sprite.Sprite.kill(shot_obj)
        pygame.display.flip()
        dt = clock.tick(60) / 1000
    

if __name__ == "__main__":
    main()
