REM  *****  BASIC  ****

Sub TickAtLab_AniShare
rem ----------------------------------------------------------------------
rem define variables
dim document   as object
dim dispatcher as object
dim oSheet as object
Dim FDate As String
Dim TDate As String

FDate = Date
TDate = Date + 14
rem ----------------------------------------------------------------------
rem get access to the document
document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

dim oFunction as variant
oFunction = createUnoService("com.sun.star.sheet.FunctionAccess")
oSheet = ThisComponent.getCurrentController().getActiveSheet()
myRange = oSheet.getCellRangeByName( "A:A" )
dim aArgument(1) as variant
aArgument(0)=myRange
aArgument(1)="<>"
TotalCount = oFunction.callFunction( "COUNTIFS", aArgument() )

rem ----------------------------------------------------------------------
dim args2(0) as new com.sun.star.beans.PropertyValue
args2(0).Name = "ToPoint"
args2(0).Value = "$A$1"

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args2())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args2())

rem ----------------------------------------------------------------------
dim args3(0) as new com.sun.star.beans.PropertyValue
args3(0).Name = "StringName"
args3(0).Value = "Comment"

dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args3())

rem ----------------------------------------------------------------------
dim args4(0) as new com.sun.star.beans.PropertyValue
args4(0).Name = "ToPoint"
args4(0).Value = "$B$1"

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args4())

rem ----------------------------------------------------------------------
dim args5(0) as new com.sun.star.beans.PropertyValue
args5(0).Name = "StringName"
args5(0).Value = "Sex"

dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args5())

rem ----------------------------------------------------------------------
dim args6(0) as new com.sun.star.beans.PropertyValue
args6(0).Name = "ToPoint"
args6(0).Value = "$C$1"

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args6())

rem ----------------------------------------------------------------------
dim args7(0) as new com.sun.star.beans.PropertyValue
args7(0).Name = "StringName"
args7(0).Value = "Line / Strain (Name)"

dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args7())

args6(0).Value = "$D$1"

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args6())

rem ----------------------------------------------------------------------
dim args8(0) as new com.sun.star.beans.PropertyValue
args8(0).Name = "StringName"
args8(0).Value = "ID"

dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args8())

rem ----------------------------------------------------------------------

args6(0).Value = "$E$1"

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args6())

dim args9(0) as new com.sun.star.beans.PropertyValue
args9(0).Name = "StringName"
args9(0).Value = "DOB"

dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args9())

args6(0).Value = "$F$1"
dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args6())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args6())

rem ----------------------------------------------------------------------
dim args11(0) as new com.sun.star.beans.PropertyValue
args11(0).Name = "StringName"
args11(0).Value = "Amount"

dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args11())

rem ----------------------------------------------------------------------
args6(0).Value = "$G$1"
dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args6())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
rem ----------------------------------------------------------------------

rem ----------------------------------------------------------------------
dim args14(0) as new com.sun.star.beans.PropertyValue
args14(0).Name = "ToPoint"
args14(0).Value = "$G$1"

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args14())

rem ----------------------------------------------------------------------
dim args15(0) as new com.sun.star.beans.PropertyValue
args15(0).Name = "StringName"
args15(0).Value = "License Number"

dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args15())

rem ----------------------------------------------------------------------
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())

rem ----------------------------------------------------------------------
dim args17(0) as new com.sun.star.beans.PropertyValue
args17(0).Name = "ToPoint"
args17(0).Value = "$H$1"

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args17())

rem ----------------------------------------------------------------------
dim args18(0) as new com.sun.star.beans.PropertyValue
args18(0).Name = "StringName"
args18(0).Value = "Building"

dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args18())

rem ----------------------------------------------------------------------
args6(0).Value = "$I$1"
dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args6())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())
args6(0).Value = "$J$1"
dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args6())
dispatcher.executeDispatch(document, ".uno:DeleteColumns", "", 0, Array())

args6(0).Value = "$I$2"
dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args6())

i=1
Do	
	responsibleuser
	i=i+1
Loop Until i >= TotalCount	

addfields

end sub

Sub responsibleuser()
    Dim respUser As String
    dim document   as object
	dim dispatcher as object
	dim oSheet as object
    
    Dim user As String
    dim args3(0) as new com.sun.star.beans.PropertyValue
	args3(0).Name = "StringName"
	document   = ThisComponent.CurrentController.Frame
	dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")
	
    user = thisComponent.getCurrentSelection().getString()
    respUser = Right(user, Len(user) - InStr(user, ",") - 1) + " " + Left(user, InStr(user, ",") - 1)
    args3(0).Value = respUser
    dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args3())
	dispatcher.executeDispatch(document, ".uno:JumpToNextCell", "", 0, Array())
End Sub

Sub addfields()
dim document   as object
dim dispatcher as object
dim oSheet as object
Dim FDate As String
Dim TDate As String
rem ----------------------------------------------------------------------
rem get access to the document

FDate = Date
TDate = Date + 14

document   = ThisComponent.CurrentController.Frame
dim oFunction as variant
oFunction = createUnoService("com.sun.star.sheet.FunctionAccess")
oSheet = ThisComponent.getCurrentController().getActiveSheet()
myRange = oSheet.getCellRangeByName( "B:B" )
dim aArgument(1) as variant
aArgument(0)=myRange
aArgument(1)="<>"
TotalCount = oFunction.callFunction( "COUNTIFS", aArgument() )
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

dim args2(0) as new com.sun.star.beans.PropertyValue
args2(0).Name = "ToPoint"
args2(0).Value = "$A$1"

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args2())

rem ----------------------------------------------------------------------
dispatcher.executeDispatch(document, ".uno:InsertColumnsBefore", "", 0, Array())

rem ----------------------------------------------------------------------
dispatcher.executeDispatch(document, ".uno:InsertColumnsBefore", "", 0, Array())

rem ----------------------------------------------------------------------
dispatcher.executeDispatch(document, ".uno:InsertColumnsBefore", "", 0, Array())

rem ----------------------------------------------------------------------
dim args4(0) as new com.sun.star.beans.PropertyValue
args4(0).Name = "ToPoint"
args4(0).Value = "$A$1"

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args4())

rem ----------------------------------------------------------------------
dim args5(0) as new com.sun.star.beans.PropertyValue
args5(0).Name = "StringName"
args5(0).Value = "Animal type"

dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args5())

rem ----------------------------------------------------------------------
dim args6(1) as new com.sun.star.beans.PropertyValue
args6(0).Name = "By"
args6(0).Value = 1
args6(1).Name = "Sel"
args6(1).Value = false

dispatcher.executeDispatch(document, ".uno:GoRight", "", 0, args6())

rem ----------------------------------------------------------------------
dim args7(0) as new com.sun.star.beans.PropertyValue
args7(0).Name = "StringName"
args7(0).Value = "Available from"

dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args7())

rem ----------------------------------------------------------------------
dim args8(1) as new com.sun.star.beans.PropertyValue
args8(0).Name = "By"
args8(0).Value = 1
args8(1).Name = "Sel"
args8(1).Value = false

dispatcher.executeDispatch(document, ".uno:GoRight", "", 0, args8())

rem ----------------------------------------------------------------------
dim args9(0) as new com.sun.star.beans.PropertyValue
args9(0).Name = "StringName"
args9(0).Value = "Available to"

dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args9())

rem ----------------------------------------------------------------------
dim args10(1) as new com.sun.star.beans.PropertyValue
args10(0).Name = "By"
args10(0).Value = 1
args10(1).Name = "Sel"
args10(1).Value = false

dispatcher.executeDispatch(document, ".uno:GoDown", "", 0, args10())
dim i as integer
i=1
dim args11(0) as new com.sun.star.beans.PropertyValue
	args11(0).Name = "StringName"
rem	args11(0).Value = "=TODAY()+14"
	args11(0).Value = TDate
Do
	rem ----------------------------------------------------------------------
	
	
	dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args11())
	
	rem ----------------------------------------------------------------------
	dispatcher.executeDispatch(document, ".uno:JumpToNextCell", "", 0, Array())
	i=i+1
Loop Until i >= TotalCount	


dim args15(0) as new com.sun.star.beans.PropertyValue
args15(0).Name = "ToPoint"
args15(0).Value = "$C$2"

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args15())

rem ----------------------------------------------------------------------
rem dispatcher.executeDispatch(document, ".uno:AutoFill", "", 0, Array())

rem ----------------------------------------------------------------------
dim args17(0) as new com.sun.star.beans.PropertyValue
args17(0).Name = "ToPoint"
args17(0).Value = "$H$2:$H$"+TotalCount

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args17())

rem ----------------------------------------------------------------------
dim args18(0) as new com.sun.star.beans.PropertyValue
args18(0).Name = "NumberFormatValue"
args18(0).Value = 84

dispatcher.executeDispatch(document, ".uno:NumberFormatValue", "", 0, args18())
args17(0).Value = "$C$2:$C$"+TotalCount
dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args17())
dispatcher.executeDispatch(document, ".uno:NumberFormatValue", "", 0, args18())

rem ----------------------------------------------------------------------
dim args19(0) as new com.sun.star.beans.PropertyValue
args19(0).Name = "ToPoint"
args19(0).Value = "$B$1"

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args19())

rem ----------------------------------------------------------------------
rem dispatcher.executeDispatch(document, ".uno:JumpToNextCell", "", 0, Array())

dispatcher.executeDispatch(document, ".uno:GoDown", "", 0, args10())
i=1
rem args11(0).Value = "=TODAY()"
args11(0).Value = FDate
Do	
	dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args11())
	
	dispatcher.executeDispatch(document, ".uno:JumpToNextCell", "", 0, Array())
	i=i+1
Loop Until i >= TotalCount	



dim args25(0) as new com.sun.star.beans.PropertyValue
args25(0).Name = "ToPoint"
args25(0).Value = "$B$2:$B$"+TotalCount

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args25())

rem ----------------------------------------------------------------------
dim args26(0) as new com.sun.star.beans.PropertyValue
args26(0).Name = "NumberFormatValue"
args26(0).Value = 84

dispatcher.executeDispatch(document, ".uno:NumberFormatValue", "", 0, args26())

dim args28(0) as new com.sun.star.beans.PropertyValue
args28(0).Name = "ToPoint"
args28(0).Value = "$A$2"

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args28())

dim args29(0) as new com.sun.star.beans.PropertyValue
args29(0).Name = "StringName"
args29(0).Value = "fish"

i=1
Do	
	dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args29())
	
	dispatcher.executeDispatch(document, ".uno:JumpToNextCell", "", 0, Array())
	i=i+1
Loop Until i >= TotalCount	
End Sub REM  *****  BASIC  *****
	
