param(
    [string]$WorkbookPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "LISTA_RTD.xlsm"),
    [string]$SymbolsPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "dados\rtd_symbols.txt"),
    [string]$CsvPath = (Join-Path (Split-Path -Parent $PSScriptRoot) "dados\RTD_LINKS.csv"),
    [int]$WaitSeconds = 20,
    [switch]$Visible
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8


function Invoke-WithRetry {
    param(
        [scriptblock]$Block,
        [int]$Retries = 20,
        [int]$DelayMs = 500
    )

    for ($i = 1; $i -le $Retries; $i++) {
        try {
            return & $Block
        } catch {
            if ($i -eq $Retries) {
                throw
            }
            Start-Sleep -Milliseconds $DelayMs
        }
    }
}

if (!(Test-Path $SymbolsPath)) {
    throw "Arquivo de símbolos não encontrado: $SymbolsPath"
}

$symbols = Get-Content $SymbolsPath |
    ForEach-Object { $_.Trim().ToUpper() } |
    Where-Object { $_ -ne "" } |
    Select-Object -Unique

if ($symbols.Count -eq 0) {
    throw "Nenhum símbolo encontrado em: $SymbolsPath"
}

Write-Host "Símbolos carregados:" $symbols.Count

$excel = New-Object -ComObject Excel.Application
$excel.Visible = [bool]$Visible
$excel.DisplayAlerts = $false
$excel.EnableEvents = $false

# xlCalculationAutomatic = -4105
try {
    $excel.Calculation = -4105
} catch {
    Write-Host ("Aviso: não foi possível alterar o modo de cálculo do Excel. Continuando. Detalhe: " + $_.Exception.Message)
}
try {
    $wb = Invoke-WithRetry { $excel.Workbooks.Open($WorkbookPath) }

    $sheetName = "RTD_OPTION_QUOTES"

    $ws = $null
    foreach ($s in $wb.Worksheets) {
        if ($s.Name -eq $sheetName) {
            $ws = $s
            break
        }
    }

    if ($null -eq $ws) {
        $ws = $wb.Worksheets.Add()
        $ws.Name = $sheetName
    }

    Invoke-WithRetry { $ws.Cells.Clear() | Out-Null }

    $headers = @(
        "codigo_opcao",
        "ativo_base",
        "call_put",
        "strike",
        "vencimento",
        "ultimo_preco",
        "ultima_quantidade",
        "bid",
        "ask",
        "volume",
        "iv",
        "delta",
        "gamma",
        "theta",
        "vega"
    )

    for ($c = 1; $c -le $headers.Count; $c++) {
        $ws.Cells.Item(1, $c).Value2 = $headers[$c - 1]
    }

    $fields = @(
        "QUOTE.UNDERLYING_SYMBOL",
        "QUOTE.OPTION_TYPE",
        "QUOTE.STRIKE_PRICE",
        "QUOTE.MATURITYDATE",
        "QUOTE.LAST_TRADE_PRICE",
        "QUOTE.LAST_TRADE_QUANTITY",
        "QUOTE.BID_PRICE",
        "QUOTE.ASK_PRICE",
        "QUOTE.VOLUME",
        "QUOTE.IMPLIED_VOLATILITY",
        "QUOTE.DELTA",
        "QUOTE.GAMMA",
        "QUOTE.THETA",
        "QUOTE.VEGA"
    )

    $row = 2

    foreach ($sym in $symbols) {
        $ws.Cells.Item($row, 1).Value2 = $sym

        for ($i = 0; $i -lt $fields.Count; $i++) {
            $col = $i + 2
            $field = $fields[$i]
            $formula = '=RTD("btg_pro_rtd";"";"' + $field + '";$A' + $row + ')'
            $ws.Cells.Item($row, $col).FormulaLocal = $formula
        }

        $row++
    }

    $lastRow = $symbols.Count + 1
    $lastCol = $headers.Count

    Invoke-WithRetry { $ws.Range($ws.Cells.Item(1,1), $ws.Cells.Item($lastRow,$lastCol)).Columns.AutoFit() | Out-Null }

    Write-Host "Aba RTD_OPTION_QUOTES preenchida. Linhas:" $symbols.Count
    Write-Host "Recalculando Excel/RTD..."

    Invoke-WithRetry { $excel.CalculateFullRebuild() | Out-Null }

    Start-Sleep -Seconds $WaitSeconds

    Write-Host "Exportando CSV para:" $CsvPath

    if (Test-Path $CsvPath) {
        Remove-Item $CsvPath -Force
    }

    # Copia somente a aba RTD_OPTION_QUOTES para novo workbook e salva como CSV UTF-8.
    Invoke-WithRetry { $ws.Copy() | Out-Null }
    $csvWb = $excel.ActiveWorkbook

    # 62 = xlCSVUTF8
    Invoke-WithRetry { $csvWb.SaveAs($CsvPath, 62) | Out-Null }
    Invoke-WithRetry { $csvWb.Close($false) | Out-Null }

    Invoke-WithRetry { $wb.Save() | Out-Null }
    Invoke-WithRetry { $wb.Close($false) | Out-Null }

    Write-Host "OK: CSV gerado em $CsvPath"
}
finally {
    $excel.Quit() | Out-Null
}
