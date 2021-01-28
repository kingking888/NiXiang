function showStacks() {
    Java.perform(function() {
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
    });
}


function hook() {
    Java.perform(function () {
        const commonPaths = [
            "/data/local/bin/su",
            "/data/local/su",
            "/data/local/xbin/su",
            "/dev/com.koushikdutta.superuser.daemon/",
            "/sbin/su",
            "/system/app/Superuser.apk",
            "/system/bin/failsafe/su",
            "/system/bin/su",
            "/system/etc/init.d/99SuperSUDaemon",
            "/system/sd/xbin/su",
            "/system/xbin/busybox",
            "/system/xbin/daemonsu",
            "/system/xbin/su",
        ];

        var JavaString = Java.use("java.lang.String");
        JavaString.contains.implementation = function (name) {
            if (name !== "test-keys") {
                var ret = this.contains(name);
                console.log("JavaString",name,ret);
            }
            else{
                var ret = this.contains(name);
                return false
            }
            return ret
        };

        var JavaRuntime = Java.use("java.lang.Runtime");
        var iOException = Java.use("java.io.IOException");
        JavaRuntime.exec.overload("java.lang.String").implementation = function (command) {
            if (command.endsWith("su")) {
                ret = this.exec(command);
                console.log("JavaRuntime" ,command,ret)
                throw iOException.$new("Hacker");
            }
            else {
                var ret = this.exec(command);
                console.log("JavaRuntime2" ,command,ret)
            }
            return ret;
        }

        var JavaFile = Java.use("java.io.File");
        JavaFile.exists.implementation = function () {
            const filename = this.getAbsolutePath();
            if (commonPaths.indexOf(filename) >= 0) {
                var ret = this.exists();
                console.log("JavaFile",filename,ret)
                return false
            }
            else {
                var ret = this.exists();
            }

            return ret;

        }
    })
};

setImmediate(function () {
    setTimeout(hook, 0);
})