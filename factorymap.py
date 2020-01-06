class Map:
    def __init__(self):
        self.map = [[0 for i in range(41)] for i in range(39)]
        for i in range(10, 31):
            for j in range(2):
                self.map[j][i] = 6
                self.map[38-j][40-i] = 5
                self.map[i-1][j] = 3
                self.map[39-i][40-j] = 4
        for i in range(6,8):
            for j in range(8,19):
                self.map[i][j] = 2
                self.map[i][40-j] = 2
                self.map[i+5][j] = 2
                self.map[i+5][40-j] = 2
                self.map[i+10][j] = 2
                self.map[i+10][40-j] = 2
                self.map[i+15][j] = 2
                self.map[i+15][40-j] = 2
                self.map[i+20][j] = 2
                self.map[i+20][40-j] = 2
                self.map[i+25][j] = 2
                self.map[i+25][40-j] = 2
        for j in range(8, 19):
            self.map[8][j] = 1
            self.map[8][40 - j] = 1
            self.map[13][j] = 1
            self.map[13][40 - j] = 1
            self.map[18][j] = 1
            self.map[18][40 - j] = 1
            self.map[23][j] = 1
            self.map[23][40 - j] = 1
            self.map[28][j] = 1
            self.map[28][40 - j] = 1
            self.map[33][j] = 1
            self.map[33 ][40 - j] = 1
        for i in range(4,5):
            for j in range(5,21):
                self.map[i][j] = 1
                self.map[i][40-j] = 1
                self.map[i+5][j] = 1
                self.map[i+5][40-j] = 1
                self.map[i+10][j] = 1
                self.map[i+10][40-j] = 1
                self.map[i+15][j] = 1
                self.map[i+15][40-j] = 1
                self.map[i+20][j] = 1
                self.map[i+20][40-j] = 1
                self.map[i+25][j] = 1
                self.map[i+25][40-j] = 1
                self.map[i+30][j] = 1
                self.map[i+30][40-j] = 1
        for i in range(4,35):
            self.map[i][5] = 1
            self.map[i][20] = 1
            self.map[i][35] = 1
        for i in range(9,32,5):
            for j in range(2,5):
                self.map[i][j] = 1
                self.map[i][40-j] = 1
        for i in range(2,4):
            self.map[i][20] = 1
            self.map[38-i][20] = 1
            self.map[i][16] = 1
            self.map[38-i][16] = 1
            self.map[i][12] = 1
            self.map[38-i][12] = 1
            self.map[i][24] = 1
            self.map[38-i][24] = 1
            self.map[i][28] = 1
            self.map[38-i][28] = 1
            
