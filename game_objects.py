import random
import pygame

# Define global variables
Snake = None
Food = None
SpecialFood = None
PinkFood = None
Score = None
FoodCollected = None

def reset_game(Config, Colors):
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
    RandomizeFoodLocation(Config, Colors)
    RandomizeSpecialFoodLocation(Config, Colors)
    RandomizePinkFoodLocation(Config, Colors)

def RandomizeFoodLocation(Config, Colors):
    global Food
    Food.clear()
    for _ in range(Config["FoodCount"]):
        while True:
            x = round(random.randrange(Config["WallThickness"], Config["ScreenX"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
            y = round(random.randrange(Config["WallThickness"], Config["ScreenY"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
            if [x, y] not in Snake["Body"] and [x, y] not in Food:
                Food.append({"X": x, "Y": y, "Color": Colors["LightBlue"]})
                break

def RandomizeSpecialFoodLocation(Config, Colors):
    global SpecialFood
    SpecialFood.clear()
    for _ in range(int(Config["SpecialFoodCount"])):
        if random.random() < Config["SpecialFoodChance"]:
            while True:
                x = round(random.randrange(Config["WallThickness"], Config["ScreenX"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
                y = round(random.randrange(Config["WallThickness"], Config["ScreenY"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
                if [x, y] not in Snake["Body"] and [x, y] not in Food and [x, y] not in SpecialFood:
                    SpecialFood.append({"X": x, "Y": y, "Color": Colors["Yellow"]})
                    break

def RandomizePinkFoodLocation(Config, Colors):
    global PinkFood
    PinkFood.clear()
    for _ in range(int(Config["PinkFoodCount"])):
        if random.random() < Config["PinkFoodChance"]:
            while True:
                x = round(random.randrange(Config["WallThickness"], Config["ScreenX"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
                y = round(random.randrange(Config["WallThickness"], Config["ScreenY"] - Config["WallThickness"] - Config["BlockSize"], Config["BlockSize"]))
                if [x, y] not in Snake["Body"] and [x, y] not in Food and [x, y] not in SpecialFood and [x, y] not in PinkFood:
                    PinkFood.append({"X": x, "Y": y, "Color": Colors["Pink"]})
                    break

def draw_walls(screen, Config, Colors):
    pygame.draw.rect(screen, Colors["Black"], [0, 0, Config["ScreenX"], Config["WallThickness"]])  # Top wall
    pygame.draw.rect(screen, Colors["Black"], [0, 0, Config["WallThickness"], Config["ScreenY"]])  # Left wall
    pygame.draw.rect(screen, Colors["Black"], [0, Config["ScreenY"] - Config["WallThickness"], Config["ScreenX"], Config["WallThickness"]])  # Bottom wall
    pygame.draw.rect(screen, Colors["Black"], [Config["ScreenX"] - Config["WallThickness"], 0, Config["WallThickness"], Config["ScreenY"]])  # Right wall

def DrawGame(screen, Config, Colors, show_instructions):
    global Snake, Food, SpecialFood, PinkFood, Score
    screen.fill(Config["background"])
    draw_walls(screen, Config, Colors)

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