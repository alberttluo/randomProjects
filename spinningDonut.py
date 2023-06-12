import pygame
import math

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
hue = 0

width = 1920
height = 1080

xstart, ystart = 0, 0

xsep = 10
ysep = 20

rows = height // ysep
cols = width // xsep
screen_size = rows*cols

x_offset = cols / 2
y_offset = rows / 2

A, B = 0, 0

theta_spacing = 10
phi_spacing = 5

chars = ".,-~:;=!*#$@"

screen = pygame.display.set_mode((width, height))

display_surface = pygame.display.set_mode((width, height))

pygame.display.set_caption('Spinning Donut')
font = pygame.font.SysFont('Arial', 18, bold=True)

def display(letter, xstart, ystart):
    text = font.render(str(letter), True, white)
    display_surface.blit(text, (xstart, ystart))



run = True
while run:

    screen.fill((black))

    z = [0] * screen_size
    b = [' '] * screen_size

    for j in range (0, 628, theta_spacing):
        for i in range(0, 628, phi_spacing):
            c = math.sin(i)
            d = math.cos(j)
            e = math.sin(A)
            f = math.sin(j)
            g = math.cos(A)
            h = d + 2
            D = 1 / (c * h * e + f * g + 5)
            l = math.cos(i)
            m = math.cos(B)
            n = math.sin(B)
            t = c * h * g - f * e
            x = int(x_offset + 40 * D * (l * h * m - t * n))  # 3D x coordinate after rotation
            y = int(y_offset + 20 * D * (l * h * n + t * m))  # 3D y coordinate after rotation
            o = int(x + cols * y)  
            N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))  # luminance index
            if rows > y and y > 0 and x > 0 and cols > x and D > z[o]:
                z[o] = D
                b[o] = chars[N if N > 0 else 0]

    if ystart == rows * ysep - ysep:
        ystart = 0

    for i in range(len(b)):
        A += 0.00004
        B += 0.00002
        if i == 0 or i % cols:
            display(b[i], xstart, ystart)
            xstart += xsep
        else:
            ystart += ysep
            xstart = 0
            display(b[i], xstart, ystart)
            xstart += xsep


    pygame.display.update()

    hue += 0.005

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
