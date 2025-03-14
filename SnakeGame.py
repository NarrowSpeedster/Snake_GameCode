# The starting code for the Snake Game
# This code is a simple snake game that uses the Pygame library
# The game is a simple snake game where the player controls the snake to eat the food.
# The snake grows longer as it eats the food and the game ends when the snake hits the wall or itself.
# The player can control the snake using the arrow keys or the WASD keys.
# The player can restart the game by clicking the restart button after the game ends.
import sys
import pygame
import random

pygame.init()

Colors = {
    "MintyGreen": (40, 210, 180),
    "Red": (255, 0, 0),
    "LightBlue": (0, 128, 255),
    "Black": (0, 0, 0),
}

Config = {
    "ScreenX": 1000,
    "ScreenY": 900,
    "ScreenTitle": "Narrows Snake Game!",
    "background": Colors["MintyGreen"],
    "BlockSize": 10,  # Reverted block size back to 10 was 20
    "speed": 15,
}

def reset_game():
    global Snake, Food
    Snake = {
        "Body": [[Config["ScreenX"] // 2, Config["ScreenY"] // 2]],
        "Direction": "none",
        "Color": Colors["Red"],
    }
    Food = {
        "X": 0,
        "Y": 0,
        "Color": Colors["LightBlue"], 
    }
    RandomizeFoodLocation()

def RandomizeFoodLocation():
    while True:
        Food["X"] = round(random.randrange(0, Config["ScreenX"] - Config["BlockSize"], Config["BlockSize"]))
        Food["Y"] = round(random.randrange(0, Config["ScreenY"] - Config["BlockSize"], Config["BlockSize"]))
        if [Food["X"], Food["Y"]] not in Snake["Body"]:
            break

def DrawGame(screen):
    screen.fill(Config["background"])
    for segment in Snake["Body"]:
        pygame.draw.rect(screen, Snake["Color"], [segment[0], segment[1], Config["BlockSize"], Config["BlockSize"]])
    pygame.draw.rect(screen, Food["Color"], [Food["X"], Food["Y"], Config["BlockSize"], Config["BlockSize"]])
    pygame.display.update()

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
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Exit the function to restart the game
                if quit_button_rect.collidepoint(event.pos):
                    sys.exit()  # Exit the game

def game_loop(screen, clock):
    direction_map = {
        "left": (-Config["BlockSize"], 0),
        "right": (Config["BlockSize"], 0),
        "up": (0, -Config["BlockSize"]),
        "down": (0, Config["BlockSize"]),
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if Snake["Direction"] != "right":
                        Snake["Direction"] = "left"                
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if Snake["Direction"] != "left":
                        Snake["Direction"] = "right"              
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if Snake["Direction"] != "down":
                        Snake["Direction"] = "up"              
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if Snake["Direction"] != "up":
                        Snake["Direction"] = "down"

        if Snake["Direction"] != "none":
            new_head = [
                Snake["Body"][0][0] + direction_map[Snake["Direction"]][0],
                Snake["Body"][0][1] + direction_map[Snake["Direction"]][1]
            ]
            Snake["Body"].insert(0, new_head)

            if new_head == [Food["X"], Food["Y"]]:
                print("You eat a Delicious Apple!")
                RandomizeFoodLocation()
            else:
                Snake["Body"].pop()

            if (new_head[0] < 0 or new_head[0] >= Config["ScreenX"] or
                new_head[1] < 0 or new_head[1] >= Config["ScreenY"] or
                new_head in Snake["Body"][1:]):
                GameOver(screen)
                return  # Exit the game loop to restart the game

        DrawGame(screen)
        clock.tick(Config["speed"])

def main():
    screen = pygame.display.set_mode([Config["ScreenX"], Config["ScreenY"]])
    clock = pygame.time.Clock()
    pygame.display.set_caption(Config["ScreenTitle"])
    pygame.display.update()

    while True:
        reset_game()
        game_loop(screen, clock)

if __name__ == "__main__":
    main()