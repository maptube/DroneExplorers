"""
PID Controller.py
"""

class PIDController:
    def __init__(self,Kp,Ki,Kd):
        self.Kp=Kp #Proportional gain constant
        self.Ki=Ki #Integral gain constant
        self.Kd=Kd #Derivative gain constant
        #Imax=5.0 #max limit on I
        #SampleTime = 0.01 #seconds interval at which computation is done
        #elapsedDeltaT = 0 #time since last update
 
        self.x0 = 0 #previous input value
        self.e0 = 0 #previous error value
        self.I = 0 #Integral accumulator
        self.D = 0 #Derivative accumulator
        self.u = 0 #copy of last output value
    #end def

    ################################################################################

    """
    Run the PID calculation with a new error value and delta time from the last calculation.
    @param x Current Value
    @param y Desired Value 
    @param deltaT Time elapsed since process was last called i.e. time between e and e0
    @returns u=Kp*e + Ki*I + Kd*D
    """
    def process(self, x, y, deltaT):
        e = y - x #current error
        self.I+=e*deltaT

        self.D = (e - self.e0) / deltaT
        #dx = (x - x0) / deltaT #change in input, or dInput/dt, this is the derivative kick fix
        self.u = self.Kp * e + self.Ki * self.I + self.Kd * self.D #standard PID formula
        #u = Kp * e + Ki * I + Kd * dx; //derivative kick modification
        self.e0 = e
        self.x0 = x
        
        return self.u
    #enddef
