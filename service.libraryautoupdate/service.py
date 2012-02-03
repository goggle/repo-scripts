import time
import xbmc
import xbmcaddon
                
class AutoUpdater:
    addon_id = "service.libraryautoupdate"
    Addon = xbmcaddon.Addon(addon_id)
    datadir = "special://userdata/addon_data/" + addon_id + "/"
    
    def runProgram(self):
        #setup the timer amounts
        timer_amounts = {}
        timer_amounts['0'] = 1
        timer_amounts['1'] = 2
        timer_amounts['2'] = 5
        timer_amounts['3'] = 10
        timer_amounts['4'] = 15
        timer_amounts['5'] = 24
           
        #check if we should delay the first run
        if(int(self.Addon.getSetting("startup_delay")) != 0):
            self.readLastRun()
            
            #check if we would have run an update anyway
            if(time.time() >= self.last_run + (timer_amounts[self.Addon.getSetting('timer_amount')] * 60 * 60)):
                #trick system by subtracting the timer amount then adding a delay (now - timer + delay = nextrun)
                self.last_run = time.time() - (timer_amounts[self.Addon.getSetting('timer_amount')] * 60 *60) + (int(self.Addon.getSetting("startup_delay")) * 60)
                self.writeLastRun()
                xbmc.log("Setting delay at " + self.Addon.getSetting("startup_delay") + " minute")
            
        while(not xbmc.abortRequested):
            now = time.time()
            sleep_time = 10
            self.readLastRun()

            #check if we should run an update
            if(now >= self.last_run + (timer_amounts[self.Addon.getSetting('timer_amount')] * 60 * 60)):

                #make sure player isn't running
                if(xbmc.Player().isPlaying() == False):
                    
                    if(self.scanRunning() == False):

                        self.runUpdates()

                        xbmc.log("Update Library will run again in " + str(timer_amounts[self.Addon.getSetting("timer_amount")]) + " hours")
                        
                else:
                    xbmc.log("Player is running, waiting until finished")
                    
            #put the thread to sleep for x number of seconds
            time.sleep(sleep_time)
            
    def scanRunning(self):
        #check if any type of scan is currently running
        if(xbmc.getCondVisibility('Library.IsScanningVideo') or xbmc.getCondVisibility('Library.IsScanningMusic')):
            return True
        else:
            return False
        
    def runUpdates(self):
        #run the update
        if(self.Addon.getSetting('update_video') == 'true'):
            xbmc.log('Updating Video')
            xbmc.executebuiltin('UpdateLibrary(video)')
            time.sleep(1)
                            
        if(self.Addon.getSetting('update_music') == 'true'):
            #check if scan is running again, wait until finished if it is
            while(self.scanRunning()):
                time.sleep(10)
                            
            xbmc.log('Update Music')
            xbmc.executebuiltin('UpdateLibrary(music)')

        #reset the last run timer    
        self.last_run = time.time()
        self.writeLastRun()

    def readLastRun(self):
        
        try:
            f = open(xbmc.translatePath(self.datadir + "last_run.txt"),"r")
            self.last_run = float(f.read())
            f.close()
        except IOError:
            #the file doesn't exist, most likely first time running
            self.last_run = 0
        

    def writeLastRun(self):
        f = open(xbmc.translatePath(self.datadir + "last_run.txt"),"w")
        
        #write out the value for the last time the program ran
        f.write(str(self.last_run));
        f.close();

