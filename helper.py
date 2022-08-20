import numpy as np

a1 = 1
a2 = 1
a3 = 1
d1 = 0
d2 = 0
d3 = 0

#Roation + translation calculating matrix

R0_1 = [[0,0,1],[1,0,0],[0,-1,0]]
R1_2 = [[0,0,-1],[1,0,0],[0,-1,0]]
R2_3 = [[1,0,0],[0,1,0],[0,0,1]]

d0_1 = [[0], [0],[a1+d1]]
d1_2 = [[0], [0],[a2+d2]]
d2_3 = [[0], [0],[a3+d3]]

H0_1 = np.concatenate((R0_1, d0_1),1)
H0_1 = np.concatenate((H0_1, [[0,0,0,1]]))
H1_2 = np.concatenate((R1_2, d1_2),1)
H1_2 = np.concatenate((H1_2, [[0,0,0,1]]))
H2_3 = np.concatenate((R2_3, d2_3),1)
H2_3 = np.concatenate((H2_3, [[0,0,0,1]]))

H0_2 = np.dot(H0_1,H1_2)
H0_3 = np.dot(H0_2, H2_3)
print(H0_3)

#DH way of calculating homogenious matrix
PT = [[-(90.0*180.0)*np.pi,-(90.0*180.0)*np.pi,0,a1+d1], 
[(90.0*180.0)*np.pi,-(90.0*180.0)*np.pi,0,a2+d2], 
[0,0,0,a3+d3]] # DH value table for 3 joints

#for i in range(1,3):

H0_1 = [[np.cos(PT[0][0]),-np.sin(PT[0][0]) * np.cos(PT[0][1]),np.sin(PT[0][0]) * np.sin(PT[0][1]), PT[0][2]*np.cos(PT[0][0])],
        [np.sin(PT[0][0]), np.cos(PT[0][0]) * np.cos(PT[0][1]), -np.cos(PT[0][0]) * np.sin(PT[0][1]), PT[0][2] *np.sin(PT[0][0])],
        [0, np.sin(PT[0][1]), np.cos(PT[0][1]),  PT[0][3]],
        [0,0,0,1],
] #DH homogenious matrix

i=1
H1_2 = [[np.cos(PT[i][0]),-np.sin(PT[i][0]) * np.cos(PT[i][1]),np.sin(PT[i][0]) * np.sin(PT[i][1]), PT[i][2]*np.cos(PT[0][0])],
        [np.sin(PT[i][0]), np.cos(PT[i][0]) * np.cos(PT[i][1]), -np.cos(PT[i][0]) * np.sin(PT[i][1]), PT[0][2] *np.sin(PT[i][0])],
        [0, np.sin(PT[0][1]), np.cos(PT[i][1]),  PT[i][3]],
        [0,0,0,1],
] #DH homogenious matrix
H0_2 = np.dot(H0_1,H1_2)
i=2


H2_3 = [[np.cos(PT[0][0]),-np.sin(PT[0][0]) * np.cos(PT[0][1]),np.sin(PT[0][0]) * np.sin(PT[0][1]), PT[0][2]*np.cos(PT[0][0])],
        [np.sin(PT[0][0]), np.cos(PT[0][0]) * np.cos(PT[0][1]), -np.cos(PT[0][0]) * np.sin(PT[0][1]), PT[0][2] *np.sin(PT[0][0])],
        [0, np.sin(PT[0][1]), np.cos(PT[0][1]),  PT[0][3]],
        [0,0,0,1],
] #DH homogenious matrix

H0_3 = np.dot(H0_2, H2_3)


#DH way of calculating homogenious matrix

d_h_table = np.array([[np.deg2rad(90), np.deg2rad(-90), 0, a1 + d1],
                      [np.deg2rad(90), np.deg2rad(-90), 0, a2 + d2],
                      [0, 0, 0, a3 + d3]]) 
homgen_0_1 = np.array([[np.cos(d_h_table[0,0]), -np.sin(d_h_table[0,0]) * np.cos(d_h_table[0,1]), np.sin(d_h_table[0,0]) * np.sin(d_h_table[0,1]), d_h_table[0,2] * np.cos(d_h_table[0,0])],
                      [np.sin(d_h_table[0,0]), np.cos(d_h_table[0,0]) * np.cos(d_h_table[0,1]), -np.cos(d_h_table[0,0]) * np.sin(d_h_table[0,1]), d_h_table[0,2] * np.sin(d_h_table[0,0])],
                      [0, np.sin(d_h_table[0,1]), np.cos(d_h_table[0,1]), d_h_table[0,3]],
                      [0, 0, 0, 1]])  
i = 1
homgen_1_2 = np.array([[np.cos(d_h_table[i,0]), -np.sin(d_h_table[i,0]) * np.cos(d_h_table[i,1]), np.sin(d_h_table[i,0]) * np.sin(d_h_table[i,1]), d_h_table[i,2] * np.cos(d_h_table[i,0])],
                      [np.sin(d_h_table[i,0]), np.cos(d_h_table[i,0]) * np.cos(d_h_table[i,1]), -np.cos(d_h_table[i,0]) * np.sin(d_h_table[i,1]), d_h_table[i,2] * np.sin(d_h_table[i,0])],
                      [0, np.sin(d_h_table[i,1]), np.cos(d_h_table[i,1]), d_h_table[i,3]],
                      [0, 0, 0, 1]])  
 
# Homogeneous transformation matrix from frame 2 to frame 3
i = 2
homgen_2_3 = np.array([[np.cos(d_h_table[i,0]), -np.sin(d_h_table[i,0]) * np.cos(d_h_table[i,1]), np.sin(d_h_table[i,0]) * np.sin(d_h_table[i,1]), d_h_table[i,2] * np.cos(d_h_table[i,0])],
                      [np.sin(d_h_table[i,0]), np.cos(d_h_table[i,0]) * np.cos(d_h_table[i,1]), -np.cos(d_h_table[i,0]) * np.sin(d_h_table[i,1]), d_h_table[i,2] * np.sin(d_h_table[i,0])],
                      [0, np.sin(d_h_table[i,1]), np.cos(d_h_table[i,1]), d_h_table[i,3]],
                      [0, 0, 0, 1]])  
 
homgen_0_3 = homgen_0_1 @ homgen_1_2 @ homgen_2_3
print(homgen_0_3)


#Jacobian Matrix

Jinv = np.array([[0,0,1], [1,0,0], [0,-1,0]])

desiredCoord = np.array([[4],[3],[2]])
res = Jinv @ desiredCoord
print(res)
print(np.dot(Jinv, desiredCoord))

#gear diameter is 4.2
def rotationsToDistance(rotations, diameter):
    return np.pi*diameter
def degreesToDistance(degrees, diameter):
    distancePerDegree = np.pi * diameter / 360
    return distancePerDegree * degrees

