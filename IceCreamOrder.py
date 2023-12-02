# By: Cassie Stevens 11/3/2023
# Project for CS335
# 'Ice Cream Parlor' Game
import random               #For randomizing
from PIL import Image
import sounddevice as sd    #For music
import soundfile as sf      #For music

class IceCreamOrder:
#Constructor
    def __init__(self):
        #Score for user
        self.score = 0
        #The order number
        self.orderNum  = 0
        self.streak = 0
        #The number of scoops in the order, which can be 1, 2, or 3 scoops
        #Defaulting as 1, but will randomly generated for each order
        self.scoopNum   = 1
        #To keep track of how many scoops are made by user
        self.userScoopMaking = self.scoopNum
        
        #Default Order
        self.orderFlavors   = [None]*3
        self.orderToppings  = ["No Topping"]*3
        self.orderContainer = ""
        
        #User's Choices
        self.userFlavors    = [None]*3
        self.userToppings   = ["No Topping"]*3
        self.userContainer  = ""
        self.userIceCream   = None
        
        #Images of Ice Cream Scoops
        self.scoopImages    = [None]*3
        self.userScoops     = [None]*3
        #Image of Ice Cream Final
        self.iceCreamOrder  = None
        
#Method: Get the randomly generated ice cream order
    def takeOrder(self):
        self.orderNum += 1
        #Options at the Ice Cream Parlor
        listOfFlavors      = ["Vanilla", "Chocolate", "Strawberry"]
        listOfToppings     = ["Sprinkles", "Chocolate Chips", "Cherry", "No Topping"]
        listOfConesAndCup  = ["Waffle Cone", "Cake Cone", "Cup"]
        #Get the number of scoops
        self.scoopNum = random.randrange(1,4)
        #Update the num of scoops
        self.userScoopMaking = self.scoopNum
        #Get what the ice cream is put in
        self.orderContainer = random.choice(listOfConesAndCup)
        #Reset the lists
        self.orderFlavors   = [None]*3
        self.orderToppings  = ["No Topping"]*3
        #Get each scoop of ice cream and its topping
        for x in range(self.scoopNum):
            #Will always get at least one scoop of ice cream
            self.orderFlavors[x]    = random.choice(listOfFlavors)
            self.orderToppings[x]   = random.choice(listOfToppings)
            #A cherry can only go on the top scoop (when x = 0)
            while x != 0:
                if self.orderToppings[x] == "Cherry":
                    self.orderToppings[x] = random.choice(listOfToppings)
                else:
                    break

#Method: Get single scoops for the user
    def singleScoop(self):
        userFlavorImg   = f'{self.userFlavors[self.userScoopMaking-1]}.png'
        userToppingImg  = f'{self.userToppings[self.userScoopMaking-1]}.png'
        layer1 = Image.open(userFlavorImg) #Name of ice cream png
        if userToppingImg == 'No Topping.png':
            userScoop = layer1
        else: #Add topping
            layer2 = Image.open(userToppingImg)
            if userToppingImg == 'Cherry.png':
                userScoop = self.addCherry(layer1)
            else:
                #Compositing image using Image.alpha_composite
                userScoop = Image.new("RGBA", layer1.size)
                userScoop = Image.alpha_composite(userScoop, layer1)
                userScoop = Image.alpha_composite(userScoop, layer2)
        userScoop.save("userScoop.png", format="png")
        #Add user scoop images to list
        self.userScoops[self.userScoopMaking-1] = userScoop
                
#Method: Create the images for the ice cream scoops
    def scoopImage(self):
        for x in range(self.scoopNum):
            #Get the name of the .png image file for
            #the flavor and topping of scoop x
            flavorImg   = f'{self.orderFlavors[x]}.png'
            toppingImg  = f'{self.orderToppings[x]}.png'

            #Get the image for the ice cream
            iceCreamLayer = Image.open(flavorImg)

            #The cherry will be added elsewhere, so leave as is
            if toppingImg in ['No Topping.png', 'Cherry.png']:
                finalScoop = iceCreamLayer

            #Add the topping
            else:
                #Get the image for the topping
                toppingLayer = Image.open(toppingImg)
                
                #Get the composite image with the topping on the ice cream
                #using Image.alpha_composite
                finalScoop = Image.new("RGBA", iceCreamLayer.size)
                finalScoop = Image.alpha_composite(finalScoop, iceCreamLayer)
                finalScoop = Image.alpha_composite(finalScoop, toppingLayer)

            self.scoopImages[x] = finalScoop

#Method: Get the image for the final order
    def getFinalOrder(self):
        #Get the images of the ice cream scoops
        self.scoopImage()
        #Number of scoops
        y = self.scoopNum
        #Set the default as 1 scoop
        stack = self.scoopImages[y-1]
        #Only combine scoops if there are more than one scoops in the order
        while y != 1: 
            #Get the image for bottom 2 scoops
            stack = self.getStackScoops(stack, self.scoopImages[y-2])
            #Decrease by 1 so that the next loop will get the 
            #stacked scoops image with the third scoop added
            y -= 1
        #Check if a cherry is on top
        if self.orderToppings[0]  == "Cherry":
            stack = self.addCherry(stack)
        #
        self.iceCreamOrder = self.addStackContainer(stack)
        # Save this image 
        self.iceCreamOrder.save("order.png", format="png")

#Method: Get an image with the stacked scoops of ice cream from the provided images
    def getStackScoops(self, iceCreamScoops, addToStack):
        #Open Front Image 
        addToStack = addToStack 
        #Open Background Image 
        iceCreamScoops = iceCreamScoops
        #Convert image to RGBA 
        addToStack = addToStack.convert("RGBA") 
        #Convert image to RGBA 
        iceCreamScoops = iceCreamScoops.convert("RGBA") 
        #Calculate width to be at the center
        #All scoops are the same size 
        width = 0
        #Calculate height to be at the center 
        height = (addToStack.height)// 2
        scoopStack = Image.new('RGB', (iceCreamScoops.width, iceCreamScoops.height + height))
        #Paste onto the new image
        scoopStack.paste(iceCreamScoops, (0, scoopStack.height-iceCreamScoops.height), iceCreamScoops) 
        scoopStack.paste(addToStack,(width,0), addToStack)
        return scoopStack
    
#Method: Add the cherry on top of the image, and return the image
    def addCherry(self, scoopStack):
        #Open Front Image 
        cherry = Image.open("Cherry.png") 
        #Open Background Image 
        iceCreamScoops = scoopStack
        #Convert image to RGBA 
        cherry = cherry.convert("RGBA") 
        #Convert image to RGBA 
        iceCreamScoops = iceCreamScoops.convert("RGBA") 
        #Calculate width to be at the center 
        #Had to adjust since the stem of the cherry moves it over some
        width = (iceCreamScoops.width - cherry.width) // 2 + 20
        #Calculate height of cherry 
        height = cherry.height-iceCreamScoops.height // 8
        stack = Image.new('RGB', (iceCreamScoops.width, iceCreamScoops.height + height))
        #Paste the ice cream scoops
        stack.paste(iceCreamScoops, (0, stack.height-iceCreamScoops.height), iceCreamScoops)
        #Paste the cherry 
        stack.paste(cherry,(width,0), cherry)
        return stack

#Method: Add the container to an image with the stacked scoops of ice cream
    def addStackContainer(self, scoopStack):
        #Container Image 
        containerFileName = f'{self.orderContainer}.png'
        #Open Front Image 
        iceCreamContainer = Image.open(containerFileName)
        #Open Background Image 
        scoopStack = scoopStack 
        #Convert image to RGBA 
        iceCreamContainer = iceCreamContainer.convert("RGBA") 
        #Convert image to RGBA 
        scoopStack = scoopStack.convert("RGBA") 
        #Calculate width to be at the center 
        width   = (iceCreamContainer.width - scoopStack.width) // 2
        #Calculate height so ice cream is in the container 
        height  = scoopStack.height-100
        order   = Image.new('RGB', (iceCreamContainer.width, iceCreamContainer.height + height))
        #Paste the frontImage at (width, height) 
        order.paste(scoopStack,(width,0), scoopStack)
        order.paste(iceCreamContainer, (0, order.height-iceCreamContainer.height), iceCreamContainer)
        return order 

#Method: Get the image for the final order
    def getFinalOrder(self):
        self.scoopImage()
        y = self.scoopNum
        #Set the default as 1 scoop
        stack = self.scoopImages[y-1]
        #Only combine scoops if there are more than one scoop in the order
        while y != 1: 
            #Get the image for bottom 2 scoops
            stack = self.getStackScoops(stack, self.scoopImages[y-2])
            #Decrease by 1 so that the next loop will get the 
            #stacked scoops image with the third scoop added
            y -= 1
        #Check if a cherry is on top
        if self.orderToppings[0]  == "Cherry":
            stack = self.addCherry(stack)
        #
        self.iceCreamOrder = self.addStackContainer(stack)
        # Save this image 
        self.iceCreamOrder.save("order.png", format="png")

#Method: Reset user's choices
    def resetUserIceCream(self):
        #Reset user's choices to default
        self.userScoopMaking = self.scoopNum
        self.userFlavors    = [None]*3
        self.userToppings   = ["No Topping"]*3
        self.userContainer  = ""
        self.userIceCream   = None
    
#Method: Compare user's ice cream to the order
    def compareIceCream(self):
        #Check the container matches
        if self.orderContainer == self.userContainer:   #Container is right
            for x in range(self.scoopNum):  #Check flavors and toppings        
                if self.orderFlavors[x] == self.userFlavors[x] and self.orderToppings[x] == self.userToppings[x]:
                    orderMatch = True   #Scoop(s) is/are right
                else: #Scoop(s) is/are wrong
                    orderMatch = False
                    break
        else:   #Container is wrong
            orderMatch = False
        return orderMatch
    
#Method: Play Music
    def playMusic(self, music):
        match music:
            case 'game1':
                data, fs = sf.read('IceCreamMusicLong1.wav')
            case 'game2':
                data, fs = sf.read('IceCreamMusicLong4.wav')
            case 'gameOver':
                data, fs = sf.read('IceCreamMusicGameEnd.wav')
            case _:
                data, fs = sf.read('IceCreamMusicLong4.wav')
        sd.play(data,fs, loop = False)