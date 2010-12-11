from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import thread
import sys
sys.path.append('broker')
from Broker import *
from BrokerCallBack import *
from Message import *



class MsgHandler(BrokerCallBack):
    def setClient(self, agclient):
        self.client = agclient
    
    def receive(self,request, response):
        if request.getString("mid") == "init":
            self.client.loadTerrain()
            self.client.createWorld(request)
            #print request.toString()
            
            self.client.myPlayerID = request.getObjectID()
            print self.client.myPlayerID
            self.client.myPlayer = self.client.objectDic[self.client.myPlayerID]
            
        #elif request.getString("mid") == "move":
        #    self.client.moveObject(request)
        #elif request.getString("mid") == "plUpdate":
        #    pass
        return 0
    
        
class Object:
    pass

class AGClient(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.objectDic = {}
        self.keyboardLock = thread.allocate_lock()
        self.initControls()
        
        self.b = Broker()
        self.MH = MsgHandler()
        self.MH.setClient(self)
        self.b.registerCallBack(self.MH)

        self.b.setAuthenticationData("test1","test")
        self.b.setServerName("AztecServer")
        self.b._registrarAddress = "127.0.0.1"
        
        self.b.init()
        

        #self.fakeInit(self.MH)

        #init-login

    def fakeInit(self, msgH):
        m = Message()
        m.setString("mid", "init")

        m.setInteger("numTrees", 2)
        m.setDouble("xTree0", -5.0)
        m.setDouble("yTree0", -5.0)
        m.setDouble("xTree1", -5.0)
        m.setDouble("yTree1", -2.0)

        m.setInteger("numHuts", 2)
        m.setDouble("xHut0", -5.0)
        m.setDouble("yHut0", -5.0)
        m.setDouble("xHut1", -5.0)
        m.setDouble("yHut1", -2.0)


        

        dummy = Message()
        msgH.receive(m, dummy)
        
    def createObject(self,key,objectType, xpos,ypos,head):
        o = Object()        
        o.x = xpos
        o.y = ypos
        o.h = head
        o.oType = objectType
        
        if o.oType == "coin":
            o.model = self.loader.loadModel("models/coin")  
        elif o.oType == "player":
            o.model = self.loader.loadModel("models/shit")
        elif o.oType == "aztec":
            o.model = self.loader.loadModel("models/coin")

        self.objectDic[key] = o
        self.objectDic[key].model.reparentTo(self.render)
        self.objectDic[key].model.setScale(0.5, 0.5, 0.5)
        self.objectDic[key].model.setPos(o.x,o.y,0)
        
    def createTree(self, xpos, ypos):
        mod = self.loader.loadModel("models/shit")
        texture = loader.loadTexture("models/maps/envir-reeds.png")
        mod.setTexture(texture)
        mod.reparentTo(self.render)
        mod.setScale(0.5,0.5,0.5)
        mod.setPos(xpos,ypos,0)
        
    def createHut(self, xpos, ypos):
        mod = self.loader.loadModel("models/hut")
        mod.reparentTo(self.render)
        mod.setScale(0.5,0.5,0.5)
        mod.setPos(xpos,ypos,0)
        
    def createFort(self, xpos, ypos):
        mod = self.loader.loadModel("models/coin")
        mod.reparentTo(self.render)
        mod.setScale(0.5,0.5,0.5)
        mod.setPos(xpos,ypos,0)
        
    def createChest(self, xpos, ypos):
        mod = self.loader.loadModel("models/chest")
        mod.reparentTo(self.render)
        mod.setScale(0.5,0.5,0.5)
        mod.setPos(xpos,ypos,0)

    def movePlayerTask(self, task):
        #define stuff here
        pass
    def moveObject(self, m):
        o = pobjectDic[m.getInteger("ID")]
        o.x = m.getDouble("x")
        o.y = m.getDouble("y")
        o.h = m.getDouble("h")
        o.model.setPos(o.x,o.y,0)
        
    def changeHeading(self, key):
        if key == "arrow_up":
            self.up = 1
        elif key == "arrow_up-up":
            self.up = 0
        elif key == "arrow_down":
            self.down = 1
        elif key == "arrow_down-up":
            self.down = 0
        elif key == "arrow_left":
            self.left = 1
        elif key == "arrow_left-up":
            self.left = 0
        elif key == "arrow_right":
            self.right = 1
        elif key == "arrow_right-up":
            self.right = 0
        vmove = self.up
        vmove = vmove - self.down
        hmove = self.right
        hmove = hmove -self.left
        heading = 1000.0
        if hmove > 0:
            heading = 90.0
        elif hmove < 0:
            heading = 270
        if vmove > 0:
            heading = 0.0
            if hmove > 0:
                heading = 45
            elif hmove < 0:
                heading = 315
        elif vmove < 0:
            heading = 180.0
            if hmove > 0:
                heading = 135.0
            elif hmove < 0:
                heading = 225.0
        print heading
    def initControls(self):
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0
        self.keyboardLock.acquire()
        self.accept("arrow_up", self.changeHeading, ["arrow_up"])
        self.keyboardLock.release()
        self.keyboardLock.acquire()
        self.accept("arrow_up-up", self.changeHeading, ["arrow_up-up"])
        self.keyboardLock.release()
        self.keyboardLock.acquire()
        self.accept("arrow_down", self.changeHeading, ["arrow_down"])
        self.keyboardLock.release()
        self.keyboardLock.acquire()
        self.accept("arrow_down-up", self.changeHeading, ["arrow_down-up"])
        self.keyboardLock.release()
        self.keyboardLock.acquire()
        self.accept("arrow_left", self.changeHeading, ["arrow_left"])
        self.keyboardLock.release()
        self.keyboardLock.acquire()
        self.accept("arrow_left-up", self.changeHeading, ["arrow_left-up"])
        self.keyboardLock.release()
        self.keyboardLock.acquire()
        self.accept("arrow_right", self.changeHeading, ["arrow_right"])
        self.keyboardLock.release()
        self.keyboardLock.acquire()
        self.accept("arrow_right-up", self.changeHeading, ["arrow_right-up"])
        self.keyboardLock.release()
        
    def loadTerrain(self):
        self.environ = self.loader.loadModel("models/ground")
        #Reparent the model to render.
        self.environ.reparentTo(self.render)
        #Apply scale and position transforms on the model.
        self.environ.setScale(2, 2, 2)
        self.environ.setPos(-150, -150, -1)
            
    def createWorld(self, m):
        print "init recieved\n"

        #non-Static Objects###############################
        numPlayers = m.getInteger("numPlayers")
        for i in range(numPlayers+1):
            tmpstr = "Player" + str(i+1)
            self.createObject(m.getInteger("player" + str(i+1)),
                         "player",
                         m.getDouble("x" + tmpstr),
                         m.getDouble("y" + tmpstr),
                         m.getDouble("h" + tmpstr))
            
        '''numAztecs = m.getInteger("numAztecs")
        for i in range(numAztecs):
            tmpstr = "Aztec" + str(i)
            self.createObject(m.getInteger(aztec + str(i)),
                         "aztec",
                         m.getDouble("x" + tmpstr),
                         m.getDouble("y" + tmpstr),
                         m.getDouble("h" + tmpstr))'''
        
        '''numCoins = message.getInteger("numCoins")
        for i in range(numCoins):
            tmpstr = "Coin" + str(i)
            self.createObject(m.getInteger(coin + str(i)),
                         "coin",
                         m.getDouble("x" + tmpstr),
                         m.getDouble("y" + tmpstr),
                         m.getDouble("h" + tmpstr))'''
        #static objects####################################
        numTrees = m.getInteger("numTrees")
        for i in range(numTrees+1):
            tmpstr = "Tree" + str(i+1)
            self.createTree(m.getDouble("x" + tmpstr),
                            m.getDouble("y" + tmpstr))
        
        numHuts = m.getInteger("numHuts")
        for i in range(numHuts+1):
            tmpstr = "Hut" + str(i+1)
            self.createHut(m.getDouble("x" + tmpstr),
                              m.getDouble("y" + tmpstr))
        
        

        self.createChest(m.getDouble("xChest"), m.getDouble("yChest"))
        self.createFort(m.getDouble("xFort"), m.getDouble("yFort"))

app = AGClient()
app.run()

