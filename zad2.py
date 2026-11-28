# Zadanie 2: Przeliczenie temperatur 

kierunek = input("Wybierz kierunek (C - Celsjusz→Fahrenheit, F - Fahrenheit→Celsjusz): ").strip().upper()
temp = float(input("Podaj temperaturę: "))

if kierunek == "C":
    print(f"{temp:g}°C = {temp * 1.8 + 32:g}°F")
elif kierunek == "F":
    print(f"{temp:g}°F = {(temp - 32) / 1.8:g}°C")
else:
    print("Nieznany kierunek konwersji.")
