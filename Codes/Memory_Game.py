###############################################
#                                             #
#try to reveal all the pairs of cards in      #
#  minumum number of turns...                 #
###############################################
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
turns=0


def new_game():
    global listOfCards,exposed,openedCard,clickCounter,turns
    listOfCards=[i for i in range(8)]+[i for i in range(8)]
    random.shuffle(listOfCards)
    exposed=[False for i in range(16)]
    openedCard=[]
    clickCounter=0
    turns=0
   

def mouseclick(pos):
    global clickCounter,turns
    if clickCounter==0:
        openedCard.append(pos[0]//50)
        exposed[pos[0]//50]=True
        clickCounter+=1
        turns=1
        
    elif clickCounter==1:
        if not (pos[0]//50 in openedCard):
            openedCard.append(pos[0]//50)
            clickCounter+=1
        exposed[pos[0]//50]=True
       
    else:
        if not (pos[0]//50 in openedCard):
            if listOfCards[openedCard[-1]]!=listOfCards[openedCard[-2]]:
                exposed[openedCard[-1]]=False
                exposed[openedCard[-2]]=False
                openedCard.pop()
                openedCard.pop()
            clickCounter=1
            turns+=1
            exposed[pos[0]//50]=True
            openedCard.append(pos[0]//50)
                        

def draw(canvas):
        label.set_text("Turns = "+str(turns))
        for i in range(16):
            canvas.draw_line([50*(i%15+1),0], [50*(i%15+1),100], 2, "Green")
            if exposed[i]:
                canvas.draw_text(str(listOfCards[i]), [15+50*i,70], 40, "White")

                
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game) 
label=frame.add_label("Turns = 0")


frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)


new_game()
frame.start()