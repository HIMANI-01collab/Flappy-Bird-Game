
import pygame
import os
import random

pygame.init()

# ---------------- SETTINGS ----------------

WIDTH = 500
HEIGHT = 800
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

CLOCK = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)

FONT = pygame.font.SysFont("comicsans", 40, bold=True)
SMALL_FONT = pygame.font.SysFont("comicsans", 24)

# ---------------- LOAD IMAGES ----------------

BIRD_IMGS = [
    pygame.transform.scale2x(
        pygame.image.load(os.path.join("imgs", "bird1.png"))
    ),
    pygame.transform.scale2x(
        pygame.image.load(os.path.join("imgs", "bird2.png"))
    ),
    pygame.transform.scale2x(
        pygame.image.load(os.path.join("imgs", "bird3.png"))
    )
]

PIPE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "pipe.png"))
)

BASE_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "base.png"))
)

BG_IMG = pygame.transform.scale2x(
    pygame.image.load(os.path.join("imgs", "bg.png"))
)

BASE_Y = HEIGHT - BASE_IMG.get_height()

# ---------------- BIRD CLASS ----------------

class Bird:

    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.tilt = 0
        self.tick_count = 0
        self.vel = 0

        self.height = y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):

        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):

        self.tick_count += 1

        displacement = (
            self.vel * self.tick_count
            + 1.5 * self.tick_count ** 2
        )

        if displacement >= 16:
            displacement = 16

        if displacement < 0:
            displacement -= 2

        self.y += displacement

        if displacement < 0 or self.y < self.height + 50:

            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION

        else:

            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):

        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]

        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]

        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]

        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]

        else:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]

        rotated_image = pygame.transform.rotate(
            self.img, self.tilt
        )

        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(
                topleft=(self.x, self.y)
            ).center
        )

        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):

        return pygame.mask.from_surface(self.img)

# ---------------- PIPE CLASS ----------------

class Pipe:

    GAP = 180
    VEL = 5

    def __init__(self, x):

        self.x = x

        self.height = random.randrange(120, BASE_Y - 180)

        self.top = self.height - PIPE_IMG.get_height()
        self.bottom = self.height + self.GAP

        self.PIPE_TOP = pygame.transform.flip(
            PIPE_IMG, False, True
        )

        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False

    def move(self):

        self.x -= self.VEL

    def draw(self, win):

        win.blit(
            self.PIPE_TOP,
            (self.x, self.top)
        )

        win.blit(
            self.PIPE_BOTTOM,
            (self.x, self.bottom)
        )

    def collide(self, bird):

        bird_mask = bird.get_mask()

        top_mask = pygame.mask.from_surface(
            self.PIPE_TOP
        )

        bottom_mask = pygame.mask.from_surface(
            self.PIPE_BOTTOM
        )

        top_offset = (
            int(self.x - bird.x),
            int(self.top - bird.y)
        )

        bottom_offset = (
            int(self.x - bird.x),
            int(self.bottom - bird.y)
        )

        top_collision = bird_mask.overlap(
            top_mask, top_offset
        )

        bottom_collision = bird_mask.overlap(
            bottom_mask, bottom_offset
        )

        return top_collision or bottom_collision

# ---------------- BASE CLASS ----------------

class Base:

    VEL = 5

    def __init__(self, y):

        self.y = y

        self.x1 = 0
        self.x2 = BASE_IMG.get_width()

    def move(self):

        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + BASE_IMG.get_width() < 0:
            self.x1 = self.x2 + BASE_IMG.get_width()

        if self.x2 + BASE_IMG.get_width() < 0:
            self.x2 = self.x1 + BASE_IMG.get_width()

    def draw(self, win):

        win.blit(BASE_IMG, (self.x1, self.y))
        win.blit(BASE_IMG, (self.x2, self.y))

# ---------------- DRAW WINDOW ----------------

def draw_window(win, bird, pipes, base, score, best_score, state):

    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    bird.draw(win)

    base.draw(win)

    score_text = FONT.render(
        str(score), True, WHITE
    )

    win.blit(
        score_text,
        (WIDTH // 2 - score_text.get_width() // 2, 30)
    )

    best_text = SMALL_FONT.render(
        f"BEST: {best_score}", True, WHITE
    )

    win.blit(best_text, (10, 10))

    if state == "START":

        title = FONT.render(
            "FLAPPY BIRD", True, GOLD
        )

        instruction = SMALL_FONT.render(
            "Press SPACE to Start", True, WHITE
        )

        win.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 250)
        )

        win.blit(
            instruction,
            (WIDTH // 2 - instruction.get_width() // 2, 320)
        )

    elif state == "GAME_OVER":

        game_over = FONT.render(
            "GAME OVER", True, WHITE
        )

        restart = SMALL_FONT.render(
            "Press SPACE or R to Restart", True, WHITE
        )

        win.blit(
            game_over,
            (WIDTH // 2 - game_over.get_width() // 2, 280)
        )

        win.blit(
            restart,
            (WIDTH // 2 - restart.get_width() // 2, 350)
        )

    pygame.display.update()

# ---------------- HIGH SCORE ----------------

def load_best_score():

    try:
        with open("best_score.txt", "r") as file:
            return int(file.read())

    except (FileNotFoundError, ValueError):
        return 0


def save_best_score(score):

    with open("best_score.txt", "w") as file:
        file.write(str(score))

# ---------------- GAME ----------------

def main():

    bird = Bird(150, 300)

    pipes = [Pipe(WIDTH + 100)]

    base = Base(BASE_Y)

    score = 0
    best_score = load_best_score()

    state = "START"

    run = True

    while run:

        CLOCK.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    run = False

                if event.key == pygame.K_SPACE:

                    if state == "START":
                        state = "PLAYING"
                        bird.jump()

                    elif state == "PLAYING":
                        bird.jump()

                    elif state == "GAME_OVER":
                        bird = Bird(150, 300)
                        pipes = [Pipe(WIDTH + 100)]
                        base = Base(BASE_Y)
                        score = 0
                        state = "PLAYING"
                        bird.jump()

                if event.key == pygame.K_r and state == "GAME_OVER":

                    bird = Bird(150, 300)
                    pipes = [Pipe(WIDTH + 100)]
                    base = Base(BASE_Y)
                    score = 0
                    state = "PLAYING"
                    bird.jump()

        if state == "PLAYING":

            bird.move()

            base.move()

            # Move pipes
            for pipe in pipes:
                pipe.move()

                # Check collision
                if pipe.collide(bird):
                    state = "GAME_OVER"

                # Score
                if not pipe.passed and pipe.x + PIPE_IMG.get_width() < bird.x:

                    pipe.passed = True
                    score += 1

            # Remove pipes outside screen
            pipes = [
                pipe for pipe in pipes
                if pipe.x + PIPE_IMG.get_width() > 0
            ]

            # Add new pipes
            if len(pipes) == 0 or pipes[-1].x < WIDTH - 250:

                pipes.append(Pipe(WIDTH + 100))

            # Check ground and ceiling collision
            if bird.y + bird.img.get_height() >= BASE_Y:
                state = "GAME_OVER"

            if bird.y < 0:
                state = "GAME_OVER"

            # Save high score
            if state == "GAME_OVER" and score > best_score:

                best_score = score
                save_best_score(best_score)

        draw_window(
            WIN,
            bird,
            pipes,
            base,
            score,
            best_score,
            state
        )

    pygame.quit()


if __name__ == "__main__":
    main()
