Attribute VB_Name = "PyRatAniShareOrgan"
Sub PyRatAniShareOrgan()

    Dim document   As Object
    Dim dispatcher As Object
    Dim oSheet As Object
    Dim TotalCount As Integer
    Dim thisRange As String
    Dim i As Integer
    Dim FDate As Date
    Dim TDate As Date
    TotalCount = ActiveSheet.UsedRange.Rows.Count - 1
    thisRange = "A1:A" + CStr(TotalCount)
    
    Cells(1, 1).Select
    Range("A1").EntireColumn.Insert
    Range("A1").EntireColumn.Insert
    Range("A1").EntireColumn.Insert
    Range("A1").EntireColumn.Insert
    ActiveCell.Select
    ActiveCell.FormulaR1C1 = "Animal type"
    ActiveCell.Offset(0, 1).Range("A1").Select
    ActiveCell.FormulaR1C1 = "Organ used"
    ActiveCell.Offset(0, 1).Range("A1").Select
    ActiveCell.FormulaR1C1 = "Euthanasia performed by"
    ActiveCell.Offset(0, 1).Range("A1").Select
    ActiveCell.FormulaR1C1 = "Comment"
    ActiveCell.Offset(1, 0).Range("A1").Select
    
    Cells.Find(What:="Sacrifice date", After:=ActiveCell, LookIn:=xlFormulas _
    , LookAt:=xlPart, SearchOrder:=xlByRows, SearchDirection:=xlNext, _
    MatchCase:=False, SearchFormat:=False).Activate
    ActiveCell.Offset(1, 0).Range("A1").Select
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
