from OpenGL.GL import *
from OpenGL.GLUT import *
import math

w_width = 600
w_height = 600
bubble_radius = 15
football_radius = 30
circle_speed = 0.3


goalpost_width = w_width * 0.3
score=0

circles = []
football_pos = {"x": w_width / 2, "y": football_radius, "rad": football_radius, "color": (1.0, 1.0, 1.0)}


def draw_circle(cen_x, cen_y, rad, color):
    glBegin(GL_POINTS)
    glColor3f(*color)
    d = 1 - rad
    x = 0
    y = rad
    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        glVertex2f(x + cen_x, y + cen_y)
        glVertex2f(y + cen_x, x + cen_y)
        glVertex2f(-x + cen_x, y + cen_y)
        glVertex2f(-y + cen_x, x + cen_y)
        glVertex2f(-x + cen_x, -y + cen_y)
        glVertex2f(-y + cen_x, -x + cen_y)
        glVertex2f(x + cen_x, -y + cen_y)
        glVertex2f(y + cen_x, -x + cen_y)
    glEnd()

def draw_goalpost():
    goalpost_width = w_width * 0.3  
    goalpost_height = w_height * 0.6  

    glColor3f(1.0, 1.0, 1.0)  
    glBegin(GL_QUADS)
    glVertex2f(w_width / 2 - goalpost_width / 2, w_height - bubble_radius * 2)
    glVertex2f(w_width / 2 - goalpost_width / 2, w_height + goalpost_height)
    glVertex2f(w_width / 2 + goalpost_width / 2, w_height + goalpost_height)
    glVertex2f(w_width / 2 + goalpost_width / 2, w_height - bubble_radius * 2)
    glEnd()



football_pos = [w_width / 2, football_radius]

def draw_football():
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 1.0, 1.0) 
    glVertex2f(football_pos[0], football_pos[1])

    num_segments = 100
    for i in range(num_segments + 1):
        angle = math.pi * 2.0 * i / num_segments
        x = football_pos[0] + football_pos[2] * math.cos(angle)
        y = football_pos[1] + football_pos[2] * math.sin(angle)
        glVertex2f(x, y)
    glEnd()

def draw_objects():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    for circle in circles:
        draw_circle(circle['x'], circle['y'], circle['rad'], circle['color'])
    draw_goalpost()
    draw_football()

def move_bubbles():
    for circle in circles:
        circle['x'] += circle['speed_x']
        circle['y'] += circle['speed_y']

        if circle['x'] + circle['rad'] > w_width or circle['x'] - circle['rad'] < 0:
            circle['speed_x'] *= -1
        if circle['y'] + circle['rad'] > w_height or circle['y'] - circle['rad'] < 0:
            circle['speed_y'] *= -1

keys = {'w': False, 's': False, 'a': False, 'd': False}

football_velocity = [0, 0]

football_pos = [w_width / 2, football_radius, football_radius]

def move_football():
    global football_velocity

    speed = 2 
    diagonal_speed = speed * math.cos(math.radians(45))  
    if keys['w']:
        football_velocity = [0, speed]
    elif keys['s']:
        football_velocity[1] = -speed
    if keys['a']:
        football_velocity[0] = -diagonal_speed
        football_velocity[1] = diagonal_speed
    elif keys['d']:
        football_velocity[0] = diagonal_speed
        football_velocity[1] = diagonal_speed
    
    football_pos[0] += football_velocity[0]
    football_pos[1] += football_velocity[1]

    # Boundary checks and bouncing
    if football_pos[0] + football_pos[2] > w_width:
        football_velocity[0] *= -1
        football_pos[0] = w_width - football_pos[2]
    elif football_pos[0] - football_pos[2] < 0:
        football_velocity[0] *= -1
        football_pos[0] = football_pos[2]

    if football_pos[1] + football_pos[2] > w_height:
        football_velocity[1] *= -1
        football_pos[1] = w_height - football_pos[2]
    elif football_pos[1] - football_pos[2] < 0:
        football_velocity[1] *= -1
        football_pos[1] = football_pos[2]

    check_collision()

# Update the check_collision() function
def check_collision():
    global football_velocity

    # Check collision with circles
    for circle in circles:
        distance = math.sqrt((football_pos[0] - circle['x'])**2 + (football_pos[1] - circle['y'])**2)
        if distance < football_pos[2] + circle['rad']:
            # Collision detected with bubble
            dx = football_pos[0] - circle['x']
            dy = football_pos[1] - circle['y']
            angle = math.atan2(dy, dx)
            football_velocity = [math.cos(angle), math.sin(angle)]
            


def keyboard_press(key, x, y):
    global score
    key = key.decode('utf-8').lower()
    if key in keys:
        keys[key] = True
    elif key == 'r':
        score = 0  # Reset the score to 0
        reset_position()  # Reset the football's position

def keyboard_release(key, x, y):
    key = key.decode('utf-8').lower()
    if key in keys:
        keys[key] = False
        
        
def check_goal():
        global score
        goalpost_top = w_height + bubble_radius
        goalpost_bottom = w_height - bubble_radius * 2

        if goalpost_bottom <= football_pos[1] + football_pos[2] <= goalpost_top:
            if w_width / 2 - goalpost_width / 2 <= football_pos[0] <= w_width / 2 + goalpost_width / 2:
                # Football is in the goal box
                score += 1
                print(f"Goal! Score: {score}")
                reset_position()
                
def reset_position():
    global football_pos, score, football_radius

    # Set football position to the starting position
    football_pos[0] = 600/ 2
    football_pos[1] = football_radius
               

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPointSize(2)

    move_bubbles()
    draw_objects()

    # Display the score
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, w_width, 0, w_height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(1.0, 1.0, 1.0)  # White color for text

    # Display score at top-left corner
    
    if 0 <= score < 10:
        glRasterPos2f(20, w_height - 20)
        score_text = f"Score: {score}"
    else:
        glRasterPos2f(300, w_height - 300)
        score_text = "You win the game"

        
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

    glutSwapBuffers()

    # Display game status messages
    check_goal()
    if score <= -10:
        print("Game Over! You reached a score of -10 or higher.")
    elif score >= 10:      
        print("You win the game")

    move_football()
    glutPostRedisplay()    


def main():
    for i in range(13):
        circles.append({"x": w_width / 2, "y": w_height / 2, "rad": bubble_radius, "color": (0.447, 1.0, 0.973),
                        "speed_x": circle_speed * math.cos(math.radians(i * 27.6923)),
                        "speed_y": circle_speed * math.sin(math.radians(i * 27.6923))})
    
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(w_width, w_height)
    glutCreateWindow(b"Football Game")
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, w_width, 0, w_height, -1, 1)
    
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard_press)
    glutKeyboardUpFunc(keyboard_release)    
    glutMainLoop()

if __name__ == "__main__":
    main()