# все константы игры

WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
FPS = 10

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 80)
DARK_GREEN = (0, 140, 50)
RED  = (220, 50, 50)
DARK_RED = (120, 0, 0)
BLUE = (50, 130, 255)
YELLOW = (255, 220, 0)
ORANGE = (255, 140, 0)
PURPLE = (160, 50, 220)
GRAY = (80, 80, 80)
DARK_GRAY = (30, 30, 30)
LIGHT_GRAY= (180, 180, 180)
CYAN= (0, 220, 220)
BG_COLOR = (15, 15, 25)

# Игровые параметры
FOOD_LIFETIME= 7      # секунд до исчезновения еды
POWERUP_LIFETIME = 8000   # мс до исчезновения пауэрапа
POWERUP_DURATION = 5000   # мс действия пауэрапа
BASE_SPEED = 8
SPEED_INCREMENT = 1
SCORE_PER_LEVEL = 5
OBSTACLE_START_LEVEL= 3
OBSTACLE_COUNT = 5      # блоков за уровень

# Веса очков для разных типов еды
FOOD_WEIGHTS = {
    'normal': 1,
    'big':    3,
    'tiny':   2,
}