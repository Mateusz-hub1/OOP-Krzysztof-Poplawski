# Zadanie 1: kalkulator dwóch liczb

a = float(input("Podaj pierwszą liczbę: "))
b = float(input("Podaj druga liczbę: "))
op = input("Podaj operację (+, -, *, /): ").strip()

if op == "+":
    print(f"Wynik: {a + b:g}")
elif op == "-":
    print(f"Wynik: {a - b:g}")
elif op == "*":
    print(f"Wynik: {a * b:g}")
elif op == "/":
    if b == 0:
        print("Błąd: nie można dzielić przez zero.")
    else:
        print(f"Wynik: {a / b:g}")
else:
    print("Nieznana operacja.")
