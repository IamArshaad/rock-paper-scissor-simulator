import pygame
import random
import math

# Initialize
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissor Simulation")

# Load and resize images
ICON_SIZE = 32
rock_img = pygame.image.load("rock.png").convert_alpha()
paper_img = pygame.image.load("paper.png").convert_alpha()
scissor_img = pygame.image.load("scissor.png").convert_alpha()

rock_img = pygame.transform.scale(rock_img, (ICON_SIZE, ICON_SIZE))
paper_img = pygame.transform.scale(paper_img, (ICON_SIZE, ICON_SIZE))
scissor_img = pygame.transform.scale(scissor_img, (ICON_SIZE, ICON_SIZE))

# Colors
WHITE = (255, 255, 255)
BUTTON_COLOR = (40, 80, 160)   # classy dark blue
BUTTON_BORDER = (80, 120, 200)
GRAY = (200, 200, 200)
DARK_BG = (0, 0, 0)

class Entity:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

        speed = random.uniform(1.5, 2.5)
        angle = random.uniform(0, 2 * math.pi)
        while math.isclose(math.cos(angle), 0, abs_tol=0.2) or math.isclose(math.sin(angle), 0, abs_tol=0.2):
            angle = random.uniform(0, 2 * math.pi)

        self.vel_x = math.cos(angle) * speed
        self.vel_y = math.sin(angle) * speed
        self.update_image()

    def update_image(self):
        if self.type == "rock":
            self.image = rock_img
        elif self.type == "paper":
            self.image = paper_img
        else:
            self.image = scissor_img

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y
        if self.x <= 0 or self.x >= WIDTH - ICON_SIZE:
            self.vel_x *= -1
        if self.y <= 0 or self.y >= HEIGHT - ICON_SIZE:
            self.vel_y *= -1

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def collide(self, other):
        distance = math.hypot(self.x - other.x, self.y - other.y)
        return distance < ICON_SIZE

    def transform(self, other):
        if self.type == "rock" and other.type == "paper":
            self.type = "paper"
        elif self.type == "paper" and other.type == "rock":
            other.type = "paper"
        elif self.type == "paper" and other.type == "scissor":
            self.type = "scissor"
        elif self.type == "scissor" and other.type == "paper":
            other.type = "scissor"
        elif self.type == "scissor" and other.type == "rock":
            self.type = "rock"
        elif self.type == "rock" and other.type == "scissor":
            other.type = "rock"
        self.update_image()
        other.update_image()

def draw_start_screen():
    screen.fill(DARK_BG)
    font_big = pygame.font.SysFont("arial", 72)
    font_small = pygame.font.SysFont("arial", 36)

    title = font_big.render("Rock, Paper, Scissor", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 160))

    # Classy button
    button_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 30, 300, 70)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=12)
    pygame.draw.rect(screen, BUTTON_BORDER, button_rect, 3, border_radius=12)

    font_btn = pygame.font.SysFont("arial", 36)
    btn_text = font_btn.render("Let the battle begin", True, WHITE)
    screen.blit(btn_text, (WIDTH//2 - btn_text.get_width()//2, HEIGHT//2 - 20))

def draw_setup_screen():
    screen.fill(DARK_BG)
    # Place icons statically on edges
    screen.blit(rock_img, (WIDTH - ICON_SIZE, HEIGHT//2 - ICON_SIZE//2))
    screen.blit(paper_img, (WIDTH//2 - ICON_SIZE//2, HEIGHT - ICON_SIZE))
    screen.blit(scissor_img, (0, HEIGHT//2 - ICON_SIZE//2))

    # Classy start button
    button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 30, 200, 60)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=12)
    pygame.draw.rect(screen, BUTTON_BORDER, button_rect, 3, border_radius=12)

    font_btn = pygame.font.SysFont("arial", 32)
    btn_text = font_btn.render("Start", True, WHITE)
    screen.blit(btn_text, (WIDTH//2 - btn_text.get_width()//2, HEIGHT//2 - 15))

def check_winner(entities):
    types = set(e.type for e in entities)
    if len(types) == 1:
        return types.pop()
    return None

def spawn_entities():
    entities = []
    for _ in range(7):
        x = WIDTH - ICON_SIZE
        y = HEIGHT // 2 + random.randint(-50, 50)
        entities.append(Entity(x, y, "rock"))
    for _ in range(7):
        x = WIDTH // 2 + random.randint(-50, 50)
        y = HEIGHT - ICON_SIZE
        entities.append(Entity(x, y, "paper"))
    for _ in range(6):
        x = 0
        y = HEIGHT // 2 + random.randint(-50, 50)
        entities.append(Entity(x, y, "scissor"))
    return entities

def main():
    clock = pygame.time.Clock()
    running = True
    mode = "intro"
    entities = []
    winner = None

    while running:
        screen.fill(DARK_BG)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if mode == "intro" and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if WIDTH//2 - 150 < mx < WIDTH//2 + 150 and HEIGHT//2 - 30 < my < HEIGHT//2 + 40:
                    mode = "setup"
            elif mode == "setup" and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if WIDTH//2 - 100 < mx < WIDTH//2 + 100 and HEIGHT//2 - 30 < my < HEIGHT//2 + 30:
                    mode = "running"
                    entities = spawn_entities()
                    winner = None
            elif winner and event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if WIDTH//2 - 100 < mx < WIDTH//2 + 100 and HEIGHT//2 + 40 < my < HEIGHT//2 + 100:
                    mode = "setup"

        if mode == "intro":
            draw_start_screen()
        elif mode == "setup":
            draw_setup_screen()
        elif mode == "running":
            if not winner:
                winner = check_winner(entities)
                for e in entities:
                    e.move()
                    e.draw()
                for i in range(len(entities)):
                    for j in range(i+1, len(entities)):
                        if entities[i].collide(entities[j]):
                            entities[i].transform(entities[j])
            else:
                font = pygame.font.SysFont(None, 60)
                text = font.render(f"{winner.upper()} wins!", True, WHITE)
                screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 30))

                pygame.draw.rect(screen, GRAY, (WIDTH//2 - 100, HEIGHT//2 + 40, 200, 60), border_radius=12)
                font_btn = pygame.font.SysFont(None, 40)
                btn_text = font_btn.render("Try Again", True, (0, 0, 0))
                screen.blit(btn_text, (WIDTH//2 - btn_text.get_width()//2, HEIGHT//2 + 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
