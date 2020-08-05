import pygame
import os
import time
import linecache
import random
pygame.init()

'''
How the game works:
A series of questions will be asked to the user through the use of pygame fonts
The answers to the questions will be on one of 2-4 buttons
If the right answer is chosen then one of 2 attack animations will play
If the right answer is not chosen then the enemy's attack animation will play
If the user gets enough questions right, then a winning animation plays
Else a losing animation plays

Questions will be loaded in from a text file
buttons will be rectangles drawn on screen
'''

class Spritesheet:
    # This class loads spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(os.path.join(os.path.dirname(__file__), filename))
    
    def getImage(self, x, y, w, h):
        # grabs an image from a larger spritesheet
        image = pygame.Surface((w,h),pygame.SRCALPHA)
        image.blit(self.spritesheet, (0,0), (x, y, w, h))
        return image

def grabLine(line):
    # This will get the Questions and answers for the game
    return linecache.getline('Game Questions.txt', line)


class button():
    def __init__(self, color, x, y, w, h, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
    
    def draw(self, window, outline=None):
        # this method will draw the button
        if outline:
            pygame.draw.rect(window, outline, (self.x-2, self.y-2, self.w+4, self.h+4), 0)
        
        pygame.draw.rect(window, self.color, (self.x, self.y, self.w, self.h), 0)

        if self.text != '':
            font = pygame.font.SysFont('calibri bold', 30)
            text = font.render(self.text, 1, (255,255,255))
            window.blit(text, (self.x + (self.w/2 - text.get_width()/2), self.y + (self.h/2 - text.get_height()/2)))

    def overwriteText(self, text):
        self.text = text

    def resize(self, w, h):
        self.w = w
        self.h = h
    
    def isOver(self, pos):
        #if the mouse position is over the button
        if pos[0] > self.x and pos[0] < self.x + self.w:
            if pos[1] > self.y and pos[1] < self.y + self.h:
                return True
        
        return False

def playAnimation(num):
    animCnt = 0
    # Play Animations
    # Opening Animation
    if num == 1:
        for i in range(4):
            WIN.blit(pygame.transform.scale(openingAnim[i],(663,360)),(0,0))
            clock.tick(8)
            pygame.display.update()
    elif num == 2: # Cloud Attack 2 Animation
        for i in range(7):
            WIN.blit(pygame.transform.scale(cloudAttack_2[i],(663,360)),(0,0))
            clock.tick(8)
            pygame.display.update()
    elif num == 3: # Cloud Attack 1 Animation
        for i in range(10):
            WIN.blit(pygame.transform.scale(cloudAttack_1[i],(663,360)),(0,0))
            clock.tick(8)
            pygame.display.update()
    elif num == 4: # Charizard Attack
        for i in range(17):
            WIN.blit(pygame.transform.scale(charizardAttack[i],(663,360)),(0,0))
            clock.tick(8)
            pygame.display.update()
    elif num == 5: # Winning Animation
        for i in range(7):
            WIN.blit(pygame.transform.scale(winAnim[i],(663,360)),(0,0))
            clock.tick(8)
            pygame.display.update()

    elif num == 6: # Losing Animation
        for i in range(7):
            WIN.blit(pygame.transform.scale(loseAnim[i],(663,360)),(0,0))
            clock.tick(8)
            pygame.display.update()

   

def redraw():
    # Draw the background 
    WIN.blit(BG, (0,0))
    WIN.blit(SB, (0,360))

    # Draw Questions
    #question = getQuestion()
    question = grabLine(questions[questionIndex])
    questionLabel = questionFont.render(question[:-1],1,(255,255,255))
    WIN.blit(questionLabel, ((WIDTH/2 - questionLabel.get_width()/2, 400)))

    # Draw answers
    if questions[questionIndex] >= 39:
        # Resize and remove buttons
        redButton.resize(328,242)
        greenButton.resize(328,242)
        # Overwrite red and green button text
        redAnswer = grabLine(questions[questionIndex]+1)
        greenAnswer = grabLine(questions[questionIndex]+2)
        redButton.overwriteText(redAnswer[:-1])
        greenButton.overwriteText(greenAnswer[:-1])
    else:
        # Overwrite the button text
        # Fix button size
        redButton.resize(328,120)
        greenButton.resize(328,120)
        # Grab answer text
        redAnswer = grabLine(questions[questionIndex]+1)
        greenAnswer = grabLine(questions[questionIndex]+2)
        blueAnswer = grabLine(questions[questionIndex]+3)
        orangeAnswer = grabLine(questions[questionIndex]+4)
        # Add text to buttons
        redButton.overwriteText(redAnswer[:-1])
        greenButton.overwriteText(greenAnswer[:-1])
        blueButton.overwriteText(blueAnswer[:-1])
        orangeButton.overwriteText(orangeAnswer[:-1])

    # Draw buttons
    blueButton.draw(WIN,(255,255,255))
    orangeButton.draw(WIN,(255,255,255))
    redButton.draw(WIN,(255,255,255))
    greenButton.draw(WIN,(255,255,255))

    # Draw hearts for both characters
    # Cloud's hearts
    cloudX = 0
    for i in range(wrongCounter):
        WIN.blit(heart, (cloudX,0))
        cloudX += 64

    charizardX = 599
    for i in range(correctCounter):
        WIN.blit(heart, (charizardX,0))
        charizardX -= 64


    # Update display
    pygame.display.update()

def isRightAnswer():
    # Returns whether the answer chosen was correct
    pos = pygame.mouse.get_pos()
    # If the button that corresponds to the right answer is clicked, return true
    if questions[questionIndex] == 4:
        if greenButton.isOver(pos):
            return True
    elif questions[questionIndex] == 11:
        if blueButton.isOver(pos):
            return True
    elif questions[questionIndex] == 18:
        if orangeButton.isOver(pos):
            return True
    elif questions[questionIndex] == 25:
        if redButton.isOver(pos):
            return True
    elif questions[questionIndex] == 32:
        if redButton.isOver(pos):
            return True
    elif questions[questionIndex] == 39:
        if redButton.isOver(pos):
            return True
    elif questions[questionIndex] == 44:
        if greenButton.isOver(pos):
            return True
    elif questions[questionIndex] == 49:
        if greenButton.isOver(pos):
            return True
    else:
        return False

def mainMenu():
    global gameRound
    global correctCounter
    global wrongCounter 
    titleFont = pygame.font.SysFont("calibri bold", 65)
    instructionFont = pygame.font.SysFont("calibri bold", 40)
    titleLabel = titleFont.render("Press Enter To Start!", 1, (255,255,255))
    instrucions = ["This is a Simple Game!", "All you need to do is answer questions", "Answer 4 questions correctly and you win!", "However, get 4 wrong and you lose!", "Press Enter when you are ready to start"]

    yCoord = 500
    run = True
    
    for i in range(5):
            instructionLabel = instructionFont.render(instrucions[i], 1, (255,255,255))
            WIN.blit(instructionLabel, (10, yCoord))
            yCoord += 35
    while run:
        WIN.blit(BG, (0,0))
        WIN.blit(SB, (0,360))
        WIN.blit(titleLabel, (WIDTH/2 - titleLabel.get_width()/2, 400))    

        pygame.display.update()
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
                gameRound = 0
                correctCounter = 4
                wrongCounter = 4
                main() 
    pygame.quit()

def endScreen(win):
    titleFont = pygame.font.SysFont("calibri bold", 45)
    endFont = pygame.font.SysFont("calibri bold", 65)
    titleLabel = titleFont.render("Press Enter To Continue To Main Menu!", 1, (255,255,255))
    winLabel = endFont.render("You Win!", 1, (255,255,255))
    loseLabel = endFont.render("You Lost!", 1, (255,255,255))
    run = True
    while run:
        if win:
            WIN.fill((0,0,0))
            WIN.blit(winScreen,(0,0))
            WIN.blit(winLabel, (WIDTH/2 - winLabel.get_width()/2, 600))   
            WIN.blit(SB, (0,360))    
        else:
            WIN.fill((0,0,0))
            WIN.blit(loseScreen,(0,0))
            WIN.blit(loseLabel, (WIDTH/2 - loseLabel.get_width()/2, 600))   
            WIN.blit(SB, (0,360))
            
        
        WIN.blit(titleLabel, (WIDTH/2 - titleLabel.get_width()/2, 400))    

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
                run = False
                WIN.fill((0,0,0))
                mainMenu()

        pygame.display.update()

# Main Function
def main():
    global questionIndex
    global gameRound
    global correctCounter
    global wrongCounter 

    questionIndex = 0
    run = True
    while run:

        redraw()
        if gameRound == 0:
            playAnimation(1)  
            gameRound+=1

        # When the x button is clicked
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
    
            # When the buttons are clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if redButton.isOver(pos): # Answer 1
                    if isRightAnswer():
                        print("Correct!")
                        playAnimation(2)
                        questionIndex += 1
                        correctCounter -= 1
                    else:
                        print("Wrong!")
                        playAnimation(4)
                        questionIndex += 1
                        wrongCounter -= 1
                elif greenButton.isOver(pos):# Answer 2
                    if isRightAnswer():
                        playAnimation(3)
                        print("Correct!")
                        questionIndex += 1
                        correctCounter -= 1
                    else:
                        print("Wrong!")
                        playAnimation(4)
                        questionIndex += 1
                        wrongCounter -= 1
                elif blueButton.isOver(pos): # Answer 3
                    if isRightAnswer():
                        playAnimation(3)
                        print("Correct!")
                        questionIndex += 1
                        correctCounter -= 1
                    else:
                        print("Wrong!")
                        playAnimation(4)
                        questionIndex += 1
                        wrongCounter -= 1
                elif orangeButton.isOver(pos): # Answer 4
                    if isRightAnswer():
                        print("Correct!")
                        playAnimation(2)
                        questionIndex += 1
                        correctCounter -= 1
                    else:
                        print("Wrong!")
                        playAnimation(4)
                        questionIndex += 1
                        wrongCounter -= 1
            
        if correctCounter <= 0:
            print ("You Win!")
            playAnimation(5)
            endScreen(True)
            run = False
        elif wrongCounter <= 0:
            print ("You Lose!")
            playAnimation(6)
            endScreen(False)
            run = False

# Setup Window
(WIDTH, HEIGHT) = (663,726)
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Basic Types Game")

# Load animation sprite sheet
spritesheet = Spritesheet('Master Sheet.png')

# Load background image
gameFolder = os.path.dirname(__file__)
BG = pygame.transform.scale(pygame.image.load(os.path.join(gameFolder, 'Neutral Stage.png')),(663,360))
# Speech Box
SB = pygame.transform.scale(pygame.image.load(os.path.join(gameFolder, 'Speech Box.png')),(663,120))
# Hearts
heart = pygame.transform.scale(pygame.image.load(os.path.join(gameFolder, 'heart.png')),(64,64))
# Win screen
winScreen = pygame.transform.scale(spritesheet.getImage(1,489,221,120),(663,360))
# Lose screen
loseScreen = pygame.transform.scale(spritesheet.getImage(224,977,221,120),(663,360))

# Setup clock
clock = pygame.time.Clock()

# Place sprites into lists
            # Neutral -> Opening 1 -> Opening 2 -> Neutral 2
openingAnim = [spritesheet.getImage(447,977,221,120),spritesheet.getImage(893,977,221,120),spritesheet.getImage(1116,1,221,120),spritesheet.getImage(670,977,221,120)]
            # Startup -> startup 2 -> Attack 1...
cloudAttack_1 = [spritesheet.getImage(893,733,221,120),spritesheet.getImage(1,855,221,120),spritesheet.getImage(224,489,221,120),spritesheet.getImage(447,489,221,120),
spritesheet.getImage(670,489,221,120),spritesheet.getImage(893,489,221,120),spritesheet.getImage(1,611,221,120),spritesheet.getImage(224,611,221,120),
spritesheet.getImage(447,611,221,120),spritesheet.getImage(670,733,221,120)]
            # startup -> attack 2-1
cloudAttack_2 = [spritesheet.getImage(893,733,221,120),spritesheet.getImage(670,611,221,120),spritesheet.getImage(893,611,221,120),spritesheet.getImage(1,733,221,120),
spritesheet.getImage(224,733,221,120),spritesheet.getImage(447,733,221,120),spritesheet.getImage(670,733,221,120)]

charizardAttack = [spritesheet.getImage(447,977,221,120),spritesheet.getImage(1,1,221,120),spritesheet.getImage(670,1,221,120),spritesheet.getImage(893,1,221,120),
spritesheet.getImage(1,123,221,120),spritesheet.getImage(224,123,221,120),spritesheet.getImage(447,123,221,120),spritesheet.getImage(670,123,221,120),
spritesheet.getImage(893,123,221,120),spritesheet.getImage(1,245,221,120),spritesheet.getImage(224,1,221,120),spritesheet.getImage(447,1,221,120),
spritesheet.getImage(224,245,221,120),spritesheet.getImage(447,245,221,120),spritesheet.getImage(670,245,221,120),spritesheet.getImage(893,245,221,120),spritesheet.getImage(447,977,221,120)]

winAnim = [spritesheet.getImage(447,977,221,120),spritesheet.getImage(1,367,221,120),spritesheet.getImage(224,367,221,120),spritesheet.getImage(447,367,221,120),
spritesheet.getImage(670,367,221,120),spritesheet.getImage(893,367,221,120),spritesheet.getImage(1,489,221,120)]

loseAnim = [spritesheet.getImage(447,977,221,120),spritesheet.getImage(224,855,221,120),spritesheet.getImage(447,855,221,120),spritesheet.getImage(670,855,221,120),
spritesheet.getImage(893,855,221,120),spritesheet.getImage(1,977,221,120),spritesheet.getImage(224,977,221,120)]

# Load Fonts
questionFont = pygame.font.SysFont('calibri bold', 50)

# Player Stats
#questionIndex = 0

# Randomize the question order
questions = [4,11,18,25,32,39,44,49]
random.shuffle(questions)

# Make buttons
redButton = button((255,0,0), 2, 482, 328, 120)
greenButton = button((0,255,0), 333, 482, 328, 120)
blueButton = button((0,0,255), 2, 604, 328, 120)
orangeButton = button((255,128,0), 333, 604, 328, 120)

# Run the program           
mainMenu()

