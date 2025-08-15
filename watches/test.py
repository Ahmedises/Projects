value = "Casio - Youth - F - 91WM - 7ADF"
import re
value = re.sub(r'\s*-\s*', ' - ', value)
parts = value.split(' - ')
new = parts[0]
print(new)