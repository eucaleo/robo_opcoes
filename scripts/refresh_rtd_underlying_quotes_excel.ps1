param(
    [string]$WorkbookPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "LISTA_RTD.xlsm"),
    [string]$SymbolsPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "dados\rtd_underlying_symbols.txt"),
    [string]$CsvPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "dados\RTD_UNDERLYING_QUOTES.csv"),
    [int]$WaitSeconds = 25,
    [switch]$Visible
)

$ErrorActionPreference = "Stop"

function CsvEscape([object]$Value) {
    if ($null -eq $Value) {
        return ""
    }

    $Text = [string]$Value
    $Text = $Text.Replace([string][char]13, " ").Replace([string][char]10, " ")

    if ($Text.Contains(";") -or $Text.Contains('"')) {
        $Text = $Text.Replace('"', '""')
        return '"' + $Text + '"'
    }

    return $Text
}

if (!(Test-Path $WorkbookPath)) {
    throw "Workbook not found: $WorkbookPath"
}

if (!(Test-Path $SymbolsPath)) {
    throw "Symbols file not found: $SymbolsPath"
}

$symbols = Get-Content $SymbolsPath |
    ForEach-Object { $_.Trim().ToUpper() } |
    Where-Object { $_ -ne "" } |
    Sort-Object -Unique

if ($symbols.Count -eq 0) {
    throw "No underlying symbols found in: $SymbolsPath"
}

Write-Host "Underlying symbols loaded:" $symbols.Count

$excel = $null
$workbook = $null

try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = [bool]$Visible
    $excel.DisplayAlerts = $false
    $excel.AskToUpdateLinks = $false

    try {
        $excel.Calculation = -4105
    }
    catch {
        Write-Host "Warning: could not change Excel calculation mode. Continuing."
    }

    $workbook = $excel.Workbooks.Open(
        (Resolve-Path $WorkbookPath).Path,
        3,
        $false
    )

    $sheetName = "RTD_UNDERLYING_QUOTES"
    $sheet = $null

    foreach ($ws in $workbook.Worksheets) {
        if ($ws.Name -eq $sheetName) {
            $sheet = $ws
            break
        }
    }

    if ($null -eq $sheet) {
        $sheet = $workbook.Worksheets.Add()
        $sheet.Name = $sheetName
    }

    $sheet.Cells.Clear() | Out-Null

    $headers = @(
        "ativo",
        "ultimo_preco",
        "vwap",
        "bid",
        "ask",
        "close_price",
        "prev_close",
        "open_price",
        "high_price",
        "low_price",
        "volume",
        "change_percent"
    )

    for ($i = 0; $i -lt $headers.Count; $i++) {
        $sheet.Cells.Item(1, $i + 1).Value2 = $headers[$i]
    }

    $row = 2

    foreach ($sym in $symbols) {
        $sheet.Cells.Item($row, 1).Value2 = $sym

        $sheet.Cells.Item($row, 2).Formula = '=RTD("btg_pro_rtd","","QUOTE.LAST_TRADE_PRICE",$A' + $row + ')'
        $sheet.Cells.Item($row, 3).Formula = '=RTD("btg_pro_rtd","","QUOTE.VWAP",$A' + $row + ')'
        $sheet.Cells.Item($row, 4).Formula = '=RTD("btg_pro_rtd","","QUOTE.BID_PRICE",$A' + $row + ')'
        $sheet.Cells.Item($row, 5).Formula = '=RTD("btg_pro_rtd","","QUOTE.ASK_PRICE",$A' + $row + ')'
        $sheet.Cells.Item($row, 6).Formula = '=RTD("btg_pro_rtd","","QUOTE.CLOSE",$A' + $row + ')'
        $sheet.Cells.Item($row, 7).Formula = '=RTD("btg_pro_rtd","","QUOTE.PREV_CLOSE",$A' + $row + ')'
        $sheet.Cells.Item($row, 8).Formula = '=RTD("btg_pro_rtd","","QUOTE.OPEN",$A' + $row + ')'
        $sheet.Cells.Item($row, 9).Formula = '=RTD("btg_pro_rtd","","QUOTE.HIGH",$A' + $row + ')'
        $sheet.Cells.Item($row, 10).Formula = '=RTD("btg_pro_rtd","","QUOTE.LOW",$A' + $row + ')'
        $sheet.Cells.Item($row, 11).Formula = '=RTD("btg_pro_rtd","","QUOTE.VOLUME",$A' + $row + ')'
        $sheet.Cells.Item($row, 12).Formula = '=RTD("btg_pro_rtd","","QUOTE.CHGPERCENT",$A' + $row + ')'

        $row++
    }

    Write-Host "Sheet RTD_UNDERLYING_QUOTES filled. Rows:" $symbols.Count
    Write-Host "Recalculating Excel/RTD..."

    try {
        $excel.CalculateFullRebuild()
    }
    catch {
        try {
            $excel.CalculateFull()
        }
        catch {
            $excel.Calculate()
        }
    }

    Start-Sleep -Seconds $WaitSeconds

    $lastRow = $symbols.Count + 1
    $lastCol = $headers.Count

    $lines = New-Object System.Collections.Generic.List[string]

    for ($r = 1; $r -le $lastRow; $r++) {
        $values = New-Object System.Collections.Generic.List[string]

        for ($c = 1; $c -le $lastCol; $c++) {
            $cellText = $sheet.Cells.Item($r, $c).Text
            $values.Add((CsvEscape $cellText))
        }

        $lines.Add(($values -join ";"))
    }

    $csvDir = Split-Path -Parent $CsvPath

    if (!(Test-Path $csvDir)) {
        New-Item -ItemType Directory -Path $csvDir | Out-Null
    }

    Write-Host "Exporting CSV to:" $CsvPath
    Set-Content -Path $CsvPath -Value $lines -Encoding UTF8

    $workbook.Save()

    Write-Host "OK: CSV generated at" $CsvPath
}
finally {
    if ($null -ne $workbook) {
        $workbook.Close($true)
    }

    if ($null -ne $excel) {
        $excel.Quit()
    }

    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
