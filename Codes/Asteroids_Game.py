import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random
 

WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False
rock_group = set()
missile_group = set()
explosion_group = set()
rock_count = 0
 
 

 
def process_sprite_group(group,canvas):
    for s in list(group):
        s.draw(canvas)
        if s.update() == True:
            group.remove(s)
 
 
def group_collide(group,other_object):
    c_num = 0
    for s in list(group):
        if s.collide(other_object) == True:
            rock_avel = random.random() * .2 - .1
            explosion = Sprite(s.get_position(), [0,0], 0, rock_avel, explosion_image, explosion_info,explosion_sound) 
            explosion_group.add(explosion)
            group.remove(s)
            c_num += 1
    return c_num
 
def group_group_collide(group1,group2):
    c_num = 0
    for s in list(group2):
        g1_c = group_collide(group1,s)
        if g1_c > 0 :
            group2.remove(s)
            c_num += g1_c
    return c_num
 
 
 
 
 
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated
 
    def get_center(self):
        return self.center
 
    def get_size(self):
        return self.size
 
    def get_radius(self):
        return self.radius
 
    def get_lifespan(self):
        return self.lifespan
 
    def get_animated(self):
        return self.animated
 
 

 

debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")
 

nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")
 

splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
 

ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
 

missile_info = ImageInfo([5,5], [10, 10], 3, 70)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
 

asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
 

explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
 

soundtrack= simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
 

def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]
 
def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
 
 

class Ship:
 
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
 
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
 
 
    def update(self):
        
        self.angle += self.angle_vel
 
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
 
        
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
 
        self.vel[0] *= .99
        self.vel[1] *= .99
 
    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
 
    def increment_angle_vel(self):
        self.angle_vel += .05
 
    def decrement_angle_vel(self):
        self.angle_vel -= .05
 
    def shoot(self):
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        m = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(m)
 
    def get_radius(self): return self.radius
    def get_position(self): return self.pos
 
    def tooclose(self,other_object):
        other = other_object.get_position()
        dist2 = dist(self.pos,other)
        rad2 = self.radius + other_object.get_radius()
        if dist2 < rad2*1.5 :
            return True
        else:
            return False 
 
 
 

class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
 
    def draw(self, canvas):
 
        if self.animated == False:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
        elif self.animated == True:
             i = self.age
             center = [self.image_center[0]+i*self.image_size[0],self.image_center[1]]
             canvas.draw_image(self.image, center, self.image_size,
                       self.pos, self.image_size, self.angle)
 
 
    def update(self):
        
        self.angle += self.angle_vel
        self.age += 1
 
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
 
        if self.age < self.lifespan:
            return False
        else:
            return True
 
    def collide(self,other_object):
        other = other_object.get_position()
        dist2 = dist(self.pos,other)
        rad2 = self.radius + other_object.get_radius()
        if dist2 < rad2 :
            return True
        else:
            return False
 
 
 
    def get_radius(self): return self.radius
    def get_position(self): return self.pos
 
 

def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
 
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
 

def click(pos):
    global started,lives,score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.play()
 
def draw(canvas):
    global time, started, lives,score, rock_count
 
    
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])
 
    
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
 
    
    my_ship.draw(canvas)
 
        
    process_sprite_group(rock_group,canvas)
    process_sprite_group(missile_group,canvas)
    process_sprite_group(explosion_group,canvas)
 
    
    my_ship.update()
 
    for r in rock_group: r.update()
 
   
 
    g1 =group_collide(rock_group,my_ship)
    lives -= g1
    rock_count -= g1
 
    g1 = group_group_collide(rock_group,missile_group)
    score += g1
    rock_count -= g1
 
    
 
    if lives < 1:
        rock_count = 0
        for r in list(rock_group):
            rock_group.discard(r)   
        started = False
        soundtrack.pause()
 
  
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
 
    
def rock_spawner():
    global rock_group,rock_count
 
    if rock_count <= 12 and started == True:
 
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        rock_avel = random.random() * .2 - .1
 
        rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info) 
 
    
        if my_ship.tooclose(rock) == False:
            rock_group.add(rock)
            rock_count += 1
 
 

frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)


my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
 
 
 

a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
 
 
 

frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)
 
timer = simplegui.create_timer(2000.0, rock_spawner)
 

timer.start()
frame.start()


