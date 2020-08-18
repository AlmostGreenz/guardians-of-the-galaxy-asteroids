
class Asteroid():
    """ Stores an asteroid, made up of its attributes """
    def __init__(self, diameter = 5, x = 5, y = 5):
        self.x = x
        self.y = y
        self.xVelocity = random(-1.5, 1.5) # randomly assigns initial movement
        self.yVelocity = random(-1.5, 1.5)
        self.diameter = diameter * 10
    
    def move(self):
        """ Relocates the asteroids based on their predefined speed """
        self.x += self.xVelocity
        self.y += self.yVelocity
        
    def render(self):
        """ Draws the asteroids to the screen """
        #noStroke()
        fill(100, 120, 100)
        ellipse(self.x, self.y, self.diameter, self.diameter)
        
    def checkCollision(self, missile):
        """ Checks if the asteroid collides with a missile """
        return sqrt(((self.x - missile.x)**2) + ((self.y - missile.y)**2)) < ((self.diameter / 2) + (missile.diameter / 2))
    

class Player():
    """ Stores the player's attributes """
    def __init__(self):
        self.x = 300
        self.y = 400
        self.xVelocity = 0
        self.yVelocity = 0
        self.rotation = 0
        self.score = 0
        self.lives = 3
        self.accelerating = False # True => accelerating
        self.rotating = 0  # -1 => clockwise, 1 => counter-clockwise
        self.magazine = 5 # number of fireable missiles at the current time
    
    def move(self):
        """ Moves the player's current location and applies friction """
        self.x += self.xVelocity
        self.y += self.yVelocity 
        
        # FRICTION
        # horizontally
        if self.xVelocity > 0:
            self.xVelocity -= 0.05
            if self.xVelocity < 0:
                self.xVelocity = 0
        
        elif self.xVelocity < 0:
            self.xVelocity += 0.05
            if self.xVelocity > 0:
                self.xVelocity = 0
        
        # vertically
        if self.yVelocity > 0:
            self.yVelocity -= 0.05
            if self.yVelocity < 0:
                self.yVelocity = 0
        
        elif self.yVelocity < 0:
            self.yVelocity += 0.05
            if self.yVelocity > 0:
                self.yVelocity = 0
        
    
    def acceleration(self):
        """ Applies the acceleration to the player """
        if ((self.accelerating) and (-6 < self.xVelocity < 6) and (-6 < self.yVelocity < 6)): # checks if velocity has gotten too high
            self.xVelocity += 0.15 * cos(radians(self.rotation)) # sin & cos applies the acceleration
            self.yVelocity += 0.15 * sin(radians(self.rotation)) # at the rotation angle
        
    
    def turn(self):
        """ Rotates the player """
        if self.rotating == 1:
            self.rotation -= 1
        
        elif self.rotating == -1:
            self.rotation += 1
            
    def reload(self, numMissile):
        """ Reloads the magazine """
        self.magazine = 5 - numMissile
        
    
    def render(self):
        """ Draws the player to the screen """
        imageMode(CENTER)
        
        if self.accelerating == 0: # changes image to a ship with thrusters active if accelerating
            image(imgs["idle"], 20, 0, imgs["idle"].width / 10, imgs["idle"].height / 10)
        else:
            image(imgs["move"], 20, 0.65, imgs["move"].width / 12.5, imgs["move"].height / 12.5)
            
        imageMode(CORNER)
        
        """
        # Hitbox
        fill(255, 255, 255, 50)
        ellipse(18, 0, 66, 66)
        """
        
    def checkCollision(self, rock):
        """ Checks if the player collides with an asteroid """
        return sqrt(((self.x - rock.x)**2) + ((self.y - rock.y)**2)) < (33 + (rock.diameter / 2))
    
    def destroy(self):
        """ Destroys the ship """
        imageMode(CENTER)
        image(imgs["explosion"], self.x + 15, self.y, imgs["explosion"].width / 4, imgs["explosion"].height / 4)
        imageMode(CORNER)
        self.lives -= 1
        self.x = 300
        self.y = 400
        self.xVelocity = 0
        self.yVelocity = 0
    
    
class Missile():
    """ Stores a missile fired """
    def __init__(self, x, y, rotation):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.diameter = 10
        self.timer = millis()
    
    def move(self):
        """ Moves the missile """
        self.x += 4 * cos(radians(self.rotation))
        self.y += 4 * sin(radians(self.rotation))
    
    def render(self):
        """ Draws the missile to the screen """
        fill(200)
        ellipse(5, 0, self.diameter, self.diameter)
    
    def checkTime(self):
        """ Set the missile to last 3.5 seconds """
        return (millis() - self.timer) > 3500


class Mode():
    """ Stores the current mode """
    def __init__(self):
        self.which = "menu"
    
    def render(self):
        """ Draws the mode's background """
        image(imgs["planet"], 0, 0, 800, 600)
        
        
    
        
def checkOver(element): 
    """ Warps specified element to other side of screen (if off) """
    if (element.x < -55): # too far left
        element.x = 815    
    
    elif (element.x > 835): # too far right
        element.x = -50
    
    elif (element.y < -55): # too far up
        element.y = 615
    
    elif (element.y > 635): # too far down
        element.y = -35
    
         
field = []
for n in range(3):
    field.append(Asteroid())


    
currentShots = []
    
rocket = Player()

currentMode = Mode()

    
def setup():
    """ Runs once at beginning of execution """
    global imgs
    size(800, 600)
    imgs = {"logo" : loadImage("GOTGLogo.png"), "babyGroot" : loadImage("babyGroot.png"), "cassette" : loadImage("AwesomeMix.png"), \
            "planet" : loadImage("morag.png"), "idle" : loadImage("milanoIdle.png"), "move" : loadImage("milanoMove.png"), "explosion" : loadImage("explosion.png"), "orb" : loadImage("orb.png")}

    
def draw():
    """ Runs repeatedly """
    
    currentMode.render()
    
    if currentMode.which == "menu": # Main Menu
        imageMode(CENTER) 
        image(imgs["logo"], 400, 125, imgs["logo"].width / 2.5, imgs["logo"].height / 2.5) # draws game logo
        
        # SPACE JUNK (on menu); draws image where 'asteroid' would be
        for item in range(3):
            field[item].move()
        
        image(imgs["babyGroot"], field[0].x, field[0].y, imgs["babyGroot"].width / 12.5, imgs["babyGroot"].height / 12.5)
        image(imgs["cassette"], field[1].x, field[1].y, imgs["cassette"].width / 12.5, imgs["cassette"].height / 12.5)
        image(imgs["orb"], field[2].x, field[2].y, imgs["orb"].width / 12, imgs["orb"].height / 12)
        
        checkOver(field[0])
        checkOver(field[1])
        
        imageMode(CORNER)
        
        textMode(CENTER)
        text("Press any key to start!", 340, 300)
        textMode(CORNER)
    
    elif currentMode.which == "play": # during gameplay
    
        # ASTEROIDS:
        asteroidAdjustment = 0
        shotAdjustment = 0
        
        for asteroid in range(len(field)):
            field[asteroid - asteroidAdjustment].move() # Draws the asteroid
            field[asteroid - asteroidAdjustment].render()
            checkOver(field[asteroid - asteroidAdjustment])
            
            if rocket.checkCollision(field[asteroid - asteroidAdjustment]): # Checks collision with the player
                rocket.destroy()
                
                if (field[asteroid - asteroidAdjustment].diameter / 10) < 5:  # Deletes the asteroid if it is not the largest type (type 5)                
                    field.pop(asteroid - asteroidAdjustment)
                    asteroidAdjustment += 1
            
            tempShots = len(currentShots)
            for shot in range(tempShots): # Checks collision with missiles
                
                if field[asteroid - asteroidAdjustment].checkCollision(currentShots[shot - shotAdjustment]):
                    currentShots.pop(shot - shotAdjustment)
                    shotAdjustment += 1
                    if (field[asteroid - asteroidAdjustment].diameter / 10) > 1: # Splits the asteroid into 3 smaller ones
                        for n in range(3):
                            field.append(Asteroid((field[asteroid - asteroidAdjustment].diameter / 10) // 2, field[asteroid - asteroidAdjustment].x, field[asteroid - asteroidAdjustment].y))
                    
                    rocket.score += int(25 * (6 -(field[asteroid - asteroidAdjustment].diameter / 10))) # updates the score (smaller asteroid = higher points)   
                                
                    field.pop(asteroid - asteroidAdjustment) # Deletes the destroyed asteroid
                    asteroidAdjustment += 1
            
            if len(field) < 4:
                for newAst in range(7): # replenishes the asteriods once too many are destroyed
                    field.append(Asteroid((random(1,5))))
                    
            
        # MISSILES:
        shotAdjustment = 0
        for shot in range(len(currentShots)):
            
            pushMatrix() # Draws the missile
            translate(currentShots[shot - shotAdjustment].x, currentShots[shot  - shotAdjustment].y)
            rotate(radians(currentShots[shot  - shotAdjustment].rotation))
            currentShots[shot  - shotAdjustment].move()
            currentShots[shot  - shotAdjustment].render()
            popMatrix()
            
            if currentShots[shot  - shotAdjustment].checkTime(): # Deletes the missile if its time limit has been passed (3.5s)
                currentShots.pop(shot  - shotAdjustment)
                shotAdjustment += 1
            
                
                    
        # ROCKET:
        rocket.move()
        rocket.acceleration()
        rocket.turn()
        rocket.reload(len(currentShots))
        pushMatrix()
        translate(rocket.x, rocket.y)
        rotate(radians(rocket.rotation))
        rocket.render()
        checkOver(rocket)
        popMatrix()
        
        fill(140, 230, 225)
        text("Score: %s"%rocket.score, 5, 595)
        text("Lives: %s"%rocket.lives, 745, 595)
                
        

def keyPressed():
    """ Starts keys' corresponding functions """
    if currentMode.which == "menu": # starts game from main menu
        currentMode.which = "play"
        field = [] 
        for n in range(15): # creates game's asteroids
            field.append(Asteroid())
    
    elif key == 'W' or key == 'w':
        rocket.accelerating = True        
        
    elif key == 'A' or key == 'a':
        rocket.rotating = 1
    
    elif key == 'D' or key == 'd':
        rocket.rotating = -1
    
    
        
        
def keyReleased():
    """ Stops keys' corresponding functions """
    if (key == 'W' or key == 'w'):
        rocket.accelerating = False
    
    elif ((key == 'A' or key == 'a') and (rocket.rotating != -1)) or ((key == 'D' or key == 'd') and (rocket.rotating != 1)):
        rocket.rotating = 0
   
def mousePressed():
    """ Fires missiles when mouse pressed """
    if rocket.magazine > 0:
        currentShots.append(Missile(rocket.x, rocket.y, rocket.rotation))
    
