### 判断有没有壳

先找出二进制文件：otool -l /Users/chion/Downloads/i4ToolsDownloads/App/Payload/discover |grep crypt

```objective-c
     cryptoff 16384
    cryptsize 90980352
      cryptid 1
```

Cryptic =1 就是加壳了。



使用frida-ios-dump砸壳，这个github上搜索就可以了。然后用class-dump反汇编

我的class-dump是官网下载的，在使用class-dump -H报错Error:Cannot find offset for address 0xd80000000101534a in stringAtAddress:由于我项目使用了Swift和Oc混编，猜测可能是官网的class-dump不支持dump swift files导致。

##### 解决办法：

从链接[https://github.com/AloneMonkey/MonkeyDev/blob/master/bin/class-dump](https://links.jianshu.com/go?to=https%3A%2F%2Fgithub.com%2FAloneMonkey%2FMonkeyDev%2Fblob%2Fmaster%2Fbin%2Fclass-dump)中重新下载class-dump拖入到路径：**/usr/local/bin**

若执行class-dump命令报错`/usr/local/bin/class-dump: Permission denied`，在终端运行`sudo chmod 777 /usr/local/bin/class-dump`命令赋予所有用户可读可写可执行class-dump文件权限

最后运行class-dump即可。



作者：Simple_Code
链接：https://www.jianshu.com/p/32818f9dc255
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。