#### ### 查看当前activity

`adb shell dumpsys activity activities | sed -En -e '/Running activities/,/Run #0/p'`