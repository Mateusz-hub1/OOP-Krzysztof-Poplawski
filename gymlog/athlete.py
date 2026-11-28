class Athlete:
    def __init__(self, athlete_id, name, body_weight_kg, height_cm):
        if not name.strip():
            raise ValueError("Imię nie może być puste.")
        if not 100 <= height_cm <= 250:
            raise ValueError("Wzrost musi być w zakresie 100–250 cm.")
        self._id = athlete_id
        self._name = name.strip()
        self._height_cm = height_cm
        self._body_weight_kg = None
        self.body_weight_kg = body_weight_kg
        self._workouts = []
        self._plan = None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def body_weight_kg(self):
        return self._body_weight_kg

    @body_weight_kg.setter
    def body_weight_kg(self, value):
        if not 30 <= value <= 300:
            raise ValueError("Waga musi być w zakresie 30–300 kg.")
        self._body_weight_kg = value

    @property
    def workouts(self):
        return tuple(sorted(self._workouts, key=lambda w: w.date))

    @property
    def plan(self):
        return self._plan

    def assign_plan(self, plan):
        self._plan = plan

    def add_workout(self, workout):
        if workout.athlete_id != self._id:
            raise ValueError("Ten trening należy do innego uzytkowniak.")
        self._workouts.append(workout)

    def bmi(self):
        return self._body_weight_kg / (self._height_cm / 100) ** 2

    def total_calories(self):
        return sum(w.total_calories(self._body_weight_kg) for w in self._workouts)

    def __str__(self):
        plan = self._plan.name if self._plan else "brak planu"
        return (f"{self._id} | {self._name:<16} | {self._body_weight_kg:g} kg, BMI {self.bmi():.1f} | "
                f"treningi: {len(self._workouts)} | plan: {plan}")
