from abc import ABC, abstractmethod


class Exercise(ABC):
    def __init__(self, exercise_id, name):
        if not name.strip():
            raise ValueError("Nazwa ćwiczenia nie może być pusta.")
        self._id = exercise_id
        self._name = name.strip()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @abstractmethod
    def exercise_type(self):
        pass

    @abstractmethod
    def duration_minutes(self):
        pass

    @abstractmethod
    def met(self):
        pass

    @abstractmethod
    def record_value(self):
        pass

    @abstractmethod
    def record_unit(self):
        pass

    @abstractmethod
    def summary(self):
        pass

    def calories(self, body_weight_kg):
        return self.met() * body_weight_kg * self.duration_minutes() / 60

    def __str__(self):
        return f"[{self.exercise_type()}] {self._name}: {self.summary()}"


class ExerciseSet:
    def __init__(self, reps, weight_kg=0.0):
        if reps <= 0:
            raise ValueError("Liczba powtórzeń musi być większa od zera.")
        if weight_kg < 0:
            raise ValueError("Ciężar nie może być ujemny.")
        self._reps = reps
        self._weight_kg = weight_kg

    @property
    def reps(self):
        return self._reps

    @property
    def weight_kg(self):
        return self._weight_kg

    def volume(self):
        return self._reps * self._weight_kg

    def __str__(self):
        return f"{self._reps}x{self._weight_kg:g}kg" if self._weight_kg else f"{self._reps}"


class StrengthExercise(Exercise):
    MINUTES_PER_SET = 3

    def __init__(self, exercise_id, name):
        super().__init__(exercise_id, name)
        self._sets = []

    def add_set(self, reps, weight_kg):
        if weight_kg <= 0:
            raise ValueError("W ćwiczeniu siłowym podaj ciężar większy od zera.")
        self._sets.append(ExerciseSet(reps, weight_kg))

    @property
    def sets(self):
        return tuple(self._sets)

    def total_volume(self):
        return sum(s.volume() for s in self._sets)

    def estimated_one_rep_max(self):
        if not self._sets:
            return 0.0
        return max(s.weight_kg * (1 + s.reps / 30) for s in self._sets)

    def exercise_type(self):
        return "Siłowe"

    def duration_minutes(self):
        return len(self._sets) * self.MINUTES_PER_SET

    def met(self):
        return 5.0

    def record_value(self):
        return self.estimated_one_rep_max()

    def record_unit(self):
        return "kg (szac. 1RM)"

    def summary(self):
        sets = ", ".join(str(s) for s in self._sets) or "brak serii"
        return f"{sets} | objętość {self.total_volume():g} kg | 1RM ≈ {self.estimated_one_rep_max():.1f} kg"


class CardioExercise(Exercise):
    MET_BY_ACTIVITY = {"bieg": 9.8, "rower": 7.5, "wioślarz": 7.0, "orbitrek": 5.0}

    def __init__(self, exercise_id, name, activity, distance_km, minutes):
        super().__init__(exercise_id, name)
        if activity not in self.MET_BY_ACTIVITY:
            raise ValueError(f"Nieznana aktywność. Dostępne: {', '.join(self.MET_BY_ACTIVITY)}.")
        if distance_km <= 0 or minutes <= 0:
            raise ValueError("Dystans i czas muszą być większe od zera.")
        self._activity = activity
        self._distance_km = distance_km
        self._minutes = minutes

    @property
    def activity(self):
        return self._activity

    @property
    def distance_km(self):
        return self._distance_km

    @property
    def minutes(self):
        return self._minutes

    def pace_min_per_km(self):
        return self._minutes / self._distance_km

    def exercise_type(self):
        return "Cardio"

    def duration_minutes(self):
        return self._minutes

    def met(self):
        return self.MET_BY_ACTIVITY[self._activity]

    def record_value(self):
        return self._distance_km

    def record_unit(self):
        return "km"

    def summary(self):
        pace = self.pace_min_per_km()
        return (f"{self._activity}, {self._distance_km:g} km w {self._minutes:g} min "
                f"| tempo {int(pace)}:{round(pace % 1 * 60):02d} min/km")


class BodyweightExercise(Exercise):
    MINUTES_PER_SET = 2

    def __init__(self, exercise_id, name):
        super().__init__(exercise_id, name)
        self._sets = []

    def add_set(self, reps):
        self._sets.append(ExerciseSet(reps))

    @property
    def sets(self):
        return tuple(self._sets)

    def total_reps(self):
        return sum(s.reps for s in self._sets)

    def exercise_type(self):
        return "Masa ciała"

    def duration_minutes(self):
        return len(self._sets) * self.MINUTES_PER_SET

    def met(self):
        return 4.0

    def record_value(self):
        return max((s.reps for s in self._sets), default=0)

    def record_unit(self):
        return "powt. w serii"

    def summary(self):
        sets = ", ".join(str(s) for s in self._sets) or "brak serii"
        return f"serie: {sets} | razem {self.total_reps()} powt."
