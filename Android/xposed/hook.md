### 全局hook加载

`hanldeLoadPackage(XC_loadPackage.loadPackageParam loadPackageParam)`



### Hook普通方法

```java
findAndHookMethod(clazz,  methodname, String.class, new XC_MethodHook() {
  @Override
  protected void beforeHookMethod (MethodHookParam param) throws Throwable {
    Log.d("TAG","emmmmm");
  }
  
  @Override
  protected void afterHookMethod (MethodHookParam param) throws Throwable {
    Log.d("TAG","emmmmm");
  }
})
```

### Hook静态变量

```java
  1. 先findclass 找到类
  2. xposedHelpers.setStaicIntField(clazz, "filenamed", value) claszz->对应的就是class的字节码。静态int的hook
  3. xposedHelpers.setstaicobjectField(clazz, "filenamed", value) claszz->对应的就是class的字节码。object的hook  java中string是一个对象
```

