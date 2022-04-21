# CBAutoHelper
Set pathLD
Example:
ld = LDPlayer()
ld.pathLD = "D:\\LDPlayer\\LDPlayer4.0\\ldconsole.exe"
Open
ld = LDPlayer()
ld.Open("name","LDPlayer")
ld.Open("name","LDPlayer-1")
ld.Open("index","0")
ld = LDPlayer()
cmd use:
[--resolution ]
[--cpu < 1 | 2 | 3 | 4 >]
[--memory < 512 | 1024 | 2048 | 4096 | 8192 >]
[--manufacturer asus]
[--model ASUS_Z00DUO]
[--pnumber 13812345678]
[--imei ]
[--imsi ]
[--simserial ]
[--androidid ]
[--mac ]
[--autorotate < 1 | 0 >]
[--lockwindow < 1 | 0 >]
Exam:   ld.Change_Property("name", "LDPlayer", " --cpu 1 --memory 1024 --imei 123456789)
