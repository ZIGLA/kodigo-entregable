def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ü", "u")
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def any_numeric(text):
    return any(chr.isdigit() for chr in text)

def notnumber(words):
  if any(chr.isdigit() for chr in words):
     word = ''.join([chr for chr in words if not chr.isdigit()])
     return word
  else:
    return words