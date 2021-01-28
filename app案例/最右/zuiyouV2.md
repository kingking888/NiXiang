### 前言

仅供学术研究,不得用于违法用途

### 思路


上篇文章讲到过，xcp协议下对应的是signv2的算法，分析java层，首先会对数据进行aes加密，再把加密的字节传进so层计算，nactive函数-》sign

写个frida主动调用，直接主动调用，自定义一下字节传进去，有利于分析。

```javascript
function call_sign() {
    Java.perform(function () {
        Java.openClassFile("/data/local/tmp/r0gson.dex").load();
        const gson = Java.use('com.r0ysue.gson.Gson');
        var NetCrypto = Java.use("com.izuiyou.network.NetCrypto");
        var string = Java.use("java.lang.String");
        var byte = string.$new("laji");
        var byte_list = byte.getBytes("UTF-8");
        NetCrypto.a("https://izuiyou.com/", byte_list);
        NetCrypto.sign.implementation = function (z, x) {
            var ff = this.sign(z, x)
            console.log(z, gson.$new().toJson(x))
            console.log("最后的返回值--->", ff)
            return ff
        }
    })
}
```

比如输入的是`laji` 返回的就是如下，v2-是一个拼接的字符串，后面的才是密文

```json
https://izuiyou.com/ [108,97,106,105]
最后的返回值---> v2-d3c1ee68387ca0133b702d39571f4af8
```

这里可以看到动态注册的地址
![image](http://note.youdao.com/yws/public/resource/cd1d25e418f478f6d64d858f9bfa6d58/31D6117E3223403488ABA35A2F707FE3?ynotemdtimestamp=1608016348301)

点进去j_sign_v2
![image](http://note.youdao.com/yws/public/resource/cd1d25e418f478f6d64d858f9bfa6d58/0348451F912D4AAAAFFC13DAD9182B55?ynotemdtimestamp=1608016348301)

一步一步跟踪
sub655dc->sub65540

![image](http://note.youdao.com/yws/public/resource/cd1d25e418f478f6d64d858f9bfa6d58/CCCEA5E72AFF4BE18B3DE36F4DA18E0F?ynotemdtimestamp=1608016348301)
这里v6，v7，v8，v9很可疑。
ida先转为16进制看看

![image](http://note.youdao.com/yws/public/resource/cd1d25e418f478f6d64d858f9bfa6d58/3C425833688E4D2BA871E79C2DB98F63?ynotemdtimestamp=1608016348301)

在结合结果，有点像md5。
![image](http://note.youdao.com/yws/public/resource/cd1d25e418f478f6d64d858f9bfa6d58/276BB31378904F37B7CEA251FC305F0A?ynotemdtimestamp=1608016348301)
在网上找了一版c的md5，果然改了一些东西，太鸡贼了。

md5算法c语言版本：https://blog.csdn.net/violet_echo_0908/article/details/51559383?utm_medium=distribute.pc_relevant_download.none-task-blog-baidujs-1.nonecase&depth_1-utm_source=distribute.pc_relevant_download.none-task-blog-baidujs-1.nonecase

然后在跟踪到sub63394，这里有一点混淆，但不影响我们看代码。
在跟到 sub63614就是一个赋位的操作，具体算法在sub_636DE
跟进去。
![image](http://note.youdao.com/yws/public/resource/cd1d25e418f478f6d64d858f9bfa6d58/26AE3017972D49FBA197525E3B602F06?ynotemdtimestamp=1608016348301)
好大一坨。
ida有插件的可以直接看出来是什么加密，这里其实就是md5加密。

然后我们hook他的a1，a2.

```java
-------------------arg1-------------------

           0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
cc02555c  01 23 55 67 89 ab cd ed fe de ba 98 76 54 32 16  .#Ug........vT2.
cc02556c  20 00 00 00 00 00 00 00 6c 61 6a 69 80 00 00 00   .......laji....
cc02557c  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
cc02558c  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
cc02559c  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
cc0255ac  20 00 00 00 00 00 00 00 4c 83 46 45 34 56 02 cc   .......L.FE4V..
cc0255bc  90 56 02 cc e8 55 02 cc fd f5 fc c2 0c 57 02 cc  .V...U.......W..
cc0255cc  4c 56 02 cc 8c 56 02 cc 90 56 02 cc e8 55 02 cc  LV...V...V...U..
-------------------ENDEND-------------------

-------------------arg3-------------------

           0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
cc025574  6c 61 6a 69 80 00 00 00 00 00 00 00 00 00 00 00  laji............
cc025584  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
cc025594  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
cc0255a4  00 00 00 00 00 00 00 00 20 00 00 00 00 00 00 00  ........ .......
cc0255b4  4c 83 46 45 34 56 02 cc 90 56 02 cc e8 55 02 cc  L.FE4V...V...U..
cc0255c4  fd f5 fc c2 0c 57 02 cc 4c 56 02 cc 8c 56 02 cc  .....W..LV...V..
cc0255d4  90 56 02 cc e8 55 02 cc 4c 83 46 45 80 ac 73 df  .V...U..L.FE..s.
cc0255e4  8c 56 02 cc 78 56 02 cc db 42 fb c2 32 35 38 37  .V..xV...B..2587
-------------------ENDEND-------------------

           0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
cc02555c  d3 c1 ee 68 38 7c a0 13 3b 70 2d 39 57 1f 4a f8  ...h8|..;p-9W.J.
cc02556c  20 00 00 00 00 00 00 00 6c 61 6a 69 80 00 00 00   .......laji....
-------------------ENDEND-------------------

https://izuiyou.com/ [108,97,106,105]
最后的返回值---> v2-d3c1ee68387ca0133b702d39571f4af8

```

看字节可以看得出，把之前的幻数以及padding复制进去了。
断定就是md5，只不过幻数变了。

不用管之后的操作了，
直接重写这个算法，验证一下
![image](http://note.youdao.com/yws/public/resource/cd1d25e418f478f6d64d858f9bfa6d58/C81C828D2431437497206C5C9DC89B49?ynotemdtimestamp=1608016348301)
对上了，多试几次，可以验证出结果是对的，那就说明sign这一块搞定了，其实还有一个encodeaes的操作，这个下篇文章在分析吧，先划水去了

在附上一个python的md5算法，已经改过了向量
https://github.com/Gengarrr/MD5_py/blob/master/MD5%E7%AE%97%E6%B3%95.py

```python
def int2bin(n, count=24):
    """returns the binary of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

class MD5(object):
    # 初始化密文
    def __init__(self, message):
        self.message = message
        self.ciphertext = ""

        self.A = 0x67552301
        self.B = 0xEDCDAB89
        self.C = 0x98BADEFE
        self.D = 0x16325476
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

        self.T = [0xD76AA478,0xE8C7B756,0x242070DB,0xC1BDCEEE,0xF57C0FAF,0x4787C62A,0xA8304613,0xFD469501,
                    0x698098D8,0x8B44F7AF,0xFFFF5BB1,0x895CD7BE,0x6B901122,0xFD987193,0xA679438E,0x49B40821,
                    0xF61E2562,0xC040B340,0x265E5A51,0xE9B6C7AA,0xD62F105D,0x02441453,0xD8A1E681,0xE7D3FBC8,
                    0x21E1CDE6,0xC33707D6,0xF4D50D87,0x455A14ED,0xA9E3E905,0xFCEFA3F8,0x676F02D9,0x8D2A4C8A,
                    0xFFFA3942,0x8771F681,0x6D9D6122,0xFDE5380C,0xA4BEEA44,0x4BDECFA9,0xF6BB4B60,0xBEBFBC70,
                    0x289B7EC6,0xEAA127FA,0xD4EF3085,0x04881D05,0xD9D4D039,0xE6DB99E5,0x1FA27CF8,0xC4AC5665,
                    0xF4292244,0x432AFF97,0xAB9423A7,0xFC93A039,0x655B59C3,0x8F0CCC92,0xFFEFF47D,0x85845DD1,
                    0x6FA87E4F,0xFE2CE6E0,0xA3014314,0x4E0811A1,0xF7537E82,0xBD3AF235,0x2AD7D2BB,0xEB86D391]
        self.s = [7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
                    5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
                    4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
                    6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21]
        self.m = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
                    1,6,11,0,5,10,15,4,9,14,3,8,13,2,7,12,
                    5,8,11,14,1,4,7,10,13,0,3,6,9,12,15,2,
                    0,7,14,5,12,3,10,1,8,15,6,13,4,11,2,9]



    # 附加填充位
    def fill_text(self):
        for i in range(len(self.message)):
            c = int2bin(ord(self.message[i]), 8)
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

    def group_processing(self):
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

        #print(M)



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





#MD5 = MD5("iscbupt")
#MD5 = MD5("Beijing University of Posts and Telecommunications")
#MD5 = MD5("njupt.information security")
message = input("输入要加密的字符串：")
MD5 = MD5(message)
MD5.fill_text()
result = MD5.group_processing()
print("32位小写MD5加密：{}".format(result))
```