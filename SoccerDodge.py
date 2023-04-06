import pygame
import random

pygame.init()

# Set up the screen
screen_width = 478
screen_height = 850
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Soccer Dodge!")

field_image = pygame.image.load("field.png").convert_alpha()
ball_image = pygame.image.load("ball.png").convert_alpha()
leg_image = pygame.image.load("leg.png").convert_alpha()

pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts
font = pygame.font.Font("SoccerLeague.ttf", 30)
font2 = pygame.font.Font("SoccerLeague.ttf", 50)

ball_rect = ball_image.get_rect()
ball_speed = 0.5

# Leg
legs = []
leg_speed = 0
leg_spawn_rate = 0
leg_spawn_timer = 0

# Score variables
score = 0
best_score = 0

clock = pygame.time.Clock()
elapsed_time = 0

class Leg:
    def __init__(self):
        self.side_random = random.randint(0, 1)
        self.image = (
            pygame.transform.flip(leg_image, False, True)
            if self.side_random == 0
            else pygame.transform.flip(leg_image, True, True)
        )
        self.leg_rect = self.image.get_rect()
        self.leg_rect.centerx = (
            screen_width - self.leg_rect.centerx + 5
            if self.side_random == 0
            else 0 + self.leg_rect.centerx - 5
        )
        self.leg_rect.centery = -self.leg_rect.height

    def Move(self):
        leg_speed = random.randint(4, 8) / 10
        self.leg_rect.centery += leg_speed * elapsed_time
        screen.blit(self.image, self.leg_rect)


# Add score text to the screen
def draw_text(text, x, y, fnt, color):
    t = fnt.render(text, True, color)
    r = t.get_rect()
    r.center = (x, y)
    screen.blit(t, r)


class Button:
    def __init__(
        self, x, y, width, height, text, text_color, button_color, hover_color
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.hovered = False

        self.rect.center = (x, y)

    def draw(self):
        if self.hovered:
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.button_color, self.rect)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.hovered = True
            else:
                self.hovered = False
        return False


start_button = Button(
    screen_width / 2,
    screen_height / 2,
    180,
    60,
    "Start",
    (255, 255, 255),
    (250, 230, 0),
    (0, 200, 0),
)
restart_button = Button(
    screen_width / 2,
    screen_height / 2,
    180,
    60,
    "Restart",
    (255, 255, 255),
    (102, 153, 255),
    (0, 200, 0),
)
quit_button = Button(
    screen_width / 2,
    screen_height / 2 + 80,
    180,
    60,
    "Quit",
    (255, 255, 255),
    (255, 0, 0),
    (200, 0, 0),
)

# Set up the game loop
game_over = False
running = True
isGameStart = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        start_clicked = start_button.handle_event(event)
        quit_clicked = quit_button.handle_event(event)
        restart_clicked = restart_button.handle_event(event)
        if start_clicked:
            isGameStart = True
            game_over = False
        if quit_clicked:
            running = False
            isGameStart = True
            game_over = True
        if restart_clicked:
            # Reset the game
            score = 0
            game_over = False
            isGameStart = True
            legs.clear()
            ball_rect.centerx = screen_width // 2
            ball_rect.centery = screen_height - 50

    # Fill the screen
    screen.blit(field_image, (0, 0))

    if not isGameStart:
        # Draw
        draw_text("Soccer Dodge!", screen_width / 2, 160, font2, (255, 255, 255))
        start_button.draw()
        quit_button.draw()

    if not game_over and isGameStart:
        # Handle player input
        elapsed_time = clock.tick(60)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and ball_rect.centery > 0 + 50:
            ball_rect.centery -= ball_speed * elapsed_time
        if keys[pygame.K_s] and ball_rect.centery < screen_height - 50:
            ball_rect.centery += ball_speed * elapsed_time
        if keys[pygame.K_a] and ball_rect.left > 0:
            ball_rect.left -= ball_speed * elapsed_time
        if keys[pygame.K_d] and ball_rect.right < screen_width:
            ball_rect.right += ball_speed * elapsed_time

        leg_spawn_timer += 1
        leg_spawn_rate = random.randint(30, 45)
        if leg_spawn_timer >= leg_spawn_rate:
            leg_spawn_timer = 0
            legs.append(Leg())

        for leg in legs:
            leg.Move()

            # Check for collision with the ball
            if leg.leg_rect.colliderect(ball_rect):
                game_over = True

            if leg.leg_rect.top > screen_height:
                legs.remove(leg)
                score += 1

        # draw ball
        screen.blit(ball_image, ball_rect)

        # Show the score on the screen
        draw_text("Score: " + str(score), screen_width / 2, 50, font, white)

    elif game_over:
        if score > best_score:
            best_score = score

        draw_text("GAME OVER!", screen_width / 2, 80, font2, white)
        draw_text("BEST SCORE: " + str(best_score), screen_width / 2, 150, font, black)

        restart_button.draw()
        quit_button.draw()

    # Update the screen
    pygame.display.flip()


# Quit Pygame
pygame.quit()
quit()
