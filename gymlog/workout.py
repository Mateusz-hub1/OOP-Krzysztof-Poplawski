from datetime import date


class Workout:
    def __init__(self, workout_id, athlete_id, workout_date, title):
        if workout_date > date.today():
            raise ValueError("Data treningu nie może być z przyszłości.")
        self._id = workout_id
        self._athlete_id = athlete_id
        self._date = workout_date
        self._title = title
        self._exercises = []

    @property
    def id(self):
        return self._id

    @property
    def athlete_id(self):
        return self._athlete_id

    @property
    def date(self):
        return self._date

    @property
    def title(self):
        return self._title

    @property
    def exercises(self):
        return tuple(self._exercises)

    def add_exercise(self, exercise):
        self._exercises.append(exercise)

    def duration_minutes(self):
        return sum(e.duration_minutes() for e in self._exercises)

    def total_calories(self, body_weight_kg):
        return sum(e.calories(body_weight_kg) for e in self._exercises)

    def exercise_names(self):
        return {e.name for e in self._exercises}

    def report(self, body_weight_kg):
        lines = [f"{self._id} | {self._date} | {self._title} | ok. {self.duration_minutes():g} min, "
                 f"{self.total_calories(body_weight_kg):.0f} kcal"]
        lines += [f"   - {e}" for e in self._exercises]
        return "\n".join(lines)
