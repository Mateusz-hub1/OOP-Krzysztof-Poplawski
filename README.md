# Zadanie 2 – tworzenie klas i obiektów

Wybrany temat: **system bankowy** (temat nr 5 z listy). Prosta aplikacja konsolowa w Pythonie i w C#. Można w niej zakładać konta, wpłacać, wypłacać, robić przelewy i przeglądać historię transakcji. Obie wersje działają tak samo.

## Klasy

- **`Transaction`** – pojedyncza operacja na koncie. Przechowuje typ (wpłata, wypłata, przelew), kwotę, saldo po operacji, opis i datę.
- **`Account`** – konto bankowe z numerem, właścicielem, saldem i listą transakcji. Ma metody `Wplac` i `Wyplac`, które sprawdzają, czy kwota jest dodatnia i czy na koncie są wystarczające środki.
- **`Bank`** – zarządza kontami: otwiera nowe konto z kolejnym numerem (od 1001), szuka konta po numerze i robi przelew między dwoma kontami.

## Co z OOP jest użyte

- **Enkapsulacja** – salda nie da się zmienić z zewnątrz bezpośrednio, tylko przez `Wplac` / `Wyplac`. W C# jest to `public decimal Saldo { get; private set; }`, a w Pythonie pole `_saldo` z `@property` tylko do odczytu.
- **Konstruktory** – konto dostaje numer i właściciela przy tworzeniu, a bank dostaje nazwę.
- **Relacje** – konto ma listę transakcji, a bank trzyma konta w słowniku (numer → konto). Przelew to wypłata z jednego konta i wpłata na drugie, obie zapisane w historii.
- **Obsługa błędów** – zła kwota, brak środków, nieistniejące konto albo przelew na to samo konto kończą się komunikatem, a program działa dalej.

## Pliki

```
zad.py           wersja w Pythonie (wszystkie klasy + menu)
Account.cs       klasa Account
Transaction.cs   klasa Transaction
Bank.cs          klasa Bank
Program.cs       menu konsolowe
Bank.csproj      projekt C#
```

## Uruchomienie

```
python3 zad.py
```

```
dotnet run
```

Na starcie są już dwa przykładowe konta: 1001 (Jan Kowalski, 1000 zł) i 1002 (Anna Nowak, 500 zł), więc od razu można testować przelewy.

## Menu

```
1. Otwórz konto
2. Lista kont
3. Wpłata
4. Wypłata
5. Przelew
6. Historia transakcji
0. Wyjście
```
