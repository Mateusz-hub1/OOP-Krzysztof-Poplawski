from datetime import timedelta


class TrainingPlan:
    def __init__(self, plan_id, name, workouts_per_week, key_exercises):
        if not 1 <= workouts_per_week <= 7:
            raise ValueError("Liczba treningów w tygodniu musi być od 1 do 7.")
        self._id = plan_id
        self._name = name
        self._workouts_per_week = workouts_per_week
        self._key_exercises = set(key_exercises)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def workouts_per_week(self):
        return self._workouts_per_week

    @property
    def key_exercises(self):
        return frozenset(self._key_exercises)

    def weekly_report(self, workouts, week_start):
        week_end = week_start + timedelta(days=6)
        in_week = [w for w in workouts if week_start <= w.date <= week_end]
        done = set().union(*(w.exercise_names() for w in in_week)) if in_week else set()
        missing = self._key_exercises - done
        adherence = min(len(in_week) / self._workouts_per_week, 1.0) * 100
        return {
            "od": week_start,
            "do": week_end,
            "treningi": len(in_week),
            "cel": self._workouts_per_week,
            "realizacja_proc": adherence,
            "brakujace_cwiczenia": sorted(missing),
        }

    def __str__(self):
        return (f"{self._id} | {self._name} | {self._workouts_per_week}x/tydz. | "
                f"kluczowe: {', '.join(sorted(self._key_exercises))}")
