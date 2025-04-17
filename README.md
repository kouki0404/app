import pygame
import random
import sys

# =====================
# 設定
# =====================
WIDTH, HEIGHT = 800, 600
FPS = 60
FONT_SIZE = 48
NUM_COUNT = 5

# =====================
# 初期化
# =====================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("数字ハンター")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, FONT_SIZE)

# =====================
# 数字生成ルール
# =====================
def generate_rule():
    rule_type = random.choice(["random", "ordered"])

    if rule_type == "random":
        numbers = random.sample(range(1, 20), NUM_COUNT)
        rule_description = "好きな順に全ての数字をタップせよ"
        correct_sequence = numbers  # 任意順OK

    elif rule_type == "ordered":
        start = random.randint(1, 10)
        ordered = [start + i for i in range(NUM_COUNT)]
        if random.choice([True, False]):
            ordered.reverse()
            rule_description = "数字を大きい順にタップせよ"
        else:
            rule_description = "数字を小さい順にタップせよ"
        numbers = ordered.copy()
        random.shuffle(numbers)
        correct_sequence = ordered

    return {
        "rule_type": rule_type,
        "numbers": numbers,
        "correct_sequence": correct_sequence,
        "description": rule_description
    }

# =====================
# 数字スプライトクラス
# =====================
class NumberSprite(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.number = number
        self.image = font.render(str(number), True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(50, WIDTH - 50),
            random.randint(50, HEIGHT - 50)
        )
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.vx *= -1
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.vy *= -1

# =====================
# ゲーム準備
# =====================
rule = generate_rule()
number_sprites = pygame.sprite.Group()

for n in rule["numbers"]:
    number_sprites.add(NumberSprite(n))

tap_index = 0  # 現在のターゲット（ordered用）

# =====================
# メインループ
# =====================
running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for sprite in number_sprites:
                if sprite.rect.collidepoint(pos):
                    selected = sprite.number
                    if rule["rule_type"] == "random":
                        number_sprites.remove(sprite)
                    elif rule["rule_type"] == "ordered":
                        if selected == rule["correct_sequence"][tap_index]:
                            number_sprites.remove(sprite)
                            tap_index += 1
                    break

    number_sprites.update()
    number_sprites.draw(screen)

    # ルール表示
    rule_text = font.render(rule["description"], True, (255, 255, 0))
    screen.blit(rule_text, (20, 20))

    # クリア判定
    if len(number_sprites) == 0:
        clear_text = font.render("クリア！", True, (0, 255, 0))
        screen.blit(clear_text, (WIDTH//2 - 80, HEIGHT//2 - 40))

    pygame.display.flip()

pygame.quit()
sys.exit()


