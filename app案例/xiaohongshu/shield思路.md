### 前言

仅供学术研究,不得用于违法用途

我不会提供成品，只会分享思路，不然会动了大佬们的蛋糕，🐶

**_APK_VER:6.78**_

1.老样子，抓包，有个shield参数，java层分析，直接搜索shied。无结果。

其实从678开始，有一个appid参数app_id=ECFAAF01

搞过开发都知道，这种静态资源一般都是启动就有了，所以顺藤摸瓜

![image-20210202211406288](image-20210202211406288.png)

找到了这个字眼，然后上面，有一个初始化的cost，和指纹一样。看看b函数，l.v.x0.a.b返回值。

点进去

```java
/* compiled from: Shield */
public class b {
    public static byte[] a = {115, 104, 105, 101, 108, 100};

    /* compiled from: Shield */
    public interface a {
        void loadLibrary(String str);
    }

    public static void a(Context context, String str, int i2, boolean z2, a aVar) {
        ContextHolder.sContext = context;
        ContextHolder.sDeviceId = str;
        ContextHolder.sAppId = i2;
        ContextHolder.sExperiment = z2;
        aVar.loadLibrary(a());
    }

    public static String a() {
        return new String(a);
    }
}
```

把字节转换一下就是shield.so。接下来一连串的请求都会在这个so里面完成。

>>> print([chr(i) for i in [115, 104, 105, 101, 108, 100]])
>>> ['s', 'h', 'i', 'e', 'l', 'd']