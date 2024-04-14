import pygame
import sys
import matplotlib.pyplot as plt

pygame.init()

screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Raketa")
FPS = 15
font = pygame.font.Font(None, 60)
font3 = pygame.font.Font(None, 30)
font2 = pygame.font.Font(None, 80)

class Button: #klasa za gumb bez slike
    def __init__(self, text_input, text_size, text_color, rectangle_width_and_height, rectangle_color, rectangle_hovering_color, position):
        self.text_input = text_input
        #rectangle ispod teksta
        self.rectangle = pygame.Rect((position[0]-(rectangle_width_and_height[0]/2), position[1]-(rectangle_width_and_height[1]/2)), rectangle_width_and_height)
        self.rectangle_color, self.rectangle_hovering_color = rectangle_color, rectangle_hovering_color
        #tekst u gumbu
        self.font = pygame.font.Font(None, text_size)
        self.text_surface = self.font.render(text_input, False, text_color)
        self.text_rectangle = self.text_surface.get_rect(center = self.rectangle.center)
    def update(self, screen):
        pygame.draw.rect(screen, self.rectangle_color, self.rectangle)
        screen.blit(self.text_surface, self.text_rectangle)
    def checkForCollision(self, mouse_position):
        if mouse_position[0] in range(self.rectangle.left, self.rectangle.right) and mouse_position[1] in range(self.rectangle.top, self.rectangle.bottom):
            return True
        return False
    def changeButtonColor(self):
        self.rectangle_color = self.rectangle_hovering_color
    def changeTextInput(self, new_text):
        self.text_input = new_text
        self.text_surface = self.font.render(self.text_input, False, (255, 255, 255))
        self.text_rectangle = self.text_surface.get_rect(center=self.rectangle.center)

class Button_Slika(): #klasa za gumb sa slikom
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		surface.blit(self.image, (self.rect.x, self.rect.y))
		return action

def draw_text(text,font,text_col,x,y): #za ispis teksta
        img = font.render(text,True,text_col)
        screen.blit(img,(x,y))
        
def main_menu():
    global screen, font, postotak_goriva, font2,font3
    #slike
    bg = pygame.transform.scale(pygame.image.load("mainmenu.jpg"), (1280,720))
    arrow = pygame.transform.rotate(pygame.image.load("arrow.png"),90)
    strijelica1 = Button_Slika(screen.get_width()*0.5, screen.get_height()*0.68,arrow, 0.1)
    strijelica2 = Button_Slika(screen.get_width()*0.7, screen.get_height()*0.68,pygame.transform.flip(arrow, True, False), 0.1)
    postotak_goriva = 100
    run = True
    while run:
        screen.blit(bg, (0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MAIN_GUMB = Button("Započni", 70, "white",(screen.get_width()*0.17, screen.get_height()*0.128), "red", "tomato", (screen.get_width()*0.618, screen.get_height()*0.87))
        for gumb in [MAIN_GUMB]:
            if gumb.checkForCollision(MENU_MOUSE_POS):
                gumb.changeButtonColor()
            gumb.update(screen)
        
        #mijenjanje varijable za količinu goriva
        draw_text(f"{postotak_goriva}%", font2, "white", 723, 490)
        draw_text(f"tip: koristi scroll wheel ;)", font3, "white", 670, 555)
        if strijelica1.draw(screen):
            if postotak_goriva > 0:
                postotak_goriva -=1
        if strijelica2.draw(screen):
            if postotak_goriva < 100:
                postotak_goriva +=1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MAIN_GUMB.checkForCollision(MENU_MOUSE_POS):
                    run = False
                    igra()
                if event.button == 5:
                    if postotak_goriva > 0:
                        postotak_goriva -= 1
                if event.button == 4:
                    if postotak_goriva < 100:
                        postotak_goriva += 1

        pygame.display.update()

def podatci(): #zapisani svi podatci i slike ovdje radi jednostavnosti
    global h,v,F, T, H, gorivo, v_, F_, t,bg1,bg2,bg3,sb,raketa,n, masa_goriva_prvi,masa_goriva_drugi,a,Ro,Fo,G,M,R,S,Cx,masa_prvi_raketa,masa_drugi_raketa,trošnja_goriva_prvi,trošnja_goriva_drugi,sila_uzgona_drugi,sila_uzgona_prvi
    #slike
    bg1 = pygame.transform.scale(pygame.image.load("world1_bg.jpg"), (1280,720))
    bg2 = pygame.transform.scale(pygame.image.load("world2_bg.jpg"), (1280,720))
    bg3 = pygame.transform.scale(pygame.image.load("world3_bg.jpg"), (1280,720))
    sb = pygame.transform.scale(pygame.image.load("stats.png"), (1280,720))
    raketa = pygame.transform.scale(pygame.image.load("raketa.png"), (1280,720))

    t = 0
    h = 0
    a = 0
    v = 0
    F = 0
    Ro = 1.225
    Fo = 0
    G = 6.67428 * (10**(-11))
    M = 5.97219 * (10**24)
    R = 6378.1 * 1000
    S = (3.6**2)*3.1419
    Cx = 0.75 #vrijedi za rakete

    #podaci su uzeti za raketu Falcon 9 iz ovog dokumenta: #https://www.researchgate.net/publication/363319640_AAS_22-821_AMBIGUITY_REMEDIATION_IN_SPACE_LAUNCH_VEHICLES_WITH_PARAMETER_UNCERTAINTIES_A_COMPARISON_BETWEEN_SPECIAL_EUCLIDEAN_GROUP_AND_DUAL_QUATERNIONS/download?_tp=eyJjb250ZXh0Ijp7ImZpcnN0UGFnZSI6Il9kaXJlY3QiLCJwYWdlIjoiX2RpcmVjdCJ9fQ
    #mase rakete za prvu i drugu fazu leta
    masa_prvi_raketa = 165700 #kg; masa same rakete bez goriva u prvoj fazi
    masa_drugi_raketa = 15419 #kg; masa same rakete bez goriva u drugoj fazi
    masa_goriva_prvi = 367900 #kg; gorivo koje se potroši u prvoj fazi
    masa_goriva_drugi = 103438 #kg; gorivo koje se potroši u drugoj fazi
    trošnja_goriva_prvi = 2536.420 #kg/s
    trošnja_goriva_drugi = 270.781 #kg/s
    sila_uzgona_prvi = 8227000 #N
    sila_uzgona_drugi = 981000 #N;

    n = 0 #za prikaz neprestanog micanje rakete u svemiru

    masa_goriva_prvi = masa_goriva_prvi*postotak_goriva/100
    masa_goriva_drugi = masa_goriva_drugi*postotak_goriva/100

    #za grafove
    H = []
    F_ = []
    v_ = []
    T = []
    gorivo = []

def prikaz_rakete():
    global n
    #micanje y komponente rakete u prikazu      
    if h < 10000: #do visine 10km smo u troposferi što označava 1. slika
        screen.blit(bg1, (0,0))
        y = -h/13.88888889
    elif h >= 10000 and h < 50000: #do visine 50km smo u statosferi što označava 2. slika
        screen.blit(bg2, (0,0))
        y = (10000-h)/55.555555555555556
        if y < -720:
            y = 0
    else: #iznad visine 50km smo u svemiru (otprilike) što označava 3. slika
        screen.blit(bg3,(0,0))
        y = (50000+100000*n-h)/138.888888888888888889
        if y < -720:
            y = 0
            n +=1
    screen.blit(raketa, (0,y))

def prikaz_podataka(): #prikaz podataka sa strane
    global omjer_goriva
    omjer_goriva = (masa_goriva_prvi+masa_goriva_drugi)/(367900+103438)
    screen.blit(sb, (0,0))
    draw_text(f'{int(t)}',font,"black",screen.get_width()*0.82,screen.get_height()*0.14)
    draw_text(f'{round(h/1000,2)}',font,"black",screen.get_width()*0.82,screen.get_height()*0.34)
    draw_text(f'{round(v/1000,2)}',font,"black",screen.get_width()*0.82,screen.get_height()*0.54)
    draw_text(f'{round(F/1000,2)}',font,"black",screen.get_width()*0.8,screen.get_height()*0.71)
    pygame.draw.rect(screen,"sienna",(screen.get_width()*0.77,screen.get_height()*0.865,screen.get_width()*0.214*omjer_goriva,screen.get_height()*0.095))

def faze_rakete(): #određivanje svake faze rakete i mijenjanje podataka po fazi
    global stanje,Fu,m,run,masa_goriva_prvi,masa_goriva_drugi
    #odabir faze u letu
    if masa_goriva_prvi > 0:
        stanje = 1
    elif masa_goriva_prvi <= 0 and masa_goriva_drugi > 0:
        stanje = 2
    else: 
        stanje = 3
    
    #odabir mase, trošnje goriva, sile uzgona po fazi
    if stanje == 1:
        masa_goriva_prvi -= trošnja_goriva_prvi
        m = masa_prvi_raketa + masa_goriva_prvi - trošnja_goriva_prvi
        Fu = sila_uzgona_prvi
    elif stanje == 2:
        masa_goriva_prvi = 0
        masa_goriva_drugi -= trošnja_goriva_drugi
        m = m = masa_drugi_raketa + masa_goriva_drugi - trošnja_goriva_drugi
        Fu = sila_uzgona_drugi
    elif stanje == 3: #prestaje simulacija kada raketa ostane bez goriva
        masa_goriva_drugi = 0
        masa_goriva_prvi = 0
        m = masa_drugi_raketa
        Fu = 0
        run = False
        game_over()

def sila_teža(): #izračun sile teže
    global h,Fg
    g = G * M/((R+h)**2)
    Fg = m*g

def otpor_zraka(): #izračun sile otpora zraka
    global Fo,Ro
    Ro1 = Ro #za sljedeću formulu gustoće zraka
    Ro = Ro1 * 2.71828**(-h/80000) #formula za gustoću zraka, nije savršena, ali je približno točna
    Fo = Cx * S * Ro * (v**2) / 2 

def izračun_sile(): #ukupna sile i akceleracija
    global a, F
    F = Fu - Fg - Fo
    a = F/m

def izračun_veličina():
    global v,h,t
    #budući da se svaka iteracija gleda kao 1 sekunda više, brzina se može izračunati preko akceleracije, a visina preko brzine.
    v += a
    h += v
    t += 1

def info_graf(): #liste potrebne za grafove
    global T,v_,H,F_,gorivo
    T.append(t)
    v_.append(v)
    H.append(h)
    F_.append(F)
    gorivo.append(omjer_goriva*100)

def igra(): #vizualizacija simulacije
    global run
    podatci()
    run = True
    while run:
        clock = pygame.time.Clock()
        clock.tick(FPS) #odreduje u koliko fps igra radi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        prikaz_rakete()
        prikaz_podataka()
        faze_rakete()
        sila_teža()
        otpor_zraka()
        izračun_sile()
        izračun_veličina()
        info_graf()
        pygame.display.update()
    
def game_over(): 
    global screen, font
    pozadina = pygame.Surface((screen.get_width(), screen.get_height()))
    pozadina.fill("Black")
    pozadina.set_alpha(200)
    screen.blit(pozadina, (0,0))
    run = True
    while run == True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        PLAY_BUTTON = Button("Grafovi", 70, "black", (screen.get_width()*0.25, screen.get_height()*0.14), "Light Grey", "Green", (screen.get_width()/2, screen.get_height()/2))
        MAIN_BUTTON = Button("Glavni izbornik", 70, "black", (screen.get_width()*0.30, screen.get_height()*0.14), "Light Grey", "dimgray", (screen.get_width()/2, screen.get_height()/1.5))
        QUIT_BUTTON = Button("Izađi", 70, "black", (screen.get_width()*0.25, screen.get_height()*0.14), "Light Grey", "Red", (screen.get_width()/2, screen.get_height()/1.2))
        
        draw_text(f"Završena simulacija!", font, "white", 450,50)
        draw_text(f"{postotak_goriva}% goriva", font, "white", 50,150)
        draw_text(f"Visina {h:.2f} m / {h/1000:.2f} km", font, "white", 50,210)
        draw_text(f"Vrijeme {t} s", font, "white", 50,270)

        for gumb in [PLAY_BUTTON,MAIN_BUTTON, QUIT_BUTTON]:
            if gumb.checkForCollision(MENU_MOUSE_POS):
                gumb.changeButtonColor()
            gumb.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForCollision(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if MAIN_BUTTON.checkForCollision(MENU_MOUSE_POS):
                    run = False
                    main_menu()
                if PLAY_BUTTON.checkForCollision(MENU_MOUSE_POS):
                    run = False
                    graf()

        pygame.display.update()

def graf():
    fig, axs = plt.subplots(4, sharex=True)
    fig.suptitle('Grafovi')
    axs[0].plot(T, H)
    axs[0].set_title("Visina[m] ovisno o vremenu[s]")
    axs[1].plot(T, gorivo)
    axs[1].set_title("Gorivo[%] ovisno o vremenu[s]")
    axs[2].plot(T, v_)
    axs[2].set_title("Brzina[m/s] ovisno o vremenu[s]")
    axs[3].plot(T, F_)
    axs[3].set_title("Sila[N] ovisno o vremenu[s]")
    plt.show()
    main_menu()
main_menu()