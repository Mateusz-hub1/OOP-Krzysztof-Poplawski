# Zadanie 3: Średnia ocen 
n = int(input("Ile ocen chcesz wprowadzić? "))

if n <= 0:
    print("Liczba ocen musi być większa od zera.")
else:
    suma = 0
    for i in range(n):
        ocena = float(input(f"Ocena {i + 1}: "))
        while ocena < 1 or ocena > 6:
            ocena = float(input("Ocena musi być z zakresu 1-6, podaj ponownie: "))
        suma += ocena

    srednia = suma / n
    print(f"Średnia: {srednia:.2f}")

    if srednia >= 3.0:
        print("Uczeń zdał.")
    else:
        print("Uczeń nie zdał.")