# coding=utf-8
"""
请先看一遍原理再来看代码，本代码所有的爹都是c/c++.这些都是衍生而来的
"""
import math
def int2bin(n, count=24):
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

class MD5(object):
    # 初始化密文
    def __init__(self):
        #小红书
        # self.A = 0x10325476
        # self.B = 0x98badcfe
        # self.C = 0xefcdab89
        # self.D = 0x67452301
        #正常
        self.A = 0x67452301
        self.B = 0xefcdab89
        self.C = 0x98badcfe
        self.D = 0x10325476
        self.init_A = self.A
        self.init_B = self.B
        self.init_C = self.C
        self.init_D = self.D
        '''
        self.A = 0x01234567
        self.B = 0x89ABCDEF
        self.C = 0xFEDCBA98
        self.D = 0x76543210
         '''

        # 使用正弦函数产生的位随机数，也就是书本上的T[i]
        self.T = [int(math.floor(abs(math.sin(i + 1)) * (2 ** 32))) for i in range(64)]

        self.s = [7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
                    5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
                    4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
                    6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21]
        self.m = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
                    1,6,11,0,5,10,15,4,9,14,3,8,13,2,7,12,
                    5,8,11,14,1,4,7,10,13,0,3,6,9,12,15,2,
                    0,7,14,5,12,3,10,1,8,15,6,13,4,11,2,9]

    def encrypt(self, message:bytes):
        self.message = message
        self.ciphertext = ""
        self.fill_text()
        return self.update()

    # 附加填充位
    def fill_text(self):
        for i in range(len(self.message)):
            # c = int2bin(ord(self.message[i]), 8)
            c = int2bin(self.message[i], 8)
            self.ciphertext += c

        if (len(self.ciphertext)%512 != 448):
            if ((len(self.ciphertext)+1)%512 != 448):
                self.ciphertext += '1'
            while (len(self.ciphertext)%512 != 448):
                self.ciphertext += '0'

        length = len(self.message)*8
        if (length <= 255):
            length = int2bin(length, 8)
        else:
            length = int2bin(length, 16)
            temp = length[8:12]+length[12:16]+length[0:4]+length[4:8]
            length = temp

        self.ciphertext += length
        while (len(self.ciphertext)%512 != 0):
            self.ciphertext += '0'

    # 分组处理（迭代压缩）
    def circuit_shift(self, x, amount):
        x &= 0xFFFFFFFF
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

    def change_pos(self):
        a = self.A
        b = self.B
        c = self.C
        d = self.D
        self.A = d
        self.B = a
        self.C = b
        self.D = c

    def FF(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.F(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp)%pow(2, 32)
        self.change_pos()

    def GG(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.G(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp)%pow(2, 32)
        self.change_pos()

    def HH(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.H(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp)%pow(2, 32)
        self.change_pos()

    def II(self, mj, s, ti):
        mj = int(mj, 2)
        temp = self.I(self.B, self.C, self.D) + self.A + mj + ti
        temp = self.circuit_shift(temp, s)
        self.A = (self.B + temp)%pow(2, 32)
        self.change_pos()

    def F(self, X, Y, Z):
        return (X & Y) | ((~X) & Z)
    def G(self, X, Y, Z):
        return (X & Z) | (Y & (~Z))
    def H(self, X, Y, Z):
        return X ^ Y ^ Z
    def I(self, X, Y, Z):
        return Y ^ (X | (~Z))

    def update(self):
        M = []
        for i in range(0, 512, 32):
            num = ""
            # 获取每一段的标准十六进制形式
            for j in range(0, len(self.ciphertext[i:i+32]), 4):
                temp = self.ciphertext[i:i+32][j:j + 4]
                temp = hex(int(temp, 2))
                num += temp[2]
            # 对十六进制进行小端排序
            num_tmp = ""
            for j in range(8, 0, -2):
                temp = num[j-2:j]
                num_tmp += temp
            num = ""
            for i in range(len(num_tmp)):
                num += int2bin(int(num_tmp[i], 16), 4)
            M.append(num)

        for j in range(0, 16, 4):
            self.FF(M[self.m[j]], self.s[j], self.T[j])
            self.FF(M[self.m[j+1]], self.s[j+1], self.T[j+1])
            self.FF(M[self.m[j+2]], self.s[j+2], self.T[j+2])
            self.FF(M[self.m[j+3]], self.s[j+3], self.T[j+3])

        for j in range(0, 16, 4):
            self.GG(M[self.m[16+j]], self.s[16+j], self.T[16+j])
            self.GG(M[self.m[16+j+1]], self.s[16+j+1], self.T[16+j+1])
            self.GG(M[self.m[16+j+2]], self.s[16+j+2], self.T[16+j+2])
            self.GG(M[self.m[16+j+3]], self.s[16+j+3], self.T[16+j+3])

        for j in range(0, 16, 4):
            self.HH(M[self.m[32+j]], self.s[32+j], self.T[32+j])
            self.HH(M[self.m[32+j+1]], self.s[32+j+1], self.T[32+j+1])
            self.HH(M[self.m[32+j+2]], self.s[32+j+2], self.T[32+j+2])
            self.HH(M[self.m[32+j+3]], self.s[32+j+3], self.T[32+j+3])

        for j in range(0, 16, 4):
            self.II(M[self.m[48+j]], self.s[48+j], self.T[48+j])
            self.II(M[self.m[48+j+1]], self.s[48+j+1], self.T[48+j+1])
            self.II(M[self.m[48+j+2]], self.s[48+j+2], self.T[48+j+2])
            self.II(M[self.m[48+j+3]], self.s[48+j+3], self.T[48+j+3])
        self.A = (self.A+self.init_A)%pow(2, 32)
        self.B = (self.B+self.init_B)%pow(2, 32)
        self.C = (self.C+self.init_C)%pow(2, 32)
        self.D = (self.D+self.init_D)%pow(2, 32)
        '''
        print("A:{}".format(hex(self.A)))
        print("B:{}".format(hex(self.B)))
        print("C:{}".format(hex(self.C)))
        print("D:{}".format(hex(self.D)))
        '''
        answer = ""
        for register in [self.A, self.B, self.C, self.D]:
            register = hex(register)[2:]
            for i in range(8, 0, -2):
                answer += str(register[i-2:i])
        return answer

if __name__ == '__main__':
    MD5 = MD5()
    res = MD5.encrypt("123".encode())
    print(res)
