仅用做学术研究



![image-20201209140056541](https://file-1252803298.cos.ap-guangzhou.myqcloud.com/2020-12-09-101255.png)

乱码，直接看源码一探究竟。

![image-20201209140243282](https://file-1252803298.cos.ap-guangzhou.myqcloud.com/2020-12-09-101301.png)

点最后一个，应该是自定义的格式

![image-20201209153615614](https://file-1252803298.cos.ap-guangzhou.myqcloud.com/2020-12-09-101307.png)

这里可以hook一下返回值，先改成json试试

![image-20201209154415871](https://file-1252803298.cos.ap-guangzhou.myqcloud.com/2020-12-09-101325.png)

进行降级处理之后，一清二楚。

上脚本

```
function headers2json(){
    Java.perform(function(){
        var h_class = Java.use("ox3");
        var c_class = Java.use("ib$a");
        h_class.a.overload("java.lang.String").implementation = function(str){
            console.log("str",str );
            return false;
        };
        c_class.c.implementation = function(){
            return 1;
        }
    })
}
```

![image-20201209173052745](https://file-1252803298.cos.ap-guangzhou.myqcloud.com/2020-12-09-101332.png)

0x4A586 就是我们需要找的so方法。generateSign


so层中：registernactive隐藏了字符串，可以用脚本打印出来，还原之后就是

```python
So Name			Java Class				Function name				Function signature	该函数SO的基址		Function偏移(IDA中可以直接跳转到这个地址)
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
libnet_crypto.so	com.izuiyou.network.NetCrypto	native_init	()V	0xc5a8c000	0x4a069
libnet_crypto.so	com.izuiyou.network.NetCrypto	encodeAES	([B)[B	0xc5a8c000	0x4a0b9
libnet_crypto.so	com.izuiyou.network.NetCrypto	decodeAES	([BZ)[B	0xc5a8c000	0x4a14d
libnet_crypto.so	com.izuiyou.network.NetCrypto	sign	(Ljava/lang/String;[B)Ljava/lang/String;	0xc5a8c000	0x4a28d
libnet_crypto.so	com.izuiyou.network.NetCrypto	getProtocolKey	()Ljava/lang/String;	0xc5a8c000	0x4a419
libnet_crypto.so	com.izuiyou.network.NetCrypto	setProtocolKey	(Ljava/lang/String;)V	0xc5a8c000	0x4a479
libnet_crypto.so	com.izuiyou.network.NetCrypto	registerDID	([B)Z	0xc5a8c000	0x4a4f5
libnet_crypto.so	com.izuiyou.network.NetCrypto	generateSign	([B)Ljava/lang/String;	0xc5a8c000	0x4a587
```

so层关键地方 这里可能顺序错了，但是直接hook就能看了。
这里看到有个关键的j_md5函数，直接hook他

```javasript
function myhexdump(name, hexdump_obj, len_obj){
    console.log("-------------------"+ name.toString()+"-------------------\n");
    console.log(hexdump(hexdump_obj,{
        length:len_obj
    }) );
    console.log("-------------------ENDEND-------------------\n")
}

function print_string(addr){
    var base_addr = Module.findBaseAddress("libnet_crypto.so");
    if(base_addr){
        console.log(base_addr.add(addr).readCString());
    }
}

function headers2json(){
    Java.perform(function(){
        var h_class = Java.use("ox3");
        var c_class = Java.use("ib$a");
        h_class.a.overload("java.lang.String").implementation = function(str){
            console.log("str",str );
            return false;
        };
        c_class.c.implementation = function(){
            return 1;
        }
    })
}

function gensign(){
    Java.perform(function(){
        // var so_addr = Module.findBaseAddress("libnet_crypto.so");
        // var pianyi_addr = so_addr.add(0x435EC+ 1);
        var pianyi_addr = Module.findExportByName("libnet_crypto.so", "MD5");

        console.log("偏移地址",pianyi_addr );
        var res = null;
        if (pianyi_addr){
            Interceptor.attach(pianyi_addr,{
                onEnter:function(args){
                    res = args[2];
                    myhexdump("arg1",args[0],1300);
                    console.log("arg2",args[1] );
                },onLeave:function(retval){
                    console.log("ret\n");
                    myhexdump("res",res,32);
                    
                }
            })
        }
    })
}
```

这里直接hook看结果
![](https://file-1252803298.cos.ap-guangzhou.myqcloud.com/2020-12-09-101338.png)

![](https://file-1252803298.cos.ap-guangzhou.myqcloud.com/2020-12-09-101345.png)

=========================================================
so具体加密

![image-20201209165947080](https://file-1252803298.cos.ap-guangzhou.myqcloud.com/2020-12-09-101352.png)

最后还原成python
![image-20201209173052745.png][1]


[1]: https://chion.xyz/usr/uploads/2020/12/832688930.png





Decodes: key:取bytes前16位

Key：7c 5a 5a 5a 5a 69 69 69 69 79 79 79 88 88 88 88