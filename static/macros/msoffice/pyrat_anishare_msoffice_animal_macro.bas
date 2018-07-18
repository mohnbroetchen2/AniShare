Attribute VB_Name = "PyRatAniShare"

Sub PyRatAniShare()
Attribute PyRatAniShare.VB_ProcData.VB_Invoke_Func = " \n14"

    Dim document   As Object
    Dim dispatcher As Object
    Dim oSheet As Object
    Dim TotalCount As Integer
    Dim thisRange As String
    Dim i As Integer
    Dim FDate As String
    Dim TDate As String
    TotalCount = ActiveSheet.UsedRange.Rows.Count - 1
    thisRange = "A1:A" + CStr(TotalCount)
    
    Cells(1, 1).Select
    Range("A1").EntireColumn.Insert
    Range("A1").EntireColumn.Insert
    Range("A1").EntireColumn.Insert
'    Selection.Insert Shift:=xlToRight, CopyOrigin:=xlFormatFromLeftOrAbove
'    Selection.Insert Shift:=xlToRight, CopyOrigin:=xlFormatFromLeftOrAbove
'    Selection.Insert Shift:=xlToRight, CopyOrigin:=xlFormatFromLeftOrAbove
    ActiveCell.Select
    ActiveCell.FormulaR1C1 = "Animal type"
    ActiveCell.Offset(0, 1).Range("A1").Select
    ActiveCell.FormulaR1C1 = "Available from"
    ActiveCell.Offset(0, 1).Range("A1").Select
    ActiveCell.FormulaR1C1 = "Available to"
    ActiveCell.Offset(1, 0).Range("A1").Select
    ActiveCell.Range(thisRange).Select
    ActiveCell.Select
    TDate = Date + 14
    ActiveCell.FormulaR1C1 = TDate
    ' ActiveCell.FormulaR1C1 = "=TODAY()+14"
    ActiveCell.Select
    i = 1
    Do
        ActiveCell.Offset(1, 0).Range("A1").Select
        ActiveCell.FormulaR1C1 = TDate
        i = i + 1
    Loop Until i >= TotalCount
   ' Selection.AutoFill Destination:=ActiveCell.Range(thisRange)
   ' ActiveCell.Range(thisRange).Select
   ' ActiveCell.Offset(0, -1).Range("A1").Select
   ' ActiveCell.FormulaR1C1 = "=TODAY()"
    Cells(2, 2).Select
    FDate = Date
    ActiveCell.FormulaR1C1 = FDate
    ActiveCell.Select
    i = 1
    Do
        ActiveCell.Offset(1, 0).Range("A1").Select
        ActiveCell.FormulaR1C1 = FDate
        i = i + 1
    Loop Until i >= TotalCount
    ' Selection.AutoFill Destination:=ActiveCell.Range(thisRange)
    ' ActiveCell.Range(thisRange).Select
    ' ActiveCell.Offset(0, -1).Range("A1").Select
    Cells(2, 1).Select
    ActiveCell.FormulaR1C1 = "mouse"
    ActiveCell.Select
    Selection.AutoFill Destination:=ActiveCell.Range(thisRange)
    ActiveCell.Range(thisRange).Select
    ActiveCell.Offset(1, 3).Range("A1").Select
End Sub


