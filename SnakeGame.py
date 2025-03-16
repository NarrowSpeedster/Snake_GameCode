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
    "Green": (0, 255, 0),  # Green color for the snake body
    "LightBlue": (0, 128, 255),
    "Black": (0, 0, 0),
    "White": (255, 255, 255),
    "Gray": (128, 128, 128),  # Gray color for the tail
    "Yellow": (255, 255, 0),  # Yellow color for the special food
    "Pink": (255, 105, 180),  # Pink color for the new special food
}

Config = {
    "ScreenX": 1000,
    "ScreenY": 900,
    "ScreenTitle": "Narrows Snake Game!",
    "background": Colors["MintyGreen"],
    "BlockSize": 10,  # Reverted block size back to 10 was 20
    "speed": 15,
    "WallThickness": 10,  # Thickness of the black wall
    "SpecialFoodChance": 0.2,  # 20% chance for special food to appear
    "PinkFoodChance": 0.1,  # 10% chance for pink special food to appear
}

def reset_game():
    global Snake, Food, SpecialFood, PinkFood, Score
    Snake = {
        "Body": [[Config["ScreenX"] // 2, Config["ScreenY"] // 2]],
        "Direction": "none",
        "Color": Colors["Green"],  # Changed snake body color to green
    }
    Food = {
        "X": 0,
        "Y": 0,
        "Color": Colors["LightBlue"], 
    }
    SpecialFood = {
        "X": -1,  # Initialize off-screen
        "Y": -1,
        "Color": Colors["Yellow"], 
    }
    PinkFood = {
        "X": -1,  # Initialize off-screen
        "Y": -1,
        "Color": Colors["Pink"], 
    }
    Score = 0  # Initialize score
    RandomizeFoodLocation()

def RandomizeFoodLocation():
    while True:
        Food["X"] = round(random.randrange(Config["WallThickness"], Config["ScreenX"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
        Food["Y"] = round(random.randrange(Config["WallThickness"], Config["ScreenY"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
        if [Food["X"], Food["Y"]] not in Snake["Body"]:
            break

def RandomizeSpecialFoodLocation():
    while True:
        SpecialFood["X"] = round(random.randrange(Config["WallThickness"], Config["ScreenX"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
        SpecialFood["Y"] = round(random.randrange(Config["WallThickness"], Config["ScreenY"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
        if [SpecialFood["X"], SpecialFood["Y"]] not in Snake["Body"] and [SpecialFood["X"], SpecialFood["Y"]] != [Food["X"], Food["Y"]]:
            break

def RandomizePinkFoodLocation():
    while True:
        PinkFood["X"] = round(random.randrange(Config["WallThickness"], Config["ScreenX"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
        PinkFood["Y"] = round(random.randrange(Config["WallThickness"], Config["ScreenY"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
        if [PinkFood["X"], PinkFood["Y"]] not in Snake["Body"] and [PinkFood["X"], PinkFood["Y"]] != [Food["X"], Food["Y"]] and [PinkFood["X"], PinkFood["Y"]] != [SpecialFood["X"], SpecialFood["Y"]]:
            break

def DrawGame(screen):
    screen.fill(Config["background"])
    
    # Draw the black wall around the edges
    pygame.draw.rect(screen, Colors["Black"], [0, 0, Config["ScreenX"], Config["WallThickness"]])  # Top wall
    pygame.draw.rect(screen, Colors["Black"], [0, 0, Config["WallThickness"], Config["ScreenY"]])  # Left wall
    pygame.draw.rect(screen, Colors["Black"], [0, Config["ScreenY"] - Config["WallThickness"], Config["ScreenX"], Config["WallThickness"]])  # Bottom wall
    pygame.draw.rect(screen, Colors["Black"], [Config["ScreenX"] - Config["WallThickness"], 0, Config["WallThickness"], Config["ScreenY"]])  # Right wall

    for i, segment in enumerate(Snake["Body"]):
        if i == len(Snake["Body"]) - 1:
            color = Colors["Gray"]  # Draw the tail in gray
        else:
            color = Snake["Color"]
        pygame.draw.rect(screen, color, [segment[0], segment[1], Config["BlockSize"], Config["BlockSize"]])
    
    # Draw eyes on the snake's head
    head = Snake["Body"][0]
    eye_size = Config["BlockSize"] // 5
    eye_offset = Config["BlockSize"] // 4

    if Snake["Direction"] == "left":
        eye_positions = [
            (head[0] - eye_offset, head[1] + eye_offset),
            (head[0] - eye_offset, head[1] + Config["BlockSize"] - eye_offset)
        ]
    elif Snake["Direction"] == "right":
        eye_positions = [
            (head[0] + Config["BlockSize"] + eye_offset, head[1] + eye_offset),
            (head[0] + Config["BlockSize"] + eye_offset, head[1] + Config["BlockSize"] - eye_offset)
        ]
    elif Snake["Direction"] == "up":
        eye_positions = [
            (head[0] + eye_offset, head[1] - eye_offset),
            (head[0] + Config["BlockSize"] - eye_offset, head[1] - eye_offset)
        ]
    elif Snake["Direction"] == "down":
        eye_positions = [
            (head[0] + eye_offset, head[1] + Config["BlockSize"] + eye_offset),
            (head[0] + Config["BlockSize"] - eye_offset, head[1] + Config["BlockSize"] + eye_offset)
        ]
    else:
        eye_positions = []

    for pos in eye_positions:
        pygame.draw.circle(screen, Colors["White"], pos, eye_size)

    pygame.draw.rect(screen, Food["Color"], [Food["X"], Food["Y"], Config["BlockSize"], Config["BlockSize"]])
    if SpecialFood["X"] != -1 and SpecialFood["Y"] != -1:
        pygame.draw.rect(screen, SpecialFood["Color"], [SpecialFood["X"], SpecialFood["Y"], Config["BlockSize"], Config["BlockSize"]])
    if PinkFood["X"] != -1 and PinkFood["Y"] != -1:
        pygame.draw.rect(screen, PinkFood["Color"], [PinkFood["X"], PinkFood["Y"], Config["BlockSize"], Config["BlockSize"]])

    # Display the score
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f"Score: {Score}", True, Colors["Black"])
    screen.blit(score_text, [10, 10])

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
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return  # Exit the function to restart the game
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()  # Exit the game

def game_loop(screen, clock):
    global Score
    direction_map = {
        "left": (-Config["BlockSize"], 0),
        "right": (Config["BlockSize"], 0),
        "up": (0, -Config["BlockSize"]),
        "down": (0, Config["BlockSize"]),
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
                Score += 1  # Increment score
                RandomizeFoodLocation()
                # Chance for special food to appear
                if random.random() < Config["SpecialFoodChance"]:
                    RandomizeSpecialFoodLocation()
                # Chance for pink special food to appear
                if random.random() < Config["PinkFoodChance"]:
                    RandomizePinkFoodLocation()
            elif new_head == [SpecialFood["X"], SpecialFood["Y"]]:
                print("You eat a Special Food!")
                Score += 2  # Increment score by 2
                SpecialFood["X"], SpecialFood["Y"] = -1, -1  # Remove special food from screen
                # Add an extra block to the snake's length
                Snake["Body"].append(Snake["Body"][-1])
                Snake["Body"].append(Snake["Body"][-1])
            elif new_head == [PinkFood["X"], PinkFood["Y"]]:
                print("You eat a Pink Special Food!")
                Score += 5  # Increment score by 5
                PinkFood["X"], PinkFood["Y"] = -1, -1  # Remove pink special food from screen
                # Add 5 extra blocks to the snake's length
                for _ in range(5):
                    Snake["Body"].append(Snake["Body"][-1])
            else:
                Snake["Body"].pop()

            # Check for collision with the wall
            if (new_head[0] < Config["WallThickness"] or new_head[0] >= Config["ScreenX"] - Config["WallThickness"] or
                new_head[1] < Config["WallThickness"] or new_head[1] >= Config["ScreenY"] - Config["WallThickness"] or
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