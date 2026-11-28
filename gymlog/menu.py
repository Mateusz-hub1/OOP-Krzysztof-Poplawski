from datetime import date, timedelta

from .demo import run_demo
from .exercises import CardioExercise


class ConsoleMenu:
    def __init__(self, gym):
        self._gym = gym
        self._actions = {
            "1": ("Lista zawodników", self.list_athletes),
            "2": ("Dodaj zawodnika", self.add_athlete),
            "3": ("Zapisz nowy trening", self.log_workout),
            "4": ("Historia treningów", self.show_history),
            "5": ("Rekordy życiowe", self.show_records),
            "6": ("Przypisz plan treningowy", self.assign_plan),
            "7": ("Raport tygodniowy planu", self.weekly_report),
            "8": ("Zmień wagę zawodnika", self.change_weight),
            "9": ("Uruchom scenariusz demo", run_demo),
        }

    def run(self):
        while True:
            print("\n===== GymLog – dziennik treningowy =====")
            for key, (label, _) in self._actions.items():
                print(f"{key}. {label}")
            print("0. Wyjście")
            choice = input("Wybierz opcję: ").strip()
            if choice == "0":
                print("Do zobaczenia na siłowni!")
                return
            action = self._actions.get(choice)
            if action is None:
                print("Nieprawidłowy wybór.")
                continue
            try:
                action[1]()
            except ValueError as e:
                print(f"Błąd: {e}")

    @staticmethod
    def _ask_number(prompt, cast=float):
        while True:
            text = input(prompt).strip().replace(",", ".")
            try:
                return cast(text)
            except ValueError:
                print("Podaj poprawną liczbę.")

    def _ask_athlete(self):
        return self._gym.find_athlete(input("ID zawodnika (np. A-001): "))

    def list_athletes(self):
        for athlete in self._gym.athletes:
            print(athlete)

    def add_athlete(self):
        name = input("Imię: ")
        weight = self._ask_number("Waga (kg): ")
        height = self._ask_number("Wzrost (cm): ")
        athlete = self._gym.register_athlete(name, weight, height)
        print(f"Dodano zawodnika {athlete.id}.")

    def log_workout(self):
        athlete = self._ask_athlete()
        title = input("Nazwa treningu (np. Push): ").strip() or "Trening"
        days_ago = self._ask_number("Ile dni temu był trening? (0 = dziś): ", int)
        workout = self._gym.new_workout(athlete.id, title, date.today() - timedelta(days=days_ago))

        while True:
            kind = input("\nDodaj ćwiczenie: [s] siłowe, [c] cardio, [m] masa ciała, [k] koniec: ").strip().lower()
            if kind == "k":
                break
            try:
                if kind == "s":
                    exercise = self._gym.new_strength(input("Nazwa ćwiczenia: "))
                    for i in range(self._ask_number("Ile serii? ", int)):
                        reps = self._ask_number(f"  Seria {i + 1} - powtórzenia: ", int)
                        weight = self._ask_number(f"  Seria {i + 1} - ciężar (kg): ")
                        exercise.add_set(reps, weight)
                elif kind == "c":
                    name = input("Nazwa ćwiczenia: ")
                    activity = input(f"Aktywność ({', '.join(CardioExercise.MET_BY_ACTIVITY)}): ").strip().lower()
                    distance = self._ask_number("Dystans (km): ")
                    minutes = self._ask_number("Czas (min): ")
                    exercise = self._gym.new_cardio(name, activity, distance, minutes)
                elif kind == "m":
                    exercise = self._gym.new_bodyweight(input("Nazwa ćwiczenia: "))
                    for i in range(self._ask_number("Ile serii? ", int)):
                        exercise.add_set(self._ask_number(f"  Seria {i + 1} - powtórzenia: ", int))
                else:
                    print("Nieznany typ ćwiczenia.")
                    continue
                workout.add_exercise(exercise)
                print(f"Dodano: {exercise}")
            except ValueError as e:
                print(f"Błąd: {e} Ćwiczenie nie zostało dodane.")

        new_records = self._gym.log_workout(workout)
        print(f"\nZapisano trening {workout.id}.")
        for record in new_records:
            print(f"NOWY REKORD! {record}")

    def show_history(self):
        athlete = self._ask_athlete()
        if not athlete.workouts:
            print("Brak treningów.")
        for workout in athlete.workouts:
            print(workout.report(athlete.body_weight_kg))

    def show_records(self):
        records = self._gym.personal_records(self._ask_athlete().id)
        if not records:
            print("Brak rekordów.")
        for record in records:
            print(record)

    def assign_plan(self):
        athlete = self._ask_athlete()
        for plan in self._gym.plans:
            print(plan)
        plan = self._gym.find_plan(input("ID planu (np. P-001): "))
        athlete.assign_plan(plan)
        print(f"{athlete.name} ma teraz plan: {plan.name}.")

    def weekly_report(self):
        athlete = self._ask_athlete()
        if athlete.plan is None:
            print("Zawodnik nie ma przypisanego planu.")
            return
        weeks_ago = self._ask_number("Który tydzień? (0 = bieżący, 1 = poprzedni...): ", int)
        today = date.today()
        week_start = today - timedelta(days=today.weekday() + 7 * weeks_ago)
        report = athlete.plan.weekly_report(athlete.workouts, week_start)
        print(f"Plan: {athlete.plan.name} | {report['od']} – {report['do']}")
        print(f"Treningi: {report['treningi']}/{report['cel']} ({report['realizacja_proc']:.0f}%)")
        missing = report["brakujace_cwiczenia"]
        print("Wszystkie kluczowe ćwiczenia zrobione." if not missing else f"Zabrakło: {', '.join(missing)}")

    def change_weight(self):
        athlete = self._ask_athlete()
        athlete.body_weight_kg = self._ask_number("Nowa waga (kg): ")
        print(f"Zaktualizowano. BMI: {athlete.bmi():.1f}")
