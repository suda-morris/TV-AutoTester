; 分号开头的为注释
; 一行为一个操作，格式为：设备名 参数列表
; 设备名与参数列表间、参数间均用一个空格分隔
; 下面的操作格式[]内的为可选参数，等号后的为默认值，数字类的参数支持小数

; 延时操作格式：d 秒数
; 红外遥控器操作格式：IR 操作名 [重复次数=1]
; 电源继电器操作格式：RELAY 开关状态（ON或者OFF）
RELAY PLUG_IN
d 1
RELAY PLUG_OUT
IR POWER_ON
d 10
IR CG_PIC_MODE 2
d 1
IR CG_SOUND_MODE 3
d 1
IR CG_TIME_ZONE 2
d 1
IR CG_LANGUAGE 2
d 1
IR CG_INPUT_SOURCE 2
d 1
IR POWER_OFF
d 1