引用 https://blog.csdn.net/carson_ho/article/details/78179340

###  Rxjava原理介绍

- `Rxjava`原理 基于 **一种扩展的观察者模式**
- `Rxjava`的扩展观察者模式中有4个角色：

| 角色                   | 作用                         | 类比   |
| ---------------------- | ---------------------------- | ------ |
| 被观察者（Observable） | 产生事件                     | 顾客   |
| 观察者（Observer）     | 接收事件，并给出响应动作     | 厨房   |
| 订阅（Subscribe）      | 连接 被观察者 & 观察者       | 服务员 |
| 事件（Event）          | 被观察者 & 观察者 沟通的载体 | 菜式   |

- 具体原理

请结合上述 **顾客到饭店吃饭** 的生活例子理解：

![](https://imgconvert.csdnimg.cn/aHR0cDovL3VwbG9hZC1pbWFnZXMuamlhbnNodS5pby91cGxvYWRfaW1hZ2VzLzk0NDM2NS01YjZlN2M4YTNiYjU1ZjM5LnBuZz9pbWFnZU1vZ3IyL2F1dG8tb3JpZW50L3N0cmlwJTdDaW1hZ2VWaWV3Mi8yL3cvMTI0MA)

![](https://imgconvert.csdnimg.cn/aHR0cDovL3VwbG9hZC1pbWFnZXMuamlhbnNodS5pby91cGxvYWRfaW1hZ2VzLzk0NDM2NS1mYzNiN2ViNWEwYWQyOGQwLnBuZz9pbWFnZU1vZ3IyL2F1dG8tb3JpZW50L3N0cmlwJTdDaW1hZ2VWaWV3Mi8yL3cvMTI0MA)

即`RxJava`原理可总结为：被观察者 `（Observable）` 通过 订阅`（Subscribe）` **按顺序发送事件** 给观察者 `（Observer）`， 观察者`（Observer）` **按顺序接收事件** & 作出对应的响应动作。具体如下图：

![](https://imgconvert.csdnimg.cn/aHR0cDovL3VwbG9hZC1pbWFnZXMuamlhbnNodS5pby91cGxvYWRfaW1hZ2VzLzk0NDM2NS05OGVjOTJkZjBhNGQ3ZTBiLnBuZz9pbWFnZU1vZ3IyL2F1dG8tb3JpZW50L3N0cmlwJTdDaW1hZ2VWaWV3Mi8yL3cvMTI0MA)

