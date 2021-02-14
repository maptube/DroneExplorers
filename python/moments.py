"""
>Moments
By Richard Milton
7/12/94
Python conversion 12/1/2021
"""

#globals to be calculated
mass=0
Ixx=0
Iyy=0
Izz=0
Izx=0

#def Cylinder(MinX,MaxX,CY,CZ,R,Density):
#   FORx=MinX TO MaxX STEPSize:FORy=CY-R TO CY+R STEPSize:FORz=CZ-R TO CZ+R STEPSize
#   IF ((CY-y)^2+(CZ-z)^2)<R^2 THEN Ixx+=Density*(y^2+z^2):Iyy+=Density*(x^2+z^2):Izz+=Density*(x^2+y^2)
#   NEXT:NEXT:NEXT
#end def

# cuboid calculate moments of inertia for cuboid shape
#
# @param X1 minimum x coordinate of the cuboid
# @param Y1 minimum y coordinate of the cuboid
# @param Z1 minimum z coordinate of the cuboid
# @param X2 maximum x coordinate of the cuboid
# @param Y2 maximum y coordinate of the cuboid
# @param Z2 maximum z coordinate of the cuboid
# @param cuboidMass the total mass of the cuboid, used to calculate density
# @POST updates globals mass, Ixx, Iyy, Izz, Izx
def cuboid(X1,Y1,Z1,X2,Y2,Z2,cuboidMass):
   global mass, Ixx, Iyy, Izz, Izx
   volume = abs((X2-X1)*(Y2-Y1)*(Z2-Z1))
   density = cuboidMass / volume
   mass+=cuboidMass # increment total mass so we can see how much we've accounted for overall
   # FORx=X1 TO X2 STEPSize:FORy=Y1 TO Y2 STEPSize:FORz=Z1 TO Z2 STEPSize
   # Ixx+=Density*(y^2+z^2):Iyy+=Density*(x^2+z^2):Izz+=Density*(x^2+y^2):Izx+=Density*x*z
   # NEXT:NEXT:NEXT:ENDPROC
   X1P2 = pow(X1,2)
   Y1P2 = pow(Y1,2)
   Z1P2 = pow(Z1,2)
   #X1P3 = pow(X1,3)
   Y1P3 = pow(Y1,3)
   Z1P3 = pow(Z1,3)
   X2P2 = pow(X2,2)
   Y2P2 = pow(Y2,2)
   Z2P2 = pow(Z2,2)
   #X2P3 = pow(X2,3)
   Y2P3 = pow(Y2,3)
   Z2P3 = pow(Z2,3)
   Ixx+=density*(X2-X1)*(Y2*(Y2P2*(Z2-Z1)+Z2P3-Z1P3)+Y1*(Y1P2*(Z1-Z2)+Z1P3-Z2P3))/3
   Iyy+=density*(Y2-Y1)*(X2*(X2P2*(Z2-Z1)+Z2P3-Z1P3)+X1*(X1P2*(Z1-Z2)+Z1P3-Z2P3))/3
   Izz+=density*(Z2-Z1)*(X2*(X2P2*(Y2-Y1)+Y2P3-Y1P3)+X1*(X1P2*(Y1-Y2)+Y1P3-Y2P3))/3
   Izx+=density*(Y2-Y1)*(X2P2*(Z2P2-Z1P2)+X1P2*(Z1P2-Z2P2))/4
#end def

################################################################################
#Contents of this section required to be input for each aircraft

realMass=0.4 #required for calculation of how much mass has been accounted for

#Required for normalisation
#b=0.81 #wing span
#cbar=0.155 #mean chord

#some useful masses of objects
mass_EmaxMT1806 = 18.0/1000.0
mass_LiPo3S1300 = 100.0/1000.0

#start calculating bits
cuboid(  -0.1,  -0.1, -0.012, -0.078, -0.078, 0.0, mass_EmaxMT1806) #motor1 back left
cuboid( 0.078,  -0.1, -0.012,  0.1,   -0.078, 0.0, mass_EmaxMT1806) #motor2 front left
cuboid( 0.078, 0.078, -0.012,  0.1,      0.1, 0.0, mass_EmaxMT1806) #motor3 front right
cuboid(  -0.1, 0.078, -0.012, -0.078,    0.1, 0.0, mass_EmaxMT1806) #motor4 rear right
cuboid(-0.04,-0.02,0.01, 0.04,0.02,0.04, mass_LiPo3S1300) #pack
#cuboid(-0.01,-0.035,-0.035,0.07,0.035,0.035,WingDens) #frame
#4xESC
#Flip32
#Taranis Rx

#now print out the results
print('Mass accounted for '+str(mass)+' Kg')
print('Real mass is '+str(realMass)+' Kg')
print('Ixx='+str(Ixx))
print('Iyy='+str(Iyy))
print('Izz='+str(Izz))
print('Izx='+str(Izx))
#these are normalisation calculations if needed
#print('ixx='+str(Ixx/(RealMass*b^2))
#print('iyy='+str(Iyy/(RealMass*cbar^2))
#print('izz='+str(Izz/(RealMass*b^2))
#print('izx='+str(Izx/(RealMass*b^2))

