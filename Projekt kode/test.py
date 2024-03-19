import pygame
import requests
import random
import html
from urllib.parse import unquote

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trivia Game")

# Define font
font = pygame.font.SysFont(None, 30)

def get_question_pool(amount, category):
    url = f"https://opentdb.com/api.php?amount={amount}&category={category}&difficulty=easy&type=multiple&encode=url3986"
    response = requests.get(url)
    response_json = response.json()
    return response_json['results']

def shuffle_choices(choices):
    random.shuffle(choices)
    return choices

def print_choices(choices):
    for choice_index, choice in enumerate(choices):
        text = font.render(f"{choice_index+1}. {html.unescape(choice)}", True, BLACK)
        screen.blit(text, (50, 150 + 50 * choice_index))

def get_user_choice():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 0
                elif event.key == pygame.K_2:
                    return 1
                elif event.key == pygame.K_3:
                    return 2
                elif event.key == pygame.K_4:
                    return 3

def play_game(amount, category):
    question_pool = get_question_pool(amount, category)
    for question in question_pool:
        question_text = unquote(question["question"])
        screen.fill(WHITE)
        text = font.render(question_text, True, BLACK)
        screen.blit(text, (50, 50))
        choices = [unquote(choice) for choice in question["incorrect_answers"]]
        choices.append(unquote(question["correct_answer"]))
        shuffled_choices = shuffle_choices(choices)
        print_choices(shuffled_choices)
        pygame.display.update()
        user_choice_index = get_user_choice()
        user_choice_text = shuffled_choices[user_choice_index]
        correct_choice_text = unquote(question["correct_answer"])
        if user_choice_text == correct_choice_text:
            result_text = font.render(f"Correct! The correct answer is: {correct_choice_text}", True, BLACK)
        else:
            result_text = font.render(f"Incorrect! The correct answer is: {correct_choice_text}", True, BLACK)
        screen.blit(result_text, (50, 500))
        pygame.display.update()
        pygame.time.wait(2000)  # Pause for 2 seconds before showing the next question


