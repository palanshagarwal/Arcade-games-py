import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
millis=0;
wins=0;
attempts=0;
boolean=False;
check=True;
def format_time(t):
    mil=t%10;
    temp=int(t/10);
    sec=temp%60;
    mnt=int(temp/60);
    if(sec<10):
        sec_string="0"+str(sec);
    else:
        sec_string=str(sec);
    return str(mnt)+":"+sec_string+"."+str(mil);    


def start_timer():
    global boolean,check;
    global wins,attempts,boolean;
    if check:
        timer.start();
        boolean=True;
        check=False;
    else :
        timer.stop();
        if boolean:
            if(millis%10==0):
                wins=wins+1;
            attempts=attempts+1;  
        boolean=False;
        check=True;
    

  

def reset_timer():
    global millis,wins,attempts
    timer.stop();
    millis=0;
    wins=0;
    attempts=0;

def timer_handler():
    global millis;
    millis +=1;
    
    
def draw_handler(canvas):
    canvas.draw_text(format_time(millis), (300,265), 150, "White");
    canvas.draw_text("W/A", (770,100), 50, "Red");
    canvas.draw_text("Score: "+str(wins)+"/"+str(attempts),(650,50),50,"Red");
    canvas.draw_text("Stopwatch Game", (10,40), 50, "Blue");
    canvas.draw_text("W--> No. of Wins", (10,360), 30, "Red");
    canvas.draw_text("A--> No. of Attempts", (10,390), 30, "Red");
    canvas.draw_text("m m    s    s       ms", (300,115), 50, "Red");
    canvas.draw_text("____   ____      ___", (300,115), 50, "Red");
    canvas.draw_line([300, 280], [680, 280], 5, 'Green');
    canvas.draw_line([300, 280], [300, 150], 5, 'Green');
    canvas.draw_line([300, 150], [680, 150], 5, 'Green');
    canvas.draw_line([680, 150], [680, 280], 5, 'Green');
    canvas.draw_text("A--> No. of Attempts", (10,390), 30, "Red");
    canvas.draw_text("*Try to stop it at 0 ms", (610,390), 30, "Pink");
frame=simplegui.create_frame("stopwatch",900,400);


frame.add_button("Start / Stop",start_timer,150);
frame.add_button("  Reset  ",reset_timer,150);
timer = simplegui.create_timer(100, timer_handler);
frame.set_draw_handler(draw_handler);


frame.start();

