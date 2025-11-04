import pygame #importing the pygame library
import pygame.gfxdraw #importing vector graphics module 


pygame.init() # initialises pygame in the program

#----------------------colors
Black      = (0, 0, 0)
White      = (255, 255, 255)
OffWhite   = (242, 241, 239)
Tar        = (24, 24, 24)
LightGreen = (142, 206, 71)
DarkGreen  = (89, 150, 45)
Blue       = (100, 152, 238)
Darkblue   = (40, 94, 197)

#---------------------setup
size = (400, 400) #screen size
screen = pygame.display.set_mode(size) #displaying screen
pygame.display.set_caption("Smart Tank") #display name

font = pygame.font.Font("Roboto-SemiBold.ttf", 14)
#font2 = pygame.font.Font("freesansbold.ttf", 14) #pygames built-in font

done = False #program will run while done is false

clock = pygame.time.Clock() #screen updates

# ----------------------persistent variables for pages
#Efficiency
e_tank_text = ""
e_dist_text = ""
e_active_box = None
e_result = None
e_tank_rect = pygame.Rect(240, 125, 100, 25)
e_dist_rect = pygame.Rect(240, 165, 100, 25)
e_calc_button = pygame.Rect(150, 205, 100, 30)

#Range
r_tank_text = ""
r_eff_text = ""
r_active_box = None
r_result = None
r_tank_rect = pygame.Rect(240, 125, 100, 25)
r_eff_rect = pygame.Rect(240, 165, 100, 25)
r_calc_button = pygame.Rect(150, 205, 100, 30)

#Tank Size
ts_dist_text = ""
ts_eff_text = ""
ts_active_box = None
ts_result = None
ts_dist_rect = pygame.Rect(240, 125, 100, 25)
ts_eff_rect = pygame.Rect(240, 165, 100, 25)
ts_calc_button = pygame.Rect(150, 205, 100, 30)

#Trip Cost
tc_cost_text = ""
tc_eff_text = ""
tc_dist_text = ""
tc_active_box = None
tc_result = None
tc_cost_rect = pygame.Rect(240, 125, 100, 25)
tc_eff_rect = pygame.Rect(240, 165, 100, 25)
tc_dist_rect = pygame.Rect(240, 205, 100, 25)
tc_calc_button = pygame.Rect(150, 245, 100, 30)

#Tank Usage
tu_dist_text = ""
tu_eff_text = ""
tu_tank_text = ""
tu_active_box = None
tu_result = None
tu_dist_rect = pygame.Rect(240, 125, 100, 25)
tu_eff_rect = pygame.Rect(240, 165, 100, 25)
tu_tank_rect = pygame.Rect(240, 205, 100, 25)
tu_calc_button = pygame.Rect(150, 245, 100, 30)


#-----------------------------------------------------------defining popups
'''
To the user only the Menu will seem like a pop-up as they select which calculation they would like to
use as all the calculation pages will look like they are integrated into the main page. However in
the background they are actually acting like pop-ups on top of the main background layer.
'''

def M(screen, font): # menu
    options = ["L/100km or Efficiency", "Range", "Tank Size", "Trip Cost", "Tank Usage"]
    rects = []
    for i, label in enumerate(options):
        rect = pygame.draw.rect(screen, White, [80, 100 + i*30, 240, 25])
        t = font.render(label, True, Black)
        screen.blit(t, (85, 105 + i*30))
        rects.append((rect, i+1))

    if pygame.mouse.get_pressed()[0]:
        for rect, opt_id in rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                return opt_id
    return None

selected_popup = 0

#helper function for all other popups
def calculator_helper(
    screen, font,
    title_text,
    label1, label2, rect1, rect2,
    calc_button_rect,
    active_box, text1, text2,
    events, prev_result,
    calc_function,
    num_inputs=2, label3=None, rect3=None, text3="",
    result_label=None
):
    """Generic calculator UI helper (supports 2 or 3 inputs)."""

    #determineing whether to show result or calculate button
    show_result = prev_result is not None
    result = prev_result

    #title
    title = font.render(title_text, True, Black)
    title_x = (screen.get_width() - title.get_width()) // 2 #titles appear sentered to the screen
    screen.blit(title, (title_x, 95))

    #labels
    screen.blit(font.render(label1, True, Black), (60, 130))
    screen.blit(font.render(label2, True, Black), (60, 170))
    if num_inputs == 3 and label3:
        screen.blit(font.render(label3, True, Black), (60, 210))

    #input boxes
    pygame.draw.rect(screen, White, rect1, 0, 5)
    pygame.draw.rect(screen, White, rect2, 0, 5)
    pygame.draw.rect(screen, Darkblue if active_box == "1" else Black, rect1, 2, 5)
    pygame.draw.rect(screen, Darkblue if active_box == "2" else Black, rect2, 2, 5)
    screen.blit(font.render(text1, True, Black), (rect1.x + 5, rect1.y + 4))
    screen.blit(font.render(text2, True, Black), (rect2.x + 5, rect2.y + 4))

    if num_inputs == 3 and rect3:
        pygame.draw.rect(screen, White, rect3, 0, 5)
        pygame.draw.rect(screen, Darkblue if active_box == "3" else Black, rect3, 2, 5)
        screen.blit(font.render(text3, True, Black), (rect3.x + 5, rect3.y + 4))

    #drawing calculate button or result
    if not show_result:
        pygame.draw.rect(screen, DarkGreen, calc_button_rect, border_radius=5)
        screen.blit(font.render("Calculate", True, White),
                    (calc_button_rect.x + 19, calc_button_rect.y + 7))
    elif result is not None:
        #format text if descriptive label provided
        if isinstance(result, str):
            result_text = result
        elif result_label:
            result_text = f"{result_label} {result}"
        else:
            result_text = str(result)
        rendered = font.render(result_text, True, Black)
        text_x = calc_button_rect.x + (calc_button_rect.width - rendered.get_width()) // 2
        text_y = calc_button_rect.y + (calc_button_rect.height - rendered.get_height()) // 2
        screen.blit(rendered, (text_x, text_y))

    mouse = pygame.mouse.get_pos()

    #event handling
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect1.collidepoint(mouse):
                active_box = "1"
                result = None
            elif rect2.collidepoint(mouse):
                active_box = "2"
                result = None
            elif num_inputs == 3 and rect3 and rect3.collidepoint(mouse):
                active_box = "3"
                result = None
            elif calc_button_rect.collidepoint(mouse) and not show_result:
                try:
                    val1 = float(text1)
                    val2 = float(text2)
                    if num_inputs == 3:
                        val3 = float(text3)
                        result = calc_function(val1, val2, val3)
                    else:
                        result = calc_function(val1, val2)
                except ValueError:
                    result = None
            else:
                active_box = None

        elif event.type == pygame.KEYDOWN and active_box:
            if event.key == pygame.K_BACKSPACE:
                if active_box == "1":
                    text1 = text1[:-1]
                elif active_box == "2":
                    text2 = text2[:-1]
                elif num_inputs == 3 and active_box == "3":
                    text3 = text3[:-1]
                result = None
            elif event.unicode.isdigit() or event.unicode == ".":
                if active_box == "1":
                    text1 += event.unicode
                elif active_box == "2":
                    text2 += event.unicode
                elif num_inputs == 3 and active_box == "3":
                    text3 += event.unicode
                result = None
            elif event.key == pygame.K_RETURN:
                active_box = None

    #returning all state values
    if num_inputs == 3:
        return text1, text2, text3, active_box, result
    else:
        return text1, text2, active_box, result


#---------------------------------------------------------image files
'''
this function isn't necessary for this project as i am not loading many images but if this was a much
larger project this function would be extremely helpful, allowing me to quickly add and change the
direction, rotation, and scale of images.
'''

def load_image(path, size=None, flip=False, rotate=0):
    #Loads, scales, flips, and rotates an image in one step.
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.smoothscale(img, size)
    if flip:
        img = pygame.transform.flip(img, True, False)
    if rotate != 0:
        img = pygame.transform.rotozoom(img, rotate, 1)
    return img

porsche_img = load_image("porsche_930.png", (120, 91), flip=True)
supra_img = load_image("supra.png", (140, 95), flip=True)
r34_img = load_image("r34.png", (49, 33), rotate=-2)
cloud_img = load_image("cloud.png", (270, 85))

#---------------------------------------------------------defining background
'''
This function isn't necessary for this project as I am not loading many images, but if this were a
much larger project, this function would be extremely beneficial, allowing me to quickly add images
and change their direction, rotation and scale.
'''

def draw_background(surface):
    
    #sky
    gradient_sky = [(123, 200, 247), (52, 120, 244)] # start and end colors of the gradient 
    num_gradient_sky_steps = 300  # amount of different stages in the gradient and size of gradient as each stage is one pix (200 will cover half the screen)
    gradient_sky_step = 1 / num_gradient_sky_steps
                    
    for i in range(num_gradient_sky_steps):
            color = tuple(int(gradient_sky[0][c] * (1 - gradient_sky_step * i) + gradient_sky[1][c] * gradient_sky_step * i) for c in range(3))
            pygame.draw.rect(surface, color, (0, i, 400, 1))
    surface.blit(cloud_img, (69, 5))
    
    #grass
    gradient_grass = [(142, 206, 71), (51, 107, 35)] # start and end colors of the gradient 
    num_gradient_grass_steps = 80  # amount of different stages in the gradient and size of gradient as each stage is one pix (200 will cover half the screen)
    gradient_grass_step = 1 / num_gradient_grass_steps
                    
    for i in range(num_gradient_grass_steps):
            color = tuple(int(gradient_grass[0][c] * (1 - gradient_grass_step * i) + gradient_grass[1][c] * gradient_grass_step * i) for c in range(3))
            pygame.draw.rect(surface, color, (0, (i + 300), 400, 1))

    pygame.draw.polygon(surface, DarkGreen, ([0, 300], [300, 300], [0, 275]))
    pygame.draw.aaline(surface, DarkGreen, (0, 275), (300, 300)) #smoother border line for the hills however aaline can not have fill or thickness
    pygame.draw.polygon(surface, LightGreen, ([0, 300], [400, 300], [400, 290]))
    pygame.draw.aaline(surface, LightGreen, (0, 300), (400, 290)) #smoother border line for the hills however aaline can not have fill or thicness

    #foreground road   
    pygame.draw.ellipse(surface, Tar, [-50, 350, 500, 100],)
    #road border
    for i in range(3): #needed to print multiple lines to cover the blockyness of the ellipse
        y = int(399.5 + i * 0.2) #y position value as gfx does not support integers
        pygame.gfxdraw.aaellipse(surface, 200, y, 250, 50, Tar)
    #deviding line
    for i in range(14): 
        y = int(437 + i * 0.1) #y position value as gfx does not support intages
        ellipse = pygame.gfxdraw.aaellipse(surface, 200, y, 250, 50, OffWhite)
    for i in range(5):
        rect = pygame.draw.rect(surface, Tar, [65 + i * 60, 380, 30, 20]) #drawing 5 rectangles 60pix apart to make divided lines 
    surface.blit(porsche_img, (280, 318))
    surface.blit(supra_img, (-10, 315))

    #background road
    pygame.draw.polygon(surface, Tar, ([0, 308], [0, 306], [400, 318], [400, 323]))
    pygame.draw.aaline(surface, Tar, (0, 306), (400, 318))
    pygame.draw.aaline(surface, Tar, (0, 308), (400, 323))
        
    surface.blit(r34_img, (238, 292))
        
# Create static background
background = pygame.Surface(size)
draw_background(background)
background = background.convert()

#--------------------------------------------------------- start loop ------------------------------------------------------------------------
#if x button is clicked quit event is true
while done ==False:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True

#---------------------------------------------------------drawing to screen
    screen.blit(background, (0, 0)) #drawing background created above to the screen

    menu_button = pygame.draw.rect(screen, White, [85, 44, 240, 38])
    if selected_popup ==0:
        text = font.render("What would you like to calculate?", True, Black)
        screen.blit(text, (100, 55))
    else:
        text = font.render("Menu", True, Black)
        screen.blit(text, (185, 55))
    
    if menu_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]: #Checking if the mouse is over the menu button and the user has left clicked
        selected_popup = 0

#---------------------------menu
    if selected_popup == 0:
        choice = M(screen, font)
        if choice:
            selected_popup = choice

#Efficiency
    elif selected_popup == 1:
        #calling inputs from the helper function 
        e_tank_text, e_dist_text, e_active_box, e_result = calculator_helper(
            screen, font,
            "Fuel Efficiency Calculator", #page title 
            "Tank Size (L):", "Distance per Tank (km):", #input lables
            e_tank_rect, e_dist_rect, e_calc_button, #input boxes and calculate button
            e_active_box, e_tank_text, e_dist_text, #curront active inpit box
            events, e_result,
            #calculation
            lambda tank, dist: (
                f"Your fuel efficiency is {round((tank / dist) * 100, 2)} L/100 km"
            ) if dist > 0 else "Invalid input"
        )

#Range
    elif selected_popup == 2:
        r_tank_text, r_eff_text, r_active_box, r_result = calculator_helper(
            screen, font,
            "Range Calculator", #page title 
            "Tank Size (L):", "Fuel Efficiency (L/100 km):", #input lables
            r_tank_rect, r_eff_rect, r_calc_button, #input boxes and calculate button
            r_active_box, r_tank_text, r_eff_text, #curront active inpit box
            events, r_result,
            #calculation
            lambda tank, eff: (
                f"Your range is {round((tank / eff) * 100, 2)} km"
            ) if eff > 0 else "Invalid input"
        )


# Tank Size
    elif selected_popup == 3:
        ts_dist_text, ts_eff_text, ts_active_box, ts_result = calculator_helper(
            screen, font,
            "Tank Size Calculator", #page title
            "Distance / Range (km):", "Fuel Efficiency (L/100 km):", #input lables
            ts_dist_rect, ts_eff_rect, ts_calc_button, #input boxes and calculate button
            ts_active_box, ts_dist_text, ts_eff_text, #curront active inpit box
            events, ts_result,
            #calculation
            lambda dist, eff: (
                f"Your tank size is {round(dist * eff / 100, 2)} L"
            ) if eff > 0 else "Invalid input"
        )
            
#Trip Cost
    elif selected_popup == 4:
        tc_cost_text, tc_eff_text, tc_dist_text, tc_active_box, tc_result = calculator_helper(
            screen, font,
            "Trip Cost Calculator", #page title
            "Fuel Cost ($/L):", "Fuel Efficiency (L/100 km):", #input lables
            tc_cost_rect, tc_eff_rect, tc_calc_button, #input boxes and calculate button
            tc_active_box, tc_cost_text, tc_eff_text, #curront active inpit box
            events, tc_result,
            #calculation
            lambda cost, eff, dist: (
                f"Your trip cost is ${(dist / 100) * eff * cost:.2f}"
            ) if cost > 0 and eff > 0 and dist > 0 else "Invalid input",
            num_inputs=3,
            label3="Trip Distance (km):", #third input lable
            rect3=tc_dist_rect, text3=tc_dist_text
        )

#Tank Usage
    elif selected_popup == 5:
        tu_dist_text, tu_eff_text, tu_tank_text, tu_active_box, tu_result = calculator_helper(
            screen, font,
            "Tank Usage Calculator", #page title
            "Trip Distance (km):", "Fuel Efficiency (L/100 km):", #input lables
            tu_dist_rect, tu_eff_rect, tu_calc_button, #input boxes and calculate button
            tu_active_box, tu_dist_text, tu_eff_text, #curront active inpit box
            events, tu_result,
            #calculation
            lambda dist, eff, tank: (
                f"You have used {min(100, (dist / 100 * eff) / tank * 100):.1f}% of your tank and have {max(0, tank / eff * 100 - dist):.1f} km left."
            ) if eff > 0 and tank > 0 and dist >= 0 else "Invalid input",
            num_inputs=3,
            label3="Tank Size (L):", #third input lable
            rect3=tu_tank_rect, text3=tu_tank_text
        )

    pygame.display.flip()
    clock.tick(30)

#if done event is true the program will quit
if done ==True:
    pygame.quit()
#-------------------------------------------------------- end loop ----------------------------------------------------------------------
