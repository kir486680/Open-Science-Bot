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
PT = [[(90.0*180.0)*np.pi,(90.0*180.0)*np.pi,0,a1+d1], 
[(90.0*180.0)*np.pi,-(90.0*180.0)*np.pi,0,a2+d2], 
[0,0,0,a3+d3]] # DH value table for 3 joints

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

H2_3 = [[np.cos(PT[0][0]),-np.sin(PT[0][0]) * np.cos(PT[0][1]),np.sin(PT[0][0]) * np.sin(PT[0][1]), PT[0][2]*np.cos(PT[0][0])],
        [np.sin(PT[0][0]), np.cos(PT[0][0]) * np.cos(PT[0][1]), -np.cos(PT[0][0]) * np.sin(PT[0][1]), PT[0][2] *np.sin(PT[0][0])],
        [0, np.sin(PT[0][1]), np.cos(PT[0][1]),  PT[0][3]],
        [0,0,0,1],
] #DH homogenious matrix

print(np.matrix(H0_1))



