import win32com.client

wb = win32com.client.GetObject(r"C:\Users\eucal\projeto\LISTA_RTD.xlsm")
app = wb.Application

print("Workbook:", wb.Name)
print("App Visible:", app.Visible)
print("Workbooks count:", app.Workbooks.Count)

# agora você tem controle total da instância certa
app.Visible = True
