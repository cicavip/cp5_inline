checkNum = msgbox ("是否循环抓取DMO？",vbokcancel,"即将抓取...")

if checkNum=vbcancel then
	wscript.quit
end if

Set Fso = CreateObject("scripting.filesystemobject")
Pat=createobject("wscript.shell").currentdirectory
TxtDir=Pat & "\" & "DMO复制不要删除.txt"
BatDir=Pat & "\" & "dmo_copy.bat"


do while true
	if not Fso.fileexists(TxtDir) then
		Set shell=Wscript.createobject("wscript.shell")
		a=shell.run(BatDir,0)
	end if


	wscript.sleep 2000
loop