import sys
import pygame
import random
import json
from game_objects.py import reset_game, DrawGame, RandomizeFoodLocation, RandomizeSpecialFoodLocation, RandomizePinkFoodLocation, draw_walls, Snake, Food, SpecialFood, PinkFood, Score, FoodCollected

pygame.init()

# Load configuration from config.json
with open('config.json') as config_file:
    config_data = json.load(config_file)

Colors = {key: tuple(value) for key, value in config_data["Colors"].items()}
Config = config_data["Config"]
Config["background"] = Colors[Config["background"]]

EYE_SIZE = Config["BlockSize"] // 5
EYE_OFFSET = Config["BlockSize"] // 4

def GameOver(screen):
    font = pygame.font.SysFont(None, 75)
    text = font.render("Game Over", True, Colors["Black"])
    screen.blit(text, [Config["ScreenX"] // 2 - 150, Config["ScreenY"] // 2 - 50])
    pygame.display.update()
    pygame.time.wait(2000)

    # Add a restart button
    button_font = pygame.font.SysFont(None, 50)
    button_text = button_font.render("Restart", True, Colors["Black"])
    button_rect = button_text.get_rect(center=(Config["ScreenX"] // 2, Config["ScreenY"] // 2 + 50))
    pygame.draw.rect(screen, Colors["LightBlue"], button_rect.inflate(20, 10))
    screen.blit(button_text, button_rect)

    # Add a quit button
    quit_button_text = button_font.render("Quit Game", True, Colors["Black"])
    quit_button_rect = quit_button_text.get_rect(center=(Config["ScreenX"] // 2, Config["ScreenY"] // 2 + 120))
    pygame.draw.rect(screen, Colors["LightBlue"], quit_button_rect.inflate(20, 10))
    screen.blit(quit_button_text, quit_button_rect)

    pygame.display.update()

    # Wait for the user to click the restart or quit button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Exit the function to restart the game
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()  # Exit the game

def WinGame(screen):
    font = pygame.font.SysFont(None, 75)
    text = font.render("You Beat the Game!", True, Colors["Black"])
    screen.blit(text, [Config["ScreenX"] // 2 - 250, Config["ScreenY"] // 2 - 50])  # Adjusted x-coordinate to move text to the left
    pygame.display.update()

    fireworks = [{
        "x": random.randint(100, Config["ScreenX"] - 100),
        "y": random.randint(50, Config["ScreenY"] // 2 - 100),
        "particles": [{"x": 0, "y": 0, "dx": random.uniform(-2, 2), "dy": random.uniform(-2, 2), "life": 80, "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))} for _ in range(100)]
    } for _ in range(10)]

    for _ in range(500):  # Display fireworks for 500 frames
        screen.fill(Config["background"])
        screen.blit(text, [Config["ScreenX"] // 2 - 250, Config["ScreenY"] // 2 - 50])
        
        for firework in fireworks:
            for particle in firework["particles"]:
                particle["x"] += particle["dx"]
                particle["y"] += particle["dy"]
                particle["life"] -= 1
                if particle["life"] > 0:
                    pygame.draw.circle(screen, particle["color"], (int(firework["x"] + particle["x"]), int(firework["y"] + particle["y"])), 4)  # Increased particle size to 4
        
        pygame.display.update()
        pygame.time.delay(50)

    # Add a play again button
    button_font = pygame.font.SysFont(None, 50)
    button_text = button_font.render("Play Again?", True, Colors["Black"])
    button_rect = button_text.get_rect(center=(Config["ScreenX"] // 2, Config["ScreenY"] // 2 + 50))
    pygame.draw.rect(screen, Colors["LightBlue"], button_rect.inflate(20, 10))
    screen.blit(button_text, button_rect)

    # Add a quit button
    quit_button_text = button_font.render("Quit Game", True, Colors["Black"])
    quit_button_rect = quit_button_text.get_rect(center=(Config["ScreenX"] // 2, Config["ScreenY"] // 2 + 120))
    pygame.draw.rect(screen, Colors["LightBlue"], quit_button_rect.inflate(20, 10))
    screen.blit(quit_button_text, quit_button_rect)

    pygame.display.update()

    # Wait for the user to click the play again or quit button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Exit the function to restart the game
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()  # Exit the game

def PauseGame(screen):
    font = pygame.font.SysFont(None, 75)
    text = font.render("Game Paused", True, Colors["Black"])
    screen.blit(text, [Config["ScreenX"] // 2 - 200, Config["ScreenY"] // 2 - 50])
    pygame.display.update()

    # Wait for the user to unpause the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    return  # Exit the function to unpause the game

def handle_direction_change(event):
    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
        if Snake["Direction"] != "right":
            Snake["Direction"] = "left"
    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        if Snake["Direction"] != "left":
            Snake["Direction"] = "right"
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        if Snake["Direction"] != "down":
            Snake["Direction"] = "up"
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        if Snake["Direction"] != "up":
            Snake["Direction"] = "down"

def game_loop(screen, clock):
    global Score, FoodCollected
    direction_map = {
        "left": (-Config["BlockSize"], 0),
        "right": (Config["BlockSize"], 0),
        "up": (0, -Config["BlockSize"]),
        "down": (0, Config["BlockSize"]),
    }

    show_instructions = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if Snake["Direction"] == "none":
                    show_instructions = False  # Hide instructions when the snake starts moving
                handle_direction_change(event)
                if event.key == pygame.K_g:
                    PauseGame(screen)  # Pause the game when "g" is pressed

        if Snake["Direction"] != "none":
            new_head = [
                Snake["Body"][0][0] + direction_map[Snake["Direction"]][0],
                Snake["Body"][0][1] + direction_map[Snake["Direction"]][1]
            ]
            Snake["Body"].insert(0, new_head)

            ate_food = False
            for food in Food:
                if new_head == [food["X"], food["Y"]]:
                    print("You eat a Delicious Apple!")
                    Score += 1  # Increment score
                    Food.remove(food)
                    FoodCollected += 1
                    ate_food = True
                    break

            if not ate_food:
                for food in SpecialFood:
                    if new_head == [food["X"], food["Y"]]:
                        print("You eat a Special Food!")
                        Score += 2  # Increment score by 2
                        SpecialFood.remove(food)
                        FoodCollected += 1
                        # Add an extra block to the snake's length
                        Snake["Body"].append(Snake["Body"][-1])
                        Snake["Body"].append(Snake["Body"][-1])
                        ate_food = True
                        break

            if not ate_food:
                for food in PinkFood:
                    if new_head == [food["X"], food["Y"]]:
                        print("You eat a Pink Special Food!")
                        Score += 5  # Increment score by 5
                        PinkFood.remove(food)
                        FoodCollected += 1
                        # Add 5 extra blocks to the snake's length
                        for _ in range(5):
                            Snake["Body"].append(Snake["Body"][-1])
                        ate_food = True
                        break

            if not ate_food:
                Snake["Body"].pop()

            # Check if the food collected threshold is reached
            if FoodCollected >= Config["FoodCollectThreshold"]:
                RandomizeFoodLocation(Config, Colors)
                RandomizeSpecialFoodLocation(Config, Colors)
                RandomizePinkFoodLocation(Config, Colors)
                FoodCollected = 0  # Reset food collected counter

            # Check for winning condition
            if Score >= Config["WinningScore"]:
                WinGame(screen)
                return  # Exit the game loop to restart the game

            # Check for collision with the wall
            if (new_head[0] < Config["WallThickness"] or new_head[0] >= Config["ScreenX"] - Config["WallThickness"] or
                new_head[1] < Config["WallThickness"] or new_head[1] >= Config["ScreenY"] - Config["WallThickness"] or
                new_head in Snake["Body"][1:]):
                GameOver(screen)
                return  # Exit the game loop to restart the game

        DrawGame(screen, Config, Colors, show_instructions)
        clock.tick(Config["speed"])

def main():
    screen = pygame.display.set_mode([Config["ScreenX"], Config["ScreenY"]])
    clock = pygame.time.Clock()
    pygame.display.set_caption(Config["ScreenTitle"])
    pygame.display.update()

    while True:
        reset_game(Config, Colors)
        game_loop(screen, clock)

if __name__ == "__main__":
    main()