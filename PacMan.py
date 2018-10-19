from pygame.locals import *
from random import randint
import pygame
import time

STEP_SIZE = 44
WINDOW_WIDTH = 18 * STEP_SIZE
WINDOW_HEIGHT = 13 * STEP_SIZE

# Defines the class for the apple
class Apple:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x * STEP_SIZE
        self.y = y * STEP_SIZE

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


# Defines the class for the player (pacman)
class Player:
    x = 0
    y = 0
    direction = 0

    updateCountMax = 2
    updateCount = 0

    def __init__(self):
        # initial positions, no collision.
        self.x = 1 * STEP_SIZE
        self.y = 2 * STEP_SIZE

    # Function controls the movement of the player
    def update(self):

        print("pacman: ", self.x, self.y)

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            # Updates the position of pacman in a direction
            if self.direction == 0: # Right
                if self.x + STEP_SIZE >= WINDOW_WIDTH:
                    self.x = WINDOW_WIDTH - STEP_SIZE
                else:
                    self.x = self.x + STEP_SIZE
            if self.direction == 1: # Left
                if self.x - STEP_SIZE < 0:
                    self.x = 0
                else:
                    self.x = self.x - STEP_SIZE
            if self.direction == 2: # Up
                if self.y - STEP_SIZE < 0:
                    self.y = 0
                else:
                    self.y = self.y - STEP_SIZE
            if self.direction == 3: # Down
                if self.y + STEP_SIZE >= WINDOW_HEIGHT:
                    self.y = WINDOW_HEIGHT - STEP_SIZE
                else:
                    self.y = self.y + STEP_SIZE

            self.updateCount = 0

    def moveRight(self):
        self.direction = 0

    def moveLeft(self):
        self.direction = 1

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


# Defines the class for the ghost
class Computer:
    x = 0
    y = 0
    direction = 0

    updateCountMax = 4
    updateCount = 0

    def __init__(self):
        # initial positions, no collision.
        self.x = 1 * STEP_SIZE
        self.y = 4 * STEP_SIZE

    # Function controls the movement of the ghost
    def update(self):

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            # Updates the position of the ghost
            if self.direction == 0: # Right
                if self.x + STEP_SIZE >= WINDOW_WIDTH:
                    self.x = WINDOW_WIDTH - STEP_SIZE
                else:
                    self.x = self.x + STEP_SIZE
            if self.direction == 1: # Left
                if self.x - STEP_SIZE < 0:
                    self.x = 0
                else:
                    self.x = self.x - STEP_SIZE
            if self.direction == 2: # Up
                if self.y - STEP_SIZE < 0:
                    self.y = 0
                else:
                    self.y = self.y - STEP_SIZE
            if self.direction == 3: # Down
                if self.y + STEP_SIZE >= WINDOW_HEIGHT:
                    self.y = WINDOW_HEIGHT - STEP_SIZE
                else:
                    self.y = self.y + STEP_SIZE

            self.updateCount = 0

    def moveRight(self):
        self.direction = 0

    def moveLeft(self):
        self.direction = 1

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3

    # Function sets the targeting mechanism for the ghost to chase pacman
    def target(self, dx, dy):

        if self.x > dx:
            self.moveLeft()

        if self.x < dx:
            self.moveRight()

        if self.x == dx:
            if self.y < dy:
                self.moveDown()

            if self.y > dy:
                self.moveUp()

    # Function sets the evading mechanism for the ghost to avoid pacman
    def evade(self, dx, dy):

        # If the ghost is hitting the left boundary or right boundary, move up or down depending on y
        if self.x == 0:
            # If the ghost is in the origin corner, move it right
            if self.y == 0 and dx == 0:
                self.moveRight()
                return
            # If the ghost is at the bottom left corner and pacman is above it, move it right
            if self.y == WINDOW_HEIGHT - STEP_SIZE and dx == 0:
                self.moveRight()
                return
            # If the ghost is at the bottom left corner and pacman is to the right of it, move it right
            if self.y == WINDOW_HEIGHT - STEP_SIZE and dy == WINDOW_HEIGHT - STEP_SIZE:
                self.moveUp()
                return
            # If the ghost is above pacman, continue running up
            if self.y < dy:
                self.moveUp()
                return
            # If the ghost is below pacman, continue running down
            else:
                self.moveDown()
                return

        # If the ghost is hitting the top or bottom boundary, move right or left depending on x
        if self.y == 0 or self.y == WINDOW_HEIGHT - STEP_SIZE:
            # If the ghost is in the bottom left corner, move it up and pacman is to the right of it
            if self.x == 0 and dx > self.x:
                self.moveUp()
                return
            # If the ghost is in the top right corner and pacman is to the left of it, move it down
            if dy == 0:
                self.moveDown()
                return
            # If the ghost is in the top right corner and pacman is below it, move it up
            if dy == WINDOW_HEIGHT - STEP_SIZE:
                self.moveUp()
                return
            # If the ghost is to the right of pacman, continue moving right
            if self.x > dx:
                self.moveRight()
                return
            # If the ghost is to the left of pacman, continue moving left
            else:
                self.moveLeft()
                return

        # Right border corner cases
        if self.x == WINDOW_WIDTH - STEP_SIZE:
            # If the ghost is above pacman, continue running up
            if self.y < dy:
                self.moveUp()
                return
            # If the ghost is below pacman, continue running down
            else:
                self.moveDown()
                return

        if self.x > dx:
            self.moveRight()

        if self.x < dx:
            self.moveLeft()

        if self.x == dx:
            if self.y < dy:
                self.moveUp()

            if self.y > dy:
                self.moveDown()

    # Function draws the computer ghost
    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


# Defines the class for the Game
class Game:

    # Function determines whether two objects have collided by comparing where the origin corners of
    # the shape are and the total size of each object (which happens to be the same for the snake heads
    # and the apple)
    def isCollision(self, x1, y1, x2, y2, bsize):
        if x1 < x2 + bsize and x1 + bsize > x2 and y1 < y2 + bsize and y1 + bsize > y2:
                return True
        return False

# Defines the class app the controls all the logic and game function
class App:
    windowWidth = WINDOW_WIDTH
    windowHeight = WINDOW_HEIGHT
    player = 0
    apple = 0
    ate = False
    score = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self._pacman_surf = None
        self.game = Game()
        self.player = Player()
        self.apple = Apple(randint(2, 9), randint(2, 9))
        self.computer = Computer()

    # Function initializes all imported pygame modules, sets screen size and caption, and loads image resources
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)

        pygame.display.set_caption('Pac-Man Implementation')
        self._running = True
        self._image_surf = pygame.image.load("ghost.png").convert()
        self._apple_surf = pygame.image.load("apple.png").convert()
        self._pacman_surf = pygame.image.load("pacman.png").convert()
        self._spooked_surf = pygame.image.load("spooked.png").convert()

    # Function determines if the app received instructions to quit and if so, sets its running parameter to
    # false, ending the game
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    # Function determines the game logic for how the apple moves, the computer snake, and player snake
    def on_loop(self):
        # Determine whether the ghost should target or evade
        if self.ate == False:
            self.computer.target(self.player.x, self.player.y)
        else:
            self.computer.evade(self.player.x, self.player.y)
        self.player.update()
        self.computer.update()

        # Detects if any part of the player snake collided with the apple and if so, it randomizes a new
        # apple location and grows the player snake by one section of snake
        if self.game.isCollision(self.apple.x, self.apple.y, self.player.x, self.player.y, STEP_SIZE):
            self.apple.x = randint(2, 9) * STEP_SIZE
            self.apple.y = randint(2, 9) * STEP_SIZE
            self.ate = True


        # Determines if the head of the player snake collides with itself and if it does, reports that the
        # player was lost by printing a message to console regarding where the collision happened.
        if self.game.isCollision(self.player.x, self.player.y, self.computer.x, self.computer.y, STEP_SIZE):
            if (self.ate == False):
                print("You were caught!")
                exit(0)
            else:
                self.score += 1     # Increase ghost catch score by one
                print("Score +1")
                self.ate = False    # Resets the ghost
                del self.computer
                self.computer = Computer()

        pass

    # Function draws the game components to screen
    def on_render(self):
        self._display_surf.fill((0, 0, 0))                          # Creates a black canvas
        self.player.draw(self._display_surf, self._pacman_surf)     # Draws pacman
        self.apple.draw(self._display_surf, self._apple_surf)       # Draws the apple image
        if self.ate == True:
            self.computer.draw(self._display_surf, self._spooked_surf)    # Draws the ghost spooked
        else:
            self.computer.draw(self._display_surf, self._image_surf)    # Draws the ghost normal
        myfont = pygame.font.SysFont('arial', 20)
        displaytext = "Score: " + str(self.score)
        textsurface = myfont.render(displaytext, False, (255, 255, 255))
        self._display_surf.blit(textsurface,(0,0))
        pygame.display.flip()                                       # Updates the display surface to screen

    # Function uninitializes all pygame modules
    def on_cleanup(self):
        pygame.quit()

    # Function defines what happens from player keyboard IO
    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        # Loop listens for user input and calls the corresponding method to key
        # to move the player snake
        while (self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.player.moveRight()

            if (keys[K_LEFT]):
                self.player.moveLeft()

            if (keys[K_UP]):
                self.player.moveUp()

            if (keys[K_DOWN]):
                self.player.moveDown()

            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()

            time.sleep(50.0 / 1000.0);
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()