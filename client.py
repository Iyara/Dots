#client.py
import pygame
from network import Network

pygame.font.init()


MENU_WIDTH = 640
MENU_HEIGHT = 480

W, H = 1600, 830

NAME_FONT = pygame.font.SysFont("comicsans", 20)
TIME_FONT = pygame.font.SysFont("comicsans", 30)
SCORE_FONT = pygame.font.SysFont("comicsans", 26)

COLORS = [(255,0,0), (255, 128, 0), (255,255,0), (128,255,0),(0,255,0),(0,255,128),(0,255,255),(0, 128, 255), (0,0,255), (0,0,255), (128,0,255),(255,0,255), (255,0,128),(128,128,128), (0,0,0)]


# Dynamic Variables
players = {}
balls = []


def start_menu():
    win = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))
    pygame.display.set_caption("Dots")
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    name = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(name)
                        done = True
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode

        win.fill((30, 30, 30))
        # Render the current text.
        draw_text_middle(win, 'Enter Player Name', 60, (255,255,255))
        txt_surface = font.render(name, True, color)
        # Blit the text.
        win.blit(txt_surface, (input_box.x+5, input_box.y+5))
        #win.blit(txt_surface, (MENU_WIDTH/2 - (label.get_width()/2), (MENU_HEIGHT/3) * 2 - (label.get_height()/2)))
        # Blit the input_box rect.
        pygame.draw.rect(win, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

    return name


def draw_text_middle(win, text, size, color):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    win.blit(label, (MENU_WIDTH/2 - (label.get_width()/2), MENU_HEIGHT/3 - (label.get_height()/2)))

def redraw_window(win):
	win.fill((255,255,255)) # fill screen white, to clear old frames
	
		# draw all the orbs/balls
	for ball in balls:
		pygame.draw.circle(WIN, ball[2], (ball[0], ball[1]), BALL_RADIUS)


def main(win, name):
	print("2name: ", name)
	#global players

	# start by connecting to the network
	server = Network()
	current_id = server.connect(name)
	balls, players, game_time = server.send("get")
	print("after get")

	# setup the clock
	clock = pygame.time.Clock()

	run = True
	while run:
		clock.tick(30) # 30 fps max




		# get key presses
		keys = pygame.key.get_pressed()		

		# movement based on key presses
		if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_KP4]:
			pass


		for event in pygame.event.get():
			# if user hits red x button close window
			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN:
				# if user hits a escape key close program
				if event.key == pygame.K_ESCAPE:
					run = False

		# redraw window then update the frame
		redraw_window()
		pygame.display.update()

	server.disconnect()
	pygame.quit()
	quit()


name = start_menu()
print("name: ", name)
pygame.display.set_caption("Dots")
win = pygame.display.set_mode((W, H))

main(win, name)
