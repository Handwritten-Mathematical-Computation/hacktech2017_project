import pygame
import re

def init(): #Initialization of the Display Window
    pygame.init()
    pygame.font.init()

class Display:
    def __init__(self, file_name, expression, answer):
        windowDisplay = pygame.display.set_mode((720,750)) #Display window is set to 720x750 resolution
        pygame.display.set_caption("HackTech 2017")
        pygame.display.update() #Repaints the display
        #windowDisplay.fill((255,255,255))
        draw(windowDisplay) #Function which partitions the display into the image, expression, and answer
        insertImage(windowDisplay,file_name)  #Function which displays the drawn image
        GoogleExpression(windowDisplay, expression)  #Function which displays the input read by the Google API
        WolframAnswer(windowDisplay, answer)    #Function which displays the Wolfram Answer to the expression
        pygame.display.update()     #Repaints the display
        gameExit = False

        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    quitDisplay()

def draw(windowDisplay):    #Produces the Display window
    white = (255,255,255)
    pygame.draw.line(windowDisplay,white, (0, 460) , (720, 460) )   #Partition
    pygame.draw.line(windowDisplay,white, (0, 610) , (720, 610) )   #Partition
    pygame.display.update() #Repaint Display window

def insertImage(windowDisplay,file_name):  #Passes the image and paints the Display window
    receivedImage = pygame.image.load(file_name)    #Specific file is loaded as an Image
    windowDisplay.blit(receivedImage, (0,0))    #Painted into display
    pygame.display.update() #Repaint Display window


def GoogleExpression(windowDisplay, expression):    #Outputs the Google API expression
    if not expression:
        expression = "None"
    expression = re.sub('[^0-9a-zA-Z+-=]+', '', expression) #Uses the re library to identify operands
    # print("myanswer:", expression)
    if not expression:  #If the output is not a legible expression
        expression = "--"
    result = pygame.font.SysFont(None, 50)   #Font is set to sie 50
    output = result.render("Eq:   " + str(expression), True, (255,255,255))     #Output
    windowDisplay.blit(output , ((360 - (len(str(expression))*30/2)), 500 ))    #Paints expression to display
    pygame.display.update() #Repaint Display window


def WolframAnswer(windowDisplay, answer):   #Outputs the Wolfram Alpha API expression
    if not answer:
        answer = "None"
    answer = re.sub('[^0-9a-zA-Z+-=]+', '', answer)
    # print("myanswer:",answer)
    if not answer:
        answer = "No Answer"
    result = pygame.font.SysFont(None, 50)  #Font is set to sie 50
    output = result.render("A:   " + str(answer), True, (255,255,255))  #Output
    windowDisplay.blit(output, ((360 - (len(str(answer))*30/2)), 650))  #Paints answer to display
    pygame.display.update() #Repaint Display window


def quitDisplay (): #Closes the Display window and stops operation
    pygame.display.quit()
    pygame.quit()
    # quit()

def main():
    newDisplay = Display()  #Creation of the Display Window

if __name__ == "__main__":
    main()
