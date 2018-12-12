checkNum = msgbox ("是否发送邮件？",vbokcancel,"即将发送...")

if checkNum=vbcancel then
	wscript.quit
end if

Set Fso = CreateObject("scripting.filesystemobject")
Pat=createobject("wscript.shell").currentdirectory
TxtDir=Pat & "\" & "sendmail不要删除.txt"
BatDir=Pat & "\" & "sendmail.bat"


do while true
	if not Fso.fileexists(TxtDir) then
		Set shell=Wscript.createobject("wscript.shell")
		a=shell.run(BatDir,0)
	end if


	wscript.sleep 10000
loop