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
    "Red": (255, 0, 0),  # Red color for the tongue
}

Config = {
    "ScreenX": 1000,
    "ScreenY": 900,
    "ScreenTitle": "Narrows Snake Game!",
    "background": Colors["MintyGreen"],
    "BlockSize": 10,  # Reverted block size back to 10 was 20
    "speed": 15,
    "WallThickness": 10,  # Thickness of the black wall
    "SpecialFoodChance": 0.75,  # Increased to 75% chance for special food to appear
    "PinkFoodChance": 0.5,  # Increased to 50% chance for pink special food to appear
    "FoodCount": 30,  # Number of regular food items
    "SpecialFoodCount": 14,  # Number of special food items (increased by 600%)
    "PinkFoodCount": 7,  # Number of pink special food items (increased by 600%)
    "FoodCollectThreshold": 25,  # Number of food items to collect before randomizing locations
    "WinningScore": 100,  # Score needed to win the game
}

def reset_game():
    global Snake, Food, SpecialFood, PinkFood, Score, FoodCollected
    Snake = {
        "Body": [[Config["ScreenX"] // 2, Config["ScreenY"] // 2]],
        "Direction": "none",
        "Color": Colors["Green"],  # Changed snake body color to green
    }
    Food = []
    SpecialFood = []
    PinkFood = []
    Score = 0  # Initialize score
    FoodCollected = 0  # Initialize food collected counter
    RandomizeFoodLocation()
    RandomizeSpecialFoodLocation()
    RandomizePinkFoodLocation()

def RandomizeFoodLocation():
    Food.clear()
    for _ in range(Config["FoodCount"]):
        while True:
            x = round(random.randrange(Config["WallThickness"], Config["ScreenX"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
            y = round(random.randrange(Config["WallThickness"], Config["ScreenY"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
            if [x, y] not in Snake["Body"] and [x, y] not in Food:
                Food.append({"X": x, "Y": y, "Color": Colors["LightBlue"]})
                break

def RandomizeSpecialFoodLocation():
    SpecialFood.clear()
    for _ in range(int(Config["SpecialFoodCount"])):
        if random.random() < Config["SpecialFoodChance"]:
            while True:
                x = round(random.randrange(Config["WallThickness"], Config["ScreenX"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
                y = round(random.randrange(Config["WallThickness"], Config["ScreenY"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
                if [x, y] not in Snake["Body"] and [x, y] not in Food and [x, y] not in SpecialFood:
                    SpecialFood.append({"X": x, "Y": y, "Color": Colors["Yellow"]})
                    break

def RandomizePinkFoodLocation():
    PinkFood.clear()
    for _ in range(int(Config["PinkFoodCount"])):
        if random.random() < Config["PinkFoodChance"]:
            while True:
                x = round(random.randrange(Config["WallThickness"], Config["ScreenX"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
                y = round(random.randrange(Config["WallThickness"], Config["ScreenY"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
                if [x, y] not in Snake["Body"] and [x, y] not in Food and [x, y] not in SpecialFood and [x, y] not in PinkFood:
                    PinkFood.append({"X": x, "Y": y, "Color": Colors["Pink"]})
                    break

def DrawGame(screen, show_instructions):
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
            (head[0] + eye_offset, head[1] + eye_offset),
            (head[0] + eye_offset, head[1] + Config["BlockSize"] - eye_offset)
        ]
        tongue_position = (head[0] - Config["BlockSize"], head[1] + Config["BlockSize"] // 2)
    elif Snake["Direction"] == "right":
        eye_positions = [
            (head[0] + Config["BlockSize"] - eye_offset, head[1] + eye_offset),
            (head[0] + Config["BlockSize"] - eye_offset, head[1] + Config["BlockSize"] - eye_offset)
        ]
        tongue_position = (head[0] + Config["BlockSize"] * 2, head[1] + Config["BlockSize"] // 2)
    elif Snake["Direction"] == "up":
        eye_positions = [
            (head[0] + eye_offset, head[1] + eye_offset),
            (head[0] + Config["BlockSize"] - eye_offset, head[1] + eye_offset)
        ]
        tongue_position = (head[0] + Config["BlockSize"] // 2, head[1] - Config["BlockSize"])
    elif Snake["Direction"] == "down":
        eye_positions = [
            (head[0] + eye_offset, head[1] + Config["BlockSize"] - eye_offset),
            (head[0] + Config["BlockSize"] - eye_offset, head[1] + Config["BlockSize"] - eye_offset)
        ]
        tongue_position = (head[0] + Config["BlockSize"] // 2, head[1] + Config["BlockSize"] * 2)
    else:
        eye_positions = []
        tongue_position = None

    for pos in eye_positions:
        pygame.draw.circle(screen, Colors["White"], pos, eye_size)

    if tongue_position:
        pygame.draw.line(screen, Colors["Red"], (head[0] + Config["BlockSize"] // 2, head[1] + Config["BlockSize"] // 2), tongue_position, 2)

    for food in Food:
        pygame.draw.rect(screen, food["Color"], [food["X"], food["Y"], Config["BlockSize"], Config["BlockSize"]])
    for food in SpecialFood:
        pygame.draw.rect(screen, food["Color"], [food["X"], food["Y"], Config["BlockSize"], Config["BlockSize"]])
    for food in PinkFood:
        pygame.draw.rect(screen, food["Color"], [food["X"], food["Y"], Config["BlockSize"], Config["BlockSize"]])

    # Display the score
    font = pygame.font.SysFont(None, 35)
    score_text = font.render(f"Score: {Score}", True, Colors["Black"])
    screen.blit(score_text, [10, 10])

    # Display the instructions
    if show_instructions:
        instructions_font = pygame.font.SysFont(None, 50)
        instructions_text = instructions_font.render("To Start Move Around with WASD!", True, Colors["Black"])
        screen.blit(instructions_text, [Config["ScreenX"] // 2 - 300, 50])

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

def WinGame(screen):
    font = pygame.font.SysFont(None, 75)
    text = font.render("You Beat the Game!", True, Colors["Black"])
    screen.blit(text, [Config["ScreenX"] // 2 - 250, Config["ScreenY"] // 2 - 50])  # Adjusted x-coordinate to move text to the left
    pygame.display.update()

    fireworks = []
    for _ in range(10):  # Create 10 fireworks
        fireworks.append({
            "x": random.randint(100, Config["ScreenX"] - 100),
            "y": random.randint(50, Config["ScreenY"] // 2 - 100),
            "particles": [{"x": 0, "y": 0, "dx": random.uniform(-2, 2), "dy": random.uniform(-2, 2), "life": 80, "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))} for _ in range(100)]
        })

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
                RandomizeFoodLocation()
                RandomizeSpecialFoodLocation()
                RandomizePinkFoodLocation()
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

        DrawGame(screen, show_instructions)
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