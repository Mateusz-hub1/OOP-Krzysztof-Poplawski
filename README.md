# GymLog – dziennik treningowy

## Temat aplikacji

GymLog to konsolowa aplikacja w Pythonie do prowadzenia dziennika treningowego na siłowni. Zawodnik zapisuje treningi złożone z różnych typów ćwiczeń: siłowych (serie z ciężarem), cardio (dystans i czas) oraz z masą ciała (serie powtórzeń). Aplikacja liczy objętość treningu, szacowany ciężar maksymalny (1RM), tempo biegu i spalone kalorie. Sama wykrywa nowe rekordy życiowe i sprawdza, jak zawodnik realizuje przypisany plan treningowy w danym tygodniu.

## Uruchomienie

Wymagany Python 3.8 lub nowszy, bez dodatkowych bibliotek.

```
python3 main.py
```

Po starcie aplikacja ładuje przykładowe dane: zawodników `A-001` (Mateusz) i `A-002` (Julia), plany `P-001` i `P-002` oraz kilka treningów z ostatnich dwóch tygodni. Opcja **9** w menu uruchamia scenariusz demo, który krok po kroku pokazuje najważniejsze metody i wszystkie cztery zasady OOP. Demo pracuje na osobnej kopii danych, więc nie zmienia danych z menu.

## Struktura projektu

```
main.py                 punkt startowy: tworzy GymLog, ładuje dane, uruchamia menu
gymlog/
  ids.py                IdGenerator
  exercises.py          Exercise (abstrakcyjna), ExerciseSet, StrengthExercise, CardioExercise, BodyweightExercise
  workout.py            Workout
  athlete.py            Athlete
  plan.py               TrainingPlan
  records.py            PersonalRecord, PersonalRecordTracker
  gym_log.py            GymLog
  menu.py               ConsoleMenu
  sample_data.py        przykładowe dane
  demo.py               scenariusz demo
```

## Lista klas

| Klasa | Odpowiedzialność | Najważniejsze właściwości | Najważniejsze metody |
|---|---|---|---|
| `IdGenerator` | Nadaje unikalne identyfikatory z prefiksem | `_prefix`, `_counter` | `next_id()` → np. `A-001`, `W-012` |
| `Exercise` *(abstrakcyjna)* | Wspólny kontrakt dla każdego ćwiczenia | `id`, `name` | abstrakcyjne: `exercise_type()`, `duration_minutes()`, `met()`, `record_value()`, `record_unit()`, `summary()`; wspólne: `calories(waga)` |
| `ExerciseSet` | Jedna seria: powtórzenia i ciężar, z walidacją | `reps`, `weight_kg` | `volume()` |
| `StrengthExercise` | Ćwiczenie siłowe z seriami z ciężarem | `sets` | `add_set(reps, kg)`, `total_volume()`, `estimated_one_rep_max()` |
| `CardioExercise` | Ćwiczenie wytrzymałościowe | `activity`, `distance_km`, `minutes` | `pace_min_per_km()` |
| `BodyweightExercise` | Ćwiczenie z masą ciała (pompki, podciąganie) | `sets` | `add_set(reps)`, `total_reps()` |
| `Workout` | Jeden trening: data, tytuł, lista ćwiczeń | `id`, `athlete_id`, `date`, `title`, `exercises` | `add_exercise()`, `duration_minutes()`, `total_calories()`, `report()` |
| `Athlete` | Zawodnik, jego dane, treningi i plan | `id`, `name`, `body_weight_kg` (z walidacją), `workouts`, `plan` | `add_workout()`, `assign_plan()`, `bmi()`, `total_calories()` |
| `TrainingPlan` | Plan: ile treningów w tygodniu i jakie ćwiczenia kluczowe | `id`, `name`, `workouts_per_week`, `key_exercises` | `weekly_report(treningi, początek_tygodnia)` |
| `PersonalRecord` | Pojedynczy rekord życiowy | `exercise_name`, `value`, `unit`, `date`, `workout_id` | `__str__()` |
| `PersonalRecordTracker` | Przechowuje i aktualizuje rekordy zawodników | `_records` | `update(athlete_id, workout)` → lista nowych rekordów, `records_for(athlete_id)` |
| `GymLog` | Główny serwis: rejestruje zawodników i plany, tworzy obiekty z ID, zapisuje treningi | `athletes`, `plans` | `register_athlete()`, `find_athlete()`, `create_plan()`, `new_workout()`, `new_strength()`, `new_cardio()`, `new_bodyweight()`, `log_workout()`, `personal_records()` |
| `ConsoleMenu` | Komunikacja z użytkownikiem w konsoli (tylko interfejs, bez logiki) | `_gym`, `_actions` | `run()` i metody dla poszczególnych opcji menu |

Każdy główny obiekt ma jednoznaczny identyfikator: zawodnik `A-…`, trening `W-…`, ćwiczenie `E-…`, plan `P-…`.

## Relacje między klasami

| Klasy | Typ relacji | Gdzie w kodzie |
|---|---|---|
| `StrengthExercise`, `CardioExercise`, `BodyweightExercise` → `Exercise` | **Dziedziczenie** („jest rodzajem”) | `exercises.py` |
| `StrengthExercise` / `BodyweightExercise` ◆ `ExerciseSet` | **Kompozycja** i **kolekcja**: serie powstają wewnątrz ćwiczenia w `add_set()` i nie istnieją bez niego | `exercises.py` |
| `Workout` ◇ `Exercise` | **Agregacja** i **kolekcja**: ćwiczenie jest przekazywane jako **parametr metody** `add_exercise(exercise)` | `workout.py` |
| `Athlete` ◇ `Workout` | **Kolekcja** (zawodnik ma wiele treningów) | `athlete.py` |
| `Athlete` → `TrainingPlan` | **Agregacja przez właściwość**: plan istnieje niezależnie i może być przypisany wielu zawodnikom | `athlete.py`, `assign_plan()` |
| `Workout` → `Athlete` | **Identyfikator ID**: trening przechowuje `athlete_id`, a nie cały obiekt zawodnika | `workout.py` |
| `GymLog` → `PersonalRecordTracker` | **Parametr konstruktora / Dependency Injection**: tracker jest tworzony na zewnątrz i przekazywany do `GymLog(tracker)` | `gym_log.py`, `main.py` |
| `GymLog` → `IdGenerator` | **Kompozycja**: generatory ID są tworzone w konstruktorze `GymLog` | `gym_log.py` |
| `PersonalRecordTracker` → `PersonalRecord` | **Zwracanie obiektu z metody** (`update()` zwraca listę nowych rekordów) i kolekcja rekordów | `records.py` |
| `ConsoleMenu` → `GymLog` | **Parametr konstruktora**: menu korzysta z serwisu, ale nie zawiera logiki biznesowej | `menu.py` |

## Cztery zasady OOP w projekcie

### Enkapsulacja
- Wszystkie pola są „prywatne” (prefiks `_`) i udostępniane przez `@property` tylko do odczytu, np. `Athlete.id`, `Workout.date`, `ExerciseSet.reps`.
- `Athlete.body_weight_kg` ma **setter z walidacją**: waga spoza zakresu 30–300 kg jest odrzucana. Z tego settera korzysta też konstruktor.
- Kolekcje zwracane są jako `tuple` / `frozenset` (`Workout.exercises`, `Athlete.workouts`, `TrainingPlan.key_exercises`), więc nie da się ich zmienić z zewnątrz z pominięciem metod `add_…()`.
- Konstruktory pilnują poprawnego stanu początkowego: niepusta nazwa, dodatni ciężar, znana aktywność cardio, data treningu nie z przyszłości, wzrost w zakresie.
- Zawodnik nie przyjmie cudzego treningu (`add_workout()` sprawdza `athlete_id`).

### Dziedziczenie
- `Exercise` jest klasą ogólną, a `StrengthExercise`, `CardioExercise` i `BodyweightExercise` to klasy szczegółowe. Każda z nich *jest rodzajem* ćwiczenia.
- Klasy pochodne wywołują `super().__init__(...)`, dziedziczą `id`, `name`, `calories()` i `__str__()` oraz dodają własne dane (serie, dystans, czas).
- Tam, gdzie zachodzi relacja „ma”, zamiast dziedziczenia użyto kompozycji lub agregacji (zawodnik *ma* treningi, trening *ma* ćwiczenia).

### Polimorfizm
- `Workout.total_calories()` i `duration_minutes()` wywołują `calories()` / `duration_minutes()` na każdym ćwiczeniu, nie sprawdzając jego typu. Każdy typ liczy czas i MET po swojemu.
- `PersonalRecordTracker.update()` wywołuje `record_value()` i `record_unit()`. Dla ćwiczenia siłowego rekordem jest szacowany 1RM w kg, dla cardio najdłuższy dystans w km, a dla masy ciała najwięcej powtórzeń w serii.
- `str(exercise)` korzysta z `summary()`, które każda klasa implementuje inaczej.
- Scenariusz demo (krok 2) pokazuje to na jednym treningu z trzema typami ćwiczeń.

### Abstrakcja
- `Exercise` dziedziczy po `ABC` i ma metody `@abstractmethod`: `exercise_type()`, `duration_minutes()`, `met()`, `record_value()`, `record_unit()` i `summary()`. To kontrakt, który musi zrealizować każde ćwiczenie.
- Reszta systemu (`Workout`, `PersonalRecordTracker`) zna tylko ten kontrakt, a nie szczegóły klas szczegółowych.
- Nie da się utworzyć obiektu `Exercise` bezpośrednio (krok 7 demo pokazuje, że Python zgłasza `TypeError`).
- Wspólny wzór na kalorie (`MET × waga × czas`) jest zapisany raz w klasie abstrakcyjnej.

## Jedna odpowiedzialność klasy

Logika domeny (`Athlete`, `Workout`, ćwiczenia, `TrainingPlan`), rekordy (`PersonalRecordTracker`), nadawanie ID (`IdGenerator`), koordynacja (`GymLog`) i interfejs konsolowy (`ConsoleMenu`) są w osobnych klasach. Menu tylko pyta użytkownika i wyświetla wyniki, a wszystkie reguły są w klasach modelu.

## Wzory użyte w obliczeniach

- Kalorie: `MET × waga [kg] × czas [h]`. Przyjęte wartości MET: siłowe 5.0, masa ciała 4.0, bieg 9.8, rower 7.5, wioślarz 7.0, orbitrek 5.0. Czas ćwiczeń seriowych jest szacowany: 3 min na serię siłową i 2 min na serię z masą ciała.
- Szacowany 1RM (wzór Epleya): `ciężar × (1 + powtórzenia / 30)`.
- Objętość: suma `powtórzenia × ciężar` ze wszystkich serii.
- BMI: `waga / wzrost[m]²`.
