from datetime import date, timedelta

from .gym_log import GymLog
from .records import PersonalRecordTracker
from .sample_data import load_sample_data


def step(title):
    print(f"\n--- {title} ---")


def run_demo():
    gym = GymLog(PersonalRecordTracker())
    load_sample_data(gym)
    mateusz = gym.find_athlete("A-001")

    step("1. Obiekty utworzone przez konstruktory (zawodnicy i plany)")
    for athlete in gym.athletes:
        print(athlete)
    for plan in gym.plans:
        print(plan)

    step("2. Polimorfizm: te same metody na różnych typach ćwiczeń")
    last_workout = next(w for w in mateusz.workouts if len(w.exercises) == 3)
    for exercise in last_workout.exercises:
        print(f"{exercise.exercise_type():<11} {exercise.name:<18} "
              f"{exercise.calories(mateusz.body_weight_kg):>5.0f} kcal | rekord: "
              f"{round(exercise.record_value(), 1):g} {exercise.record_unit()}")

    step("3. Historia treningów Mateusza")
    for workout in mateusz.workouts:
        print(workout.report(mateusz.body_weight_kg))

    step("4. Nowy trening i automatyczne wykrycie rekordu życiowego")
    workout = gym.new_workout(mateusz.id, "Legs - ciężki dzień")
    squat = gym.new_strength("Przysiad")
    squat.add_set(5, 110)
    squat.add_set(3, 115)
    workout.add_exercise(squat)
    for record in gym.log_workout(workout):
        print(f"NOWY REKORD! {record}")

    step("5. Rekordy życiowe Mateusza")
    for record in gym.personal_records(mateusz.id):
        print(record)

    step("6. Enkapsulacja: walidacja chroni dane przed błędną zmianą")
    for opis, akcja in [
        ("waga zawodnika = -5 kg", lambda: setattr(mateusz, "body_weight_kg", -5)),
        ("seria z ciężarem 0 kg", lambda: gym.new_strength("Wiosłowanie").add_set(8, 0)),
        ("cardio 'pływanie'", lambda: gym.new_cardio("Basen", "pływanie", 1, 30)),
        ("trening z przyszłą datą", lambda: gym.new_workout(mateusz.id, "X", date.today() + timedelta(days=1))),
    ]:
        try:
            akcja()
        except ValueError as e:
            print(f"Odrzucono ({opis}): {e}")

    step("7. Abstrakcja: nie da się utworzyć ogólnego ćwiczenia")
    from .exercises import Exercise
    try:
        Exercise("E-999", "Jakieś ćwiczenie")
    except TypeError:
        print("Exercise jest klasą abstrakcyjną, obiekt można utworzyć tylko z klasy szczegółowej.")

    step("8. Raport realizacji planu za poprzedni tydzień")
    last_monday = date.today() - timedelta(days=date.today().weekday() + 7)
    report = mateusz.plan.weekly_report(mateusz.workouts, last_monday)
    print(f"Plan: {mateusz.plan.name} | {report['od']} – {report['do']}")
    print(f"Treningi: {report['treningi']}/{report['cel']} ({report['realizacja_proc']:.0f}%)")
    missing = report["brakujace_cwiczenia"]
    print("Wszystkie kluczowe ćwiczenia zrobione." if not missing else f"Zabrakło: {', '.join(missing)}")

    print(f"\nŁącznie spalone kalorie (Mateusz): {mateusz.total_calories():.0f} kcal")
