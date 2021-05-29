import pygame

class Button():
    def __init__(self, color, center, font, text='', width=None):
        self.color = color
        self.font = font
        self.center = center
        self.text = self.font.render(text, True, (0,0,0))
        if width == None:
            self.width = self.text.get_width() * 1.2
        else:
            self.width = width
        self.height = self.text.get_height() * 1.1
        self.x = self.center[0] - (self.width/2)
        self.y = self.center[1] - (self.height/2)
        
        self.active = False

    def draw(self, screen, outline=None, outlineWidth=0):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x-outlineWidth,self.y-outlineWidth,self.width+(2*outlineWidth),self.height+(2*outlineWidth)),0)
            
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height), 0)
        
        if self.text != '':
            screen.blit(self.text, (self.x + (self.width/2 - self.text.get_width()/2), self.y + (self.height/2 - self.text.get_height()/2)))

    def hover(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
