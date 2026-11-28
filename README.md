# Zadanie 1 – przypomnienie podstaw programowania

Trzy proste programy konsolowe, każdy napisany w Pythonie i w C#. Ćwiczą podstawy: wczytywanie danych z konsoli, `if/else` (w C# także `switch`), pętle i działania na liczbach.

## Podzadania

1. **Kalkulator dwóch liczb** – użytkownik podaje dwie liczby i operację (`+`, `-`, `*`, `/`), a program wypisuje wynik. Dzielenie przez zero jest obsłużone.
2. **Konwerter temperatur** – `C` przelicza Celsjusze na Fahrenheity, `F` przelicza w drugą stronę. Wzory: °F = °C × 1.8 + 32 oraz °C = (°F − 32) / 1.8.
3. **Średnia ocen** – użytkownik podaje liczbę ocen i kolejne oceny (1–6). Program liczy średnią i sprawdza, czy uczeń zdał (średnia co najmniej 3.0). Ocena spoza zakresu jest wczytywana jeszcze raz.

## Pliki

```
zad1.py, zad2.py, zad3.py     wersje w Pythonie
zad1.txt, zad2.txt, zad3.txt  kod C# każdego podzadania
task.cs                       plik uruchamiany przez dotnet (domyślnie wklejone zadanie 1)
task.csproj                   projekt C#
```

## Uruchomienie

**Python**

```
python3 zad1.py
python3 zad2.py
python3 zad3.py
```

**C#**

Kod każdego podzadania jest w osobnym pliku `.txt`. Żeby uruchomić wybrane podzadanie, wklejam zawartość odpowiedniego `zadX.txt` do `task.cs` i odpalam:

```
dotnet run
```

Domyślnie w `task.cs` jest wklejone zadanie 1.

## Przykłady

```
Podaj pierwszą liczbę: 10
Podaj drugą liczbę: 20
Podaj operację (+, -, *, /): +
Wynik: 30
```

```
Wybierz kierunek (C - Celsjusz→Fahrenheit, F - Fahrenheit→Celsjusz): C
Podaj temperaturę: 0
0°C = 32°F
```

```
Ile ocen chcesz wprowadzić? 5
Ocena 1: 4
Ocena 2: 5
Ocena 3: 3
Ocena 4: 4
Ocena 5: 2
Średnia: 3.60
Uczeń zdał.
```

W C# separatorem liczb dziesiętnych jest kropka, ale przecinek też działa, bo program sam zamienia go na kropkę.
