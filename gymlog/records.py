class PersonalRecord:
    def __init__(self, exercise_name, value, unit, record_date, workout_id):
        self.exercise_name = exercise_name
        self.value = value
        self.unit = unit
        self.date = record_date
        self.workout_id = workout_id

    def __str__(self):
        return f"{self.exercise_name:<22} {round(self.value, 1):>7g} {self.unit:<15} ({self.date}, {self.workout_id})"


class PersonalRecordTracker:
    def __init__(self):
        self._records = {}

    def update(self, athlete_id, workout):
        records = self._records.setdefault(athlete_id, {})
        new_records = []
        for exercise in workout.exercises:
            value = exercise.record_value()
            current = records.get(exercise.name)
            if value > 0 and (current is None or value > current.value):
                record = PersonalRecord(exercise.name, value, exercise.record_unit(), workout.date, workout.id)
                records[exercise.name] = record
                new_records.append(record)
        return new_records

    def records_for(self, athlete_id):
        return sorted(self._records.get(athlete_id, {}).values(), key=lambda r: r.exercise_name)
