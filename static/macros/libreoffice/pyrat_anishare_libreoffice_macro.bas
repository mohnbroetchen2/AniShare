
Sub PyRatAniShare
rem ----------------------------------------------------------------------
rem define variables
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
myRange = oSheet.getCellRangeByName( "A:A" )
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
args17(0).Value = "$C$2:$C$"+TotalCount

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args17())

rem ----------------------------------------------------------------------
dim args18(0) as new com.sun.star.beans.PropertyValue
args18(0).Name = "NumberFormatValue"
args18(0).Value = 84

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
args29(0).Value = "mouse"

i=1
Do	
	dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args29())
	
	dispatcher.executeDispatch(document, ".uno:JumpToNextCell", "", 0, Array())
	i=i+1
Loop Until i >= TotalCount	

End Sub

REM  *****  BASIC  *****

REM  *****  BASIC  *****

Sub PyRatAniShareOrgan
rem ----------------------------------------------------------------------
rem define variables
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
myRange = oSheet.getCellRangeByName( "A:A" )
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

args5(0).Value = "Organ used"
dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args5())



rem ----------------------------------------------------------------------
dim args8(1) as new com.sun.star.beans.PropertyValue
args8(0).Name = "By"
args8(0).Value = 1
args8(1).Name = "Sel"
args8(1).Value = false

dispatcher.executeDispatch(document, ".uno:GoRight", "", 0, args8())

rem ----------------------------------------------------------------------

dim args7(0) as new com.sun.star.beans.PropertyValue
args7(0).Name = "StringName"
args7(0).Value = "Euthanasia performed by"

dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args7())

rem ----------------------------------------------------------------------
dispatcher.executeDispatch(document, ".uno:GoRight", "", 0, args8())

rem ----------------------------------------------------------------------
dim args9(0) as new com.sun.star.beans.PropertyValue
args9(0).Name = "StringName"
args9(0).Value = "Comment"

dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args9())

rem ----------------------------------------------------------------------

SearchFieldSacrificedate

dim args18(0) as new com.sun.star.beans.PropertyValue
args18(0).Name = "NumberFormatValue"
args18(0).Value = 84

dim i as integer
i=1
dim args11(0) as new com.sun.star.beans.PropertyValue
	args11(0).Name = "StringName"
rem	args11(0).Value = "=TODAY()+14"
	args11(0).Value = TDate
Do
	rem ----------------------------------------------------------------------
	
	
	dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args11())
	dispatcher.executeDispatch(document, ".uno:NumberFormatValue", "", 0, args18())
	rem ----------------------------------------------------------------------
	dispatcher.executeDispatch(document, ".uno:JumpToNextCell", "", 0, Array())

	i=i+1
Loop Until i >= TotalCount	


dim args28(0) as new com.sun.star.beans.PropertyValue
args28(0).Name = "ToPoint"
args28(0).Value = "$A$2"

dispatcher.executeDispatch(document, ".uno:GoToCell", "", 0, args28())

dim args29(0) as new com.sun.star.beans.PropertyValue
args29(0).Name = "StringName"
args29(0).Value = "mouse"

i=1
Do	
	dispatcher.executeDispatch(document, ".uno:EnterString", "", 0, args29())
	
	dispatcher.executeDispatch(document, ".uno:JumpToNextCell", "", 0, Array())
	i=i+1
Loop Until i >= TotalCount	

End Sub


sub SearchFieldSacrificedate
rem ----------------------------------------------------------------------
rem define variables
dim document   as object
dim dispatcher as object
rem ----------------------------------------------------------------------
rem get access to the document
document   = ThisComponent.CurrentController.Frame
dispatcher = createUnoService("com.sun.star.frame.DispatchHelper")

rem ----------------------------------------------------------------------
dim args1(20) as new com.sun.star.beans.PropertyValue
args1(0).Name = "SearchItem.StyleFamily"
args1(0).Value = 2
args1(1).Name = "SearchItem.CellType"
args1(1).Value = 0
args1(2).Name = "SearchItem.RowDirection"
args1(2).Value = true
args1(3).Name = "SearchItem.AllTables"
args1(3).Value = false
args1(4).Name = "SearchItem.SearchFiltered"
args1(4).Value = false
args1(5).Name = "SearchItem.Backward"
args1(5).Value = false
args1(6).Name = "SearchItem.Pattern"
args1(6).Value = false
args1(7).Name = "SearchItem.Content"
args1(7).Value = false
args1(8).Name = "SearchItem.AsianOptions"
args1(8).Value = false
args1(9).Name = "SearchItem.AlgorithmType"
args1(9).Value = 0
args1(10).Name = "SearchItem.SearchFlags"
args1(10).Value = 0
args1(11).Name = "SearchItem.SearchString"
args1(11).Value = "sacrifice date"
args1(12).Name = "SearchItem.ReplaceString"
args1(12).Value = ""
args1(13).Name = "SearchItem.Locale"
args1(13).Value = 255
args1(14).Name = "SearchItem.ChangedChars"
args1(14).Value = 2
args1(15).Name = "SearchItem.DeletedChars"
args1(15).Value = 2
args1(16).Name = "SearchItem.InsertedChars"
args1(16).Value = 2
args1(17).Name = "SearchItem.TransliterateFlags"
args1(17).Value = 256
args1(18).Name = "SearchItem.Command"
args1(18).Value = 0
args1(19).Name = "SearchItem.SearchFormatted"
args1(19).Value = false
args1(20).Name = "SearchItem.AlgorithmType2"
args1(20).Value = 1

dispatcher.executeDispatch(document, ".uno:ExecuteSearch", "", 0, args1())

rem ----------------------------------------------------------------------
dim args4(1) as new com.sun.star.beans.PropertyValue
args4(0).Name = "By"
args4(0).Value = 1
args4(1).Name = "Sel"
args4(1).Value = false

dispatcher.executeDispatch(document, ".uno:GoDown", "", 0, args4())


end sub
