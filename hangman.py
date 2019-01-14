import pygame
from models import Base, Word, Category, engine, Session
import random
from time import sleep

def build_caregory_buttons(screen, font, button_color, text_color):
    buttons = []
    categories = [cat.name for cat in Session.query(Category).all()]
    for category in categories:
        buttons.append(pygame.Rect(1, 1 + categories.index(category) * 53, 200, 50))
    for button in buttons:
        pygame.draw.rect(screen, button_color, button)  # draw button
        screen.blit(font.render(categories[buttons.index(button)], True, text_color),
                    (button.x + 5, button.y + 5))
    return buttons, categories


def draw_hangpost(screen):
    rect = pygame.Rect(50, 300, 50, 10)
    pygame.draw.rect(screen, (0, 0, 0), rect)

    rect = pygame.Rect(110, 300, 50, 10)
    pygame.draw.rect(screen, (0, 0, 0), rect)

    rect = pygame.Rect(100, 100, 10, 200)
    pygame.draw.rect(screen, (0, 0, 0), rect)

    rect = pygame.Rect(100, 100, 120, 10)
    pygame.draw.rect(screen, (0, 0, 0), rect)

    rect = pygame.Rect(220, 100, 10, 20)
    pygame.draw.rect(screen, (0, 0, 0), rect)


def draw_head(screen):
    pygame.draw.circle(screen, (0, 0, 0), (225, 139), 20, 3)


def draw_body(screen):
    rect = pygame.Rect(224, 159, 3, 100)
    pygame.draw.rect(screen, (0, 0, 0), rect)


def draw_left_hand(screen):
    rect = pygame.Rect(224, 165, 30, 3)
    pygame.draw.rect(screen, (0, 0, 0), rect)


def draw_right_hand(screen):
    rect = pygame.Rect(195, 165, 30, 3)
    pygame.draw.rect(screen, (0, 0, 0), rect)


def draw_left_foot(screen):
    rect = pygame.Rect(224, 256, 30, 3)
    pygame.draw.rect(screen, (0, 0, 0), rect)


def draw_right_foot(screen):
    rect = pygame.Rect(195, 256, 30, 3)
    pygame.draw.rect(screen, (0, 0, 0), rect)


def main():
    Base.metadata.create_all(engine)
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    size = [800, 600]
    bg = [255, 255, 255]
    screen = pygame.display.set_mode(size)
    intro = True
    game = False
    success = False
    fail = False
    word = ""
    hangman_func = []
    used_letters = []
    button_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    text_color = (255 - button_color[0], 255 - button_color[1], 255 - button_color[2])
    font = pygame.font.SysFont('Arial', 25)
    while True:
        if intro:
            screen.fill(bg)
            buttons, categories = build_caregory_buttons(screen, font, button_color, text_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # gets mouse position

                    # checks if mouse position is over the button
                    for button in buttons:
                        if button.collidepoint(mouse_pos):
                            intro = False
                            game = True
                            category = categories[buttons.index(button)]
        elif game:
            screen.fill(bg)
            draw_hangpost(screen)
            used_letters.sort()
            for letter in used_letters:
                screen.blit(
                    font.render(letter, True, (0, 0, 0)),
                    (400 + 40 * used_letters.index(letter), 10)
                )
            for hangman in hangman_func:
                hangman(screen)
            if type(category) is not Category:
                category = Session.query(Category).filter(Category.name == category).first()
                words = [(word, False) for word in Session.query(Word).filter(Word.category_id == category.id)]
            if not word:
                draw_hangman = [draw_head,
                                draw_body,
                                draw_left_hand,
                                draw_right_hand,
                                draw_left_foot,
                                draw_right_foot]
                used_letters = []
                word = words[random.randint(0, len(words)-1)]
                letters = [(letter, False) for letter in word[0].word]
            i = 0
            for letter in letters:
                if not letter[1]:
                    rect = pygame.Rect(300+40*i, 300, 30, 3)
                    pygame.draw.rect(screen, (0, 0, 0), rect)
                else:
                    screen.blit(
                        font.render(letter[0], True, (0,0,0)),
                        (300+40*i, 300)
                    )
                i+=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.name(event.key)
                    if key in [letter[0] for letter in letters]:
                        letters = [(letter[0], True) if letter[0] == key else letter for letter in letters]
                        unknown_count = [letter for letter in letters if letter[1] is False]
                        if not unknown_count:
                            game = False
                            success = True
                    else:
                        if draw_hangman:
                            hangman_func.append(draw_hangman[0])
                            draw_hangman.pop(0)
                            if not draw_hangman:
                                game = False
                                fail = True
                        else:
                            pygame.quit()
                    if key not in used_letters:
                        used_letters.append(key)
        elif success:
            screen.fill(bg)
            screen.blit(font.render('You won', True, (0,255,0)), (350, 250))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
        elif fail:
            screen.fill(bg)
            screen.blit(font.render('You lost', True, (255,0,0)), (350, 250))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
        pygame.display.update()
        clock.tick(fps)
        #sleep(0.01)


if __name__ == '__main__':
    main()