![image-20210202210427481](https://file-1252803298.cos.ap-guangzhou.myqcloud.com/2021-02-02-130429.png)

骚味打一下码。

shumei java层做了很多混淆，可以通过老版本去突破，或者用jeb，jeb会自动解密。但是类名混淆就不会了。还是看的头疼。从代码来看就是这里

```java
        label_48:
            String v12_1 = com.ishumei.O000O0000OOoO.O00O0000OooO.O000O0000OOoO(v11 + arg10 + v12 + SmAntiFraud.O0000O000000oO.getOrganization() + "sm_tn");
            v6.put("tn", Base64.encodeToString(com.ishumei.O000O0000OOoO.O000O0000OOoO.O0000O000000oO(SmAntiFraud.O0000O000000oO.getPublicKey(), v12_1.getBytes()), 2));
        }
        catch(Throwable unused_ex) {
        }

        try {
            boolean v12_2 = com.ishumei.O000O0000OOoO.O000O0000OoO.O0000O000000oO(v5_1);
            if(v12_2) {
                v6.put("fingerprint", arg10);
            }
            else {
                v6.put("fingerprint", v5_1);
                if(v1 != 0) {
                    v6.put("fpEncode", Integer.valueOf(11));
                    v6.put("pri", v4);
                }
            }

            v6.put("sessionId", v11);
            HashMap v10 = new HashMap();
            v10.put("organization", SmAntiFraud.O0000O000000oO.getOrganization());
            v10.put("data", v6);
            v10.put("channel", SmAntiFraud.O0000O000000oO.getChannel());
            v10.put("encrypt", Integer.valueOf(1));
            return com.ishumei.O000O0000OOoO.O00O0000OooO.O0000O000000oO(v10).toString();
        }
        catch(Exception unused_ex) {
            return "";
        
```

只需要确定pri，fingerprint，tn这三个参数就行