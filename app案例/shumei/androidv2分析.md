### 抓包hook分析

![image-20210209160606651](/Users/chion/Desktop/NiXiang/app案例/shumei/androidv2分析.assets/image-20210209160606651.png)

首先hook一遍native函数

```javascript

Java.perform(function () {
    var so_class = Java.use("com.ishumei.dfp.SMSDK");
    so_class.x1.implementation = function (a,b){
        console.log("---x1----");
        console.log("---x1--a----",a);
        console.log("---x1--b----",b);
        
        var res = this.x1(a,b);
        console.log("结果---x1----",res);

        console.log("---x1 end----");
        return res;
        
    };
    so_class.x2.implementation = function (a,b){
        console.log("---x2----");
        console.log("---x2--a----",a);
        console.log("---x2--b----",b);
        var res = this.x2(a,b);
        console.log("结果---x2----",res);

        console.log("---x2 end----");
        return res;
        
    };
    so_class.y1.overload("boolean").implementation = function (a){
        console.log("---y1----");
        var res = this.y1(a);
        console.log("结果---y1----",res);

        console.log("---y1 end----");
        return res;
        
    };
    so_class.y2.implementation = function (a,b,c){
        console.log("---y2----");
        console.log("---y2--a----",a);
        console.log("---y2--b----",b);
        console.log("---y2--c----",c);
        var res = this.y2(a,b,c);
        console.log("结果---y2----",res);

        console.log("---y2 end----");
        return res;
        
    };
    so_class.z1.implementation = function (a){
        console.log("---z1----");
        var res = this.z1(a);
        console.log("结果---z1----",res);

        console.log("---z1 end----");

        return res;
        
    };
    so_class.z2.implementation = function (a){
        console.log("---z2----");
        var res = this.z2(a);
        console.log("结果---z2----",res);

        console.log("---z2 end----");
        return res;
        
    };
    so_class.z3.implementation = function (a){
        console.log("---z3----");
        console.log("---z3--a----",a);
        var res = this.z3(a);
        console.log("结果---z3----",res);
        console.log("---z3 end----");
        return res;
        
    };
});
```

X1 就是fingerprint。通过java层分析可以得出pri是一层rsa的加密，这个直接扣代码就行。

private native String x1(String str, String str2); 

![image-20210209161148035](/Users/chion/Desktop/NiXiang/app案例/shumei/androidv2分析.assets/image-20210209161148035.png)

str应该是一个随机密钥，str2就是一些指纹加密之后的信息了。

ainfo 就是一些检测点了

![image-20210209161811585](/Users/chion/Desktop/NiXiang/app案例/shumei/androidv2分析.assets/image-20210209161811585.png)

检测了xposed，root等各种框架

Y2 的作用就是把这些信息加密给ainfo

![image-20210209162009330](/Users/chion/Desktop/NiXiang/app案例/shumei/androidv2分析.assets/image-20210209162009330.png)

然后在是x1的检测，检测有很多，100多个。这是其中一个，root被看的一览无余。。

```python
"riskapp":{
        "com.topjohnwu.magisk":1,
        "magisk":1,
        "de.robv.android.xposed.installer":1,
        "xposed":1
    },
```

这是一些加密层的分析，通过简单的hook就大概知道是什么位置，做了什么，接下来进入正题，首先要从java层入手，这个版本没有混淆，shield算法都是老的，这个我会日后分享思路。很简单的。。。。应该没有版本限制，所以这个版本还是能用就是不知道风控是不是根据版本来判断的。

### java层分析。

