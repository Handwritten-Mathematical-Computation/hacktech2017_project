import pygame
import re

def init():
    pygame.init()
    pygame.font.init()

class Display:
    def __init__(self, file_name, expression, answer):
        windowDisplay = pygame.display.set_mode((720,750)) #Image scaled x8 is (576, 368)
        pygame.display.set_caption("HackTech 2017")
        pygame.display.update() #Arguments are also valid
        #windowDisplay.fill((255,255,255))
        draw(windowDisplay)
        insertImage(windowDisplay,file_name)
        GoogleExpression(windowDisplay, expression)
        WolframAnswer(windowDisplay, answer)
        pygame.display.update()
        gameExit = False

        while not gameExit:
            for event in pygame.event.get():
#                print(event)
                if event.type == pygame.QUIT:
                    gameExit = True
                    quitDisplay()

def draw(windowDisplay):
    white = (255,255,255)
    pygame.draw.line(windowDisplay,white, (0, 460) , (720, 460) )
    pygame.draw.line(windowDisplay,white, (0, 610) , (720, 610) )
    pygame.display.update()

def insertImage(windowDisplay,file_name): #Should only be called once the image is ready
    receivedImage = pygame.image.load(file_name)
    # drawnImage.fill((255,255,255))
    windowDisplay.blit(receivedImage, (0,0))
    pygame.display.update()


def GoogleExpression(windowDisplay, expression):
    if not expression:
        expression = "None"
    expression = re.sub('[^0-9a-zA-Z+-=]+', '', expression)
    # print("myanswer:", expression)
    if not expression:
        expression = "--"
    result = pygame.font.SysFont(None, 50)
    output = result.render("Eq:   " + str(expression), True, (255,255,255))
    windowDisplay.blit(output , ((360 - (len(str(expression))*30/2)), 500 ))
    pygame.display.update()


def WolframAnswer(windowDisplay, answer):
    if not answer:
        answer = "None"
    answer = re.sub('[^0-9a-zA-Z+-=]+', '', answer)
    # print("myanswer:",answer)
    if not answer:
        answer = "No Answer"
    result = pygame.font.SysFont(None, 50)
    output = result.render("A:   " + str(answer), True, (255,255,255))
    windowDisplay.blit(output, ((360 - (len(str(answer))*30/2)), 650))
    pygame.display.update()


def quitDisplay ():
    pygame.display.quit()
    pygame.quit()
    # quit()

def main():
    newDisplay = Display()

if __name__ == "__main__":
    main()
