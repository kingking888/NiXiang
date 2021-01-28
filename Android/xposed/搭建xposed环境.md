### 导入xposed环境

1. app目录下新建 lib 目录，导入xposedbrige82api.jar

2. build.gralde 修改依赖。dependencies 

   注意！此处要用compileOnly这个修饰符！网上有些写的是provide ，现在已经停用了！）如图：

   ```java
   compileOnly 'de.robv.android.xposed:api:82'
   compileOnly 'de.robv.android.xposed:api:82:sources'
   compileOnly files(lib/api-82.jar)
   ```

   【ps:如果网络不通，或者同步不畅，就不要进行第三步的repositories { jcenter()}这个步骤了，改做这个步骤：】

   > 手动下载XposedBridgeApi-82.jar ，拖放到“项目名称/app/libs/”里面（不是网上说的单独建立lib文件夹，那是很久以前的故事了！），然后右键“Add As Library” 自行添加这个jar包。而compileOnly 'de.robv.android.xposed:api:82'和 compileOnly 'de.robv.android.xposed:api:82:sources'这两句仍然照常添加。

3. Manifest.xml 

   ``` java
   <meta-data
       android:name="xposedmodule"
       android:value="true" />
   <meta-data
       android:name="xposeddescription"
       android:value="我是一个Xposed例程" />
   <meta-data
       android:name="xposedminversion"
       android:value="53" />
   ```

   xposedmodule：value为true，表示自己是一个xposed模块
   xposeddescription：value中的文字就是对模块的描述，这些能够在手机上的Xposed框架中看到，举个栗子
   xposedminversion：xposed最低版本，这些应该都是向下兼容的吧？所以直接填最低版本好了

4. 右键点击 main ， 选择new --> Folder -->Assets Folder-->xposed_init
   这里输入 hook点。这样xposed才会去hook。

