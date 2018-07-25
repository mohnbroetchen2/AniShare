Attribute VB_Name = "TickAtLabAniShare"

Sub TickAtLabAniShare()
    Dim document   As Object
    Dim dispatcher As Object
    Dim oSheet As Object
    Dim TotalCount As Integer
    Dim thisRange As String
    Dim i As Integer
    Dim FDate As Date
    Dim TDate As Date
    Dim notice As Boolean
    Dim noticetext As String
    Dim user As String
    
    notice = False
    noticetext = "Please note that at least one responsible person is missing. It's a mandatory field for AniShare."
    
    TotalCount = ActiveSheet.UsedRange.Rows.Count - 1
    thisRange = "A1:A" + CStr(TotalCount)
    Columns("A:L").Select
    Selection.Delete Shift:=xlToLeft
    Range("A1").Select
    ActiveCell.FormulaR1C1 = "Comment"
    Range("B1").Select
    ActiveCell.FormulaR1C1 = "Sex"
    Range("C1").Select
    ActiveCell.FormulaR1C1 = "Line / Strain (Name)"
    Range("D1").Select
    ActiveCell.FormulaR1C1 = "ID"
    Range("E1").Select
    ActiveCell.FormulaR1C1 = "DOB"
    Columns("F:F").Select
    Selection.Delete Shift:=xlToLeft
    ActiveCell.FormulaR1C1 = "Amount"
    Columns("G:H").Select
    Selection.Delete Shift:=xlToLeft
    Columns("G:G").Select
    Selection.Delete Shift:=xlToLeft
    Range("G1").Select
    ActiveCell.FormulaR1C1 = "License number"
    Columns("H:H").Select
    Selection.Delete Shift:=xlToLeft
    ActiveCell.FormulaR1C1 = "Building"
    Columns("I:I").Select
    ActiveCell.FormulaR1C1 = "Animal-ID1"
    Columns("I:J").Select
    Selection.Delete Shift:=xlToLeft
    Columns("J:J").Select
    Selection.Delete Shift:=xlToLeft
    Range("I1").Select
    ActiveCell.FormulaR1C1 = "Responsible"
    Range("I2").Select
    i = 1
    Do
        user = ActiveCell.FormulaR1C1
        If Len(user) <> 0 Then
            responsibleuser
        Else
            notice = True
            With ActiveCell.Interior
                .Pattern = xlSolid
                .PatternColorIndex = xlAutomatic
                .Color = 65535
                .TintAndShade = 0
                .PatternTintAndShade = 0
            End With
        End If
        ActiveCell.Offset(1, 0).Range("A1").Select
        i = i + 1
    Loop Until i >= TotalCount
    
     Cells(1, 1).Select
    Range("A1").EntireColumn.Insert
    Range("A1").EntireColumn.Insert
    Range("A1").EntireColumn.Insert
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
    ActiveCell.Select
    i = 1
    Do
        ActiveCell.Offset(1, 0).Range("A1").Select
        ActiveCell.FormulaR1C1 = TDate
        i = i + 1
    Loop Until i >= TotalCount
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
    Cells(2, 1).Select
    ActiveCell.FormulaR1C1 = "fish"
    ActiveCell.Select
    Selection.AutoFill Destination:=ActiveCell.Range(thisRange)
    ActiveCell.Range(thisRange).Select
    ActiveCell.Offset(1, 3).Range("A1").Select
    
    If notice = True Then
        MsgBox noticetext, vbOKOnly, "Responsible person is missing"
    End If
    
End Sub

Sub responsibleuser()
    Dim respUser As String
    Dim user As String
    user = ActiveCell.FormulaR1C1
    respUser = Right(user, Len(user) - InStr(user, ",") - 1) + " " + Left(user, InStr(user, ",") - 1)
    ActiveCell.FormulaR1C1 = respUser
End Sub


