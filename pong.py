import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

BALL_SIZE = 20
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

WIN_SCORE = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)


class Paddle:
    def __init__(self, x, y, up_key, down_key):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        self.up_key = up_key
        self.down_key = down_key
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, keys):
        if keys[self.up_key]:
            self.y -= self.speed
        if keys[self.down_key]:
            self.y += self.speed

        if self.y < 0:
            self.y = 0
        if self.y + self.height > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.height

        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    def __init__(self, center_x, center_y):
        self.size = BALL_SIZE
        self.rect = pygame.Rect(
            center_x - self.size // 2,
            center_y - self.size // 2,
            self.size,
            self.size
        )
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def bounce_vertical(self):
        self.speed_y *= -1

    def bounce_horizontal(self):
        self.speed_x *= -1

    def reset_center(self, direction):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = BALL_SPEED_X * direction
        self.speed_y = BALL_SPEED_Y

    def stop(self):
        self.speed_x = 0
        self.speed_y = 0

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, self.rect.center, self.size // 2)


class Game:
    def __init__(self, screen, clock, font, small_font):
        self.screen = screen
        self.clock = clock
        self.font = font
        self.small_font = small_font

        self.left_paddle = Paddle(
            50,
            SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2,
            pygame.K_w,
            pygame.K_s
        )

        self.right_paddle = Paddle(
            SCREEN_WIDTH - 50 - PADDLE_WIDTH,
            SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2,
            pygame.K_UP,
            pygame.K_DOWN
        )

        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.score_left = 0
        self.score_right = 0

        self.paused = False
        self.game_over = False
        self.winner = ""

        button_width = 240
        button_height = 50
        self.button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2,
            SCREEN_HEIGHT // 2 + 40,
            button_width,
            button_height
        )

        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_p and not self.game_over:
                    self.paused = not self.paused

            if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                if self.button_rect.collidepoint(event.pos):
                    self.reset_game()

    def update(self):
        if self.paused or self.game_over:
            return

        keys = pygame.key.get_pressed()

        self.left_paddle.update(keys)
        self.right_paddle.update(keys)

        self.ball.move()

        if self.ball.rect.top <= 0:
            self.ball.rect.top = 0
            self.ball.bounce_vertical()

        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.ball.rect.bottom = SCREEN_HEIGHT
            self.ball.bounce_vertical()

        if self.ball.rect.colliderect(self.left_paddle.rect):
            self.ball.rect.left = self.left_paddle.rect.right
            self.ball.bounce_horizontal()

        if self.ball.rect.colliderect(self.right_paddle.rect):
            self.ball.rect.right = self.right_paddle.rect.left
            self.ball.bounce_horizontal()

        self.check_score()

    def check_score(self):
        if self.ball.rect.left <= 0:
            self.score_right += 1
            if self.score_right >= WIN_SCORE:
                self.game_over = True
                self.winner = "Jogador 2 venceu!"
                self.ball.stop()
            else:
                self.ball.reset_center(direction=1)

        elif self.ball.rect.right >= SCREEN_WIDTH:
            self.score_left += 1
            if self.score_left >= WIN_SCORE:
                self.game_over = True
                self.winner = "Jogador 1 venceu!"
                self.ball.stop()
            else:
                self.ball.reset_center(direction=-1)

    def reset_game(self):
        self.score_left = 0
        self.score_right = 0

        self.left_paddle.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.right_paddle.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.left_paddle.rect.y = self.left_paddle.y
        self.right_paddle.rect.y = self.right_paddle.y

        self.ball.reset_center(direction=1)

        self.paused = False
        self.game_over = False
        self.winner = ""

    def draw(self):
        self.screen.fill(BLACK)

        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(
                self.screen,
                GRAY,
                (SCREEN_WIDTH // 2, y),
                (SCREEN_WIDTH // 2, y + 20),
                2
            )

        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)

        score_text = self.font.render(f"{self.score_left}   {self.score_right}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(score_text, score_rect)

        info_text = self.small_font.render("P: Pausar/Continuar |ESC: Sair", True, GRAY)
        self.screen.blit(info_text, (20, SCREEN_HEIGHT - 40))

        if self.paused and not self.game_over:
            pause_text = self.font.render("PAUSADO", True, WHITE)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(pause_text, pause_rect)

        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            winner_text = self.font.render(self.winner, True, WHITE)
            winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(winner_text, winner_rect)

            pygame.draw.rect(self.screen, DARK_GRAY, self.button_rect)
            pygame.draw.rect(self.screen, WHITE, self.button_rect, 2)

            button_text = self.small_font.render("Iniciar novo jogo", True, WHITE)
            button_text_rect = button_text.get_rect(center=self.button_rect.center)
            self.screen.blit(button_text, button_text_rect)

        pygame.display.flip()


pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

game = Game(screen, clock, font, small_font)
game.run()

pygame.quit()
