import pygame # Импортируем библиотеку Pygame для работы с графикой и звуком
import random # Импортируем модуль random для генерации случайных чисел
import sys # Импортируем модуль sys для работы с параметрами командной строки и системными функциями
import time  # Импортируем модуль time для работы с временем и задержками

# Инициализация Pygame
pygame.init()


WIDTH, HEIGHT = 1800, 900  #размер экрана
FPS = 60
PLAYER_SIZE = 50 
PLAYER_SPEED = 8 
SQUARE_SIZE = 10  # Размер маленьких квадратиков
NUM_SQUARES = 150  # Количество маленьких квадратиков

# Создание шрифта для отображения времени и счётчика с размером 48 и 36
TIME_FONT = pygame.font.Font(None, 48)
SCORE_FONT = pygame.font.Font(None, 36)

# Цвета
BLACK = (255, 255, 255)
WHITE = (255, 255, 255)
RED = (255, 102, 102)
BLUE = (102, 102, 255)
GREEN = (153, 0, 76)


def load_and_scale_image(file_name, size): # функция
    # Загружаем изображение из файла с указанным именем
    image = pygame.image.load(file_name) 
    # Изменяем размер изображения до заданного размера и возвращаем его
    return pygame.transform.scale(image, size)


background_image = load_and_scale_image('gamemenu.jpg', (WIDTH, HEIGHT))
first_image = load_and_scale_image('start1.png', (200, 100))
second_image = load_and_scale_image('exit.jpg', (200, 100))
reset_image = load_and_scale_image('back_.png', (200, 100))

# Создаем окно игры с заданными размерами WIDTH и HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Устанавливаем заголовок окна игры
pygame.display.set_caption('Eat to win')

# Игроки
player1_x = 100
player1_y = HEIGHT - 50 - PLAYER_SIZE - 50  # 50px отступ снизу, 50px высота игрока
player2_x = player1_x + PLAYER_SIZE + 10
player2_y = player1_y

# создание пустого списка[] для маленьких квадратиков
small_squares = []

# Счетчики очков
player1_score = 0
player2_score = 0

# Эта строка кода сохраняет текущее время в секундах
start_time = time.time()
game_duration = 21  # секунды

# Пока игра не началась, переменная будет иметь значение False
game_started = False
# Этот объект помогает управлять частотой кадров (FPS) 
clock = pygame.time.Clock()


def generate_small_squares():
    # Создаем пустой список для хранения координат квадратов
    squares = []
    # Генерируем NUM_SQUARES квадратов
    for _ in range(NUM_SQUARES):
         # Генерируем случайное значение x в пределах ширины окна
        x = random.randint(0, WIDTH - SQUARE_SIZE)
        # Генерируем случайное значение y в пределах высоты окна
        y = random.randint(0, HEIGHT - SQUARE_SIZE)
        # Добавляем координаты квадрата в список
        squares.append((x, y))
    return squares

def main():
    # Объявляем переменные как глобальные, чтобы их можно было использовать в этой функции
    global player1_x, player1_y, player2_x, player2_y, game_started, small_squares
    global player1_score, player2_score, start_time

    running = True
    while running:
        for event in pygame.event.get(): # Перебираем все события, происходящие в текущем игровом цикле
            if event.type == pygame.QUIT:  # Проверяем, если событие "закрытия окна"
                pygame.quit() # Корректно завершаем Pygame
                sys.exit() # Выходим из программы

            if event.type == pygame.MOUSEBUTTONDOWN: # Проверяем, произошло ли нажатие кнопки мыши
                mouse_x, mouse_y = event.pos  # Получаем координаты курсора мыши в момент нажатия

                # Проверяем, не начата ли игра и было ли нажато на первую картинку
                if not game_started and first_image.get_rect(topleft=(WIDTH // 3 - 50, HEIGHT - 150)).collidepoint(mouse_x, mouse_y):
                    change_background() # Если условия выполняются, меняем фон игры

                    # Проверяем, было ли нажатие на вторую картинку
                elif not game_started and second_image.get_rect(topleft=(WIDTH // 2 + 100, HEIGHT - 150)).collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()
                    # Проверяем, была ли нажатие на кнопку сброса во время игры
                elif game_started and reset_image.get_rect(topleft=(10, 10)).collidepoint(mouse_x, mouse_y):
                    reset_background()  # Если да, то сбрасываем фон или игровое состояние

        if game_started:
            # Вычисляем время, прошедшее с начала игры
            elapsed_time = time.time() - start_time
            # Вычисляем оставшееся время, гарантируя, что оно не будет отрицательным
            remaining_time = max(0, game_duration - elapsed_time)

# Если время истекло, показываем экран завершения игры и выходим
            if remaining_time <= 0:
                show_end_screen()
                pygame.quit()
                sys.exit()

# Обрабатываем движение игрока
            handle_player_movement()
 # Проверяем столкновения объектов
            check_collisions()
# Рисуем элементы на экране
        draw()


def handle_player_movement():
    global player1_x, player1_y, player2_x, player2_y

 # Получаем текущее состояние всех клавиш
    keys = pygame.key.get_pressed()
    # Создаем словарь для управления движением первого игрока
    player1_movement = {
        pygame.K_w: (0, -PLAYER_SPEED),
        pygame.K_s: (0, PLAYER_SPEED),
        pygame.K_a: (-PLAYER_SPEED, 0),
        pygame.K_d: (PLAYER_SPEED, 0)
    }

# Проходим по всем клавишам, которые могут управлять движением игрока 1
    for key, (dx, dy) in player1_movement.items():
        # Если соответствующая клавиша нажата
        if keys[key]:
             # Обновляем координаты игрока 1, ограничивая их границами экрана
            player1_x = max(0, min(WIDTH - PLAYER_SIZE, player1_x + dx))
            player1_y = max(0, min(HEIGHT - PLAYER_SIZE, player1_y + dy))

# Определяем движения для игрока 2
    player2_movement = {
        pygame.K_UP: (0, -PLAYER_SPEED),
        pygame.K_DOWN: (0, PLAYER_SPEED),
        pygame.K_LEFT: (-PLAYER_SPEED, 0),
        pygame.K_RIGHT: (PLAYER_SPEED, 0)
    }

    for key, (dx, dy) in player2_movement.items():
        if keys[key]:
            player2_x = max(0, min(WIDTH - PLAYER_SIZE, player2_x + dx))
            player2_y = max(0, min(HEIGHT - PLAYER_SIZE, player2_y + dy))


def check_collisions():
    global player1_score, player2_score
     # Проходим по всем квадратам в списке small_squares
    for square in small_squares[:]:
        # Создаем прямоугольник для текущего квадрата
        square_rect = pygame.Rect(square[0], square[1], SQUARE_SIZE, SQUARE_SIZE)
         # Создаем прямоугольники для игроков
        player1_rect = pygame.Rect(player1_x, player1_y, PLAYER_SIZE, PLAYER_SIZE)
        player2_rect = pygame.Rect(player2_x, player2_y, PLAYER_SIZE, PLAYER_SIZE)

 # Проверяем столкновение первого игрока с квадратом
        if player1_rect.colliderect(square_rect):
             # Удаляем квадрат из списка и увеличиваем счет первого игрока
            small_squares.remove(square)
            player1_score += 1
             # Проверяем столкновение второго игрока с квадратом
        elif player2_rect.colliderect(square_rect):
            # Удаляем квадрат из списка и увеличиваем счет второго игрока
            small_squares.remove(square)
            player2_score += 1

def draw():
    # Отображаем фоновое изображение на экране
    screen.blit(background_image, (0, 0))
    
      # Если игра не начата, отображаем кнопки для начала игры
    if not game_started:
        screen.blit(first_image, (WIDTH // 3 - 50, HEIGHT - 150))  # Кнопка для старта
        screen.blit(second_image, (WIDTH // 2 + 100, HEIGHT - 150)) # Кнопка для выхода
    else:
        # Если игра начата, отображаем кнопку сброса
        screen.blit(reset_image, (10, 10))
        # Рисуем прямоугольник для первого игрока (красный)
        pygame.draw.rect(screen, RED, (player1_x, player1_y, PLAYER_SIZE, PLAYER_SIZE))
          # Рисуем прямоугольник для второго игрока (синий)
        pygame.draw.rect(screen, BLUE, (player2_x, player2_y, PLAYER_SIZE, PLAYER_SIZE))

 # Рисуем маленькие квадраты (цели) на экране
        for square in small_squares:
            pygame.draw.rect(screen, GREEN, (square[0], square[1], SQUARE_SIZE, SQUARE_SIZE))
# Отображаем счет первого игрока
        player1_score_text = SCORE_FONT.render(f"RED Score: {player1_score}", True, BLACK)
         # Отображаем счет второго игрока
        player2_score_text = SCORE_FONT.render(f"BLUE Score: {player2_score}", True, BLACK)
        screen.blit(player1_score_text, (10, HEIGHT - 40))
        screen.blit(player2_score_text, (WIDTH - player2_score_text.get_width() - 10, HEIGHT - 40))

 # Вычисляем и отображаем оставшееся время
        elapsed_time = time.time() - start_time
        remaining_time = max(0, game_duration - elapsed_time)
        time_text = TIME_FONT.render(f"Time: {int(remaining_time)}", True, BLACK)
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 10))

# Обновляем экран, чтобы отобразить все изменения
    pygame.display.flip()
    # Ограничиваем количество кадров в секунду
    clock.tick(FPS)

def show_end_screen():
    global player1_score, player2_score

    # Заполнение экрана белым цветом
    screen.fill(WHITE)

   # Проверяем, если счёт игрока 1 больше счёта игрока 2
    if player1_score > player2_score:
        # Загружаем изображение, показывающее победу игрока 1 (красного)
        end_image = load_and_scale_image('redwin.jpg', (WIDTH, HEIGHT))
    elif player2_score > player1_score:
        end_image = load_and_scale_image('bluewin.jpg', (WIDTH, HEIGHT))
    else:
        end_image = load_and_scale_image('twowin.jpg', (WIDTH, HEIGHT))

 # Отображаем изображение на экране
    screen.blit(end_image, (0, 0))
    # Обновляем экран, чтобы отобразить изменения
    pygame.display.flip()
     # Приостанавливаем выполнение программы на 5 секунд
    time.sleep(5)

    

def change_background():
    global background_image, game_started, small_squares, start_time
    # Загружаем и изменяем размер изображения фона
    background_image = load_and_scale_image('background.jpg', (WIDTH, HEIGHT))
    game_started = True
     # Генерируем маленькие квадраты и сохраняем их в переменной
    small_squares = generate_small_squares()
     # Запоминаем текущее время как время начала игры
    start_time = time.time()

#для кнопки back
def reset_background():
    global background_image, game_started, small_squares, player1_score, player2_score
    # Загружаем изображение фона для меню игры
    background_image = load_and_scale_image('gamemenu.jpg', (WIDTH, HEIGHT))
    game_started = False
    # Очищаем список маленьких квадратов
    small_squares = []
    # Сбрасываем счетчики
    player1_score = 0
    player2_score = 0

if __name__ == "__main__":
     # Запускаем основную функцию
    main()