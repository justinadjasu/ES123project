import numpy as np
import pandas as pd

# global constants 
bv = 5 # L
dt = 1 # min

class concentration_equation:
    def __init__(self, afferent=50, efferent=10, initial_concentration=20, production_rate=0, hct=0.3, blood_volume=bv, kf=3, r=8):
        self.afferent = afferent # mmhg
        self.efferent = efferent # mmhg
        self.initial_concentration = initial_concentration # mol/L
        self.production_rate = production_rate # M/min
        self.blood_volume = blood_volume # L
        self.hct = hct
        self.c = initial_concentration 
        self.kf = kf 
        self.minutes = 0
        self.r = r # micrometers
        self.old_bv = blood_volume
        return

    def calc_GFR(self):
        GFR = self.kf * (self.afferent - self.efferent) * 1e-3 # L/min
        return GFR

    # calculate GFR at new time step
    def new_concentration(self):
        c_new = self.c - ((self.GFR * self.c)/(self.blood_volume * (1 - self.hct))) + self.production_rate
        return c_new

    def progress(self):
        # calculate change
        self.c = self.old_bv * self.c / self.blood_volume
        self.old_bv  = self.blood_volume
        self.GFR = self.calc_GFR()
        self.c = self.new_concentration()
        self.minutes += 1
        return self.c

    def surface(self):
        # plasma_vol = (1 - self.hct) * self.blood_volume

        # mass = self.c * plasma_vol
        
        # create square grid for capillary cross-section
        N = 200
        x = np.linspace(-self.r/2, self.r/2, N)
        y = np.linspace(-self.r/2, self.r/2, N)

        xx, yy = np.meshgrid(x, y)

        # 
        c = np.zeros((N, N))

        for i in range(len(xx)):
            c[i][xx[i]**2 + yy[i]**2 <= self.r] = self.c * (self.r - np.sqrt(xx[i][xx[i]**2 + yy[i]**2 <= self.r]**2 + yy[i][xx[i]**2 + yy[i]**2 <= self.r]**2))

        return c










