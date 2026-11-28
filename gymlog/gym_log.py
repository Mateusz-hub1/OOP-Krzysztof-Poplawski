from datetime import date

from .athlete import Athlete
from .exercises import BodyweightExercise, CardioExercise, StrengthExercise
from .ids import IdGenerator
from .plan import TrainingPlan
from .workout import Workout


class GymLog:
    def __init__(self, record_tracker):
        self._records = record_tracker
        self._athletes = {}
        self._plans = {}
        self._athlete_ids = IdGenerator("A")
        self._workout_ids = IdGenerator("W")
        self._exercise_ids = IdGenerator("E")
        self._plan_ids = IdGenerator("P")

    @property
    def athletes(self):
        return tuple(self._athletes.values())

    @property
    def plans(self):
        return tuple(self._plans.values())

    def register_athlete(self, name, body_weight_kg, height_cm):
        athlete = Athlete(self._athlete_ids.next_id(), name, body_weight_kg, height_cm)
        self._athletes[athlete.id] = athlete
        return athlete

    def find_athlete(self, athlete_id):
        athlete = self._athletes.get(athlete_id.strip().upper())
        if athlete is None:
            raise ValueError(f"Nie ma zawodnika o ID {athlete_id}.")
        return athlete

    def create_plan(self, name, workouts_per_week, key_exercises):
        plan = TrainingPlan(self._plan_ids.next_id(), name, workouts_per_week, key_exercises)
        self._plans[plan.id] = plan
        return plan

    def find_plan(self, plan_id):
        plan = self._plans.get(plan_id.strip().upper())
        if plan is None:
            raise ValueError(f"Nie ma planu o ID {plan_id}.")
        return plan

    def new_workout(self, athlete_id, title, workout_date=None):
        athlete = self.find_athlete(athlete_id)
        return Workout(self._workout_ids.next_id(), athlete.id, workout_date or date.today(), title)

    def new_strength(self, name):
        return StrengthExercise(self._exercise_ids.next_id(), name)

    def new_cardio(self, name, activity, distance_km, minutes):
        return CardioExercise(self._exercise_ids.next_id(), name, activity, distance_km, minutes)

    def new_bodyweight(self, name):
        return BodyweightExercise(self._exercise_ids.next_id(), name)

    def log_workout(self, workout):
        if not workout.exercises:
            raise ValueError("Trening musi zawierać co najmniej jedno ćwiczenie.")
        athlete = self.find_athlete(workout.athlete_id)
        athlete.add_workout(workout)
        return self._records.update(athlete.id, workout)

    def personal_records(self, athlete_id):
        return self._records.records_for(self.find_athlete(athlete_id).id)
