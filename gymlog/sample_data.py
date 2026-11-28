from datetime import date, timedelta


def load_sample_data(gym):
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    last_monday = monday - timedelta(days=7)

    mateusz = gym.register_athlete("Mateusz", 82, 182)
    julia = gym.register_athlete("Julia", 50, 158)

    ppl = gym.create_plan("Push Pull Legs", 3, ["Wyciskanie leżąc", "Przysiad", "Martwy ciąg"])
    fbw = gym.create_plan("FBW + cardio", 2, ["Przysiad", "Bieg"])
    mateusz.assign_plan(ppl)
    julia.assign_plan(fbw)

    w = gym.new_workout(mateusz.id, "Push", last_monday)
    bench = gym.new_strength("Wyciskanie leżąc")
    for reps, kg in [(8, 70), (6, 75), (5, 77.5)]:
        bench.add_set(reps, kg)
    dips = gym.new_bodyweight("Dipy")
    for reps in [12, 10, 9]:
        dips.add_set(reps)
    w.add_exercise(bench)
    w.add_exercise(dips)
    gym.log_workout(w)

    w = gym.new_workout(mateusz.id, "Legs", last_monday + timedelta(days=2))
    squat = gym.new_strength("Przysiad")
    for reps, kg in [(8, 90), (6, 100), (5, 105)]:
        squat.add_set(reps, kg)
    w.add_exercise(squat)
    gym.log_workout(w)

    w = gym.new_workout(mateusz.id, "Pull + cardio", last_monday + timedelta(days=4))
    deadlift = gym.new_strength("Martwy ciąg")
    for reps, kg in [(5, 120), (5, 130), (3, 140)]:
        deadlift.add_set(reps, kg)
    pullups = gym.new_bodyweight("Podciąganie")
    for reps in [10, 8, 7]:
        pullups.add_set(reps)
    w.add_exercise(deadlift)
    w.add_exercise(pullups)
    w.add_exercise(gym.new_cardio("Bieg", "bieg", 3, 18))
    gym.log_workout(w)

    w = gym.new_workout(julia.id, "FBW A", last_monday + timedelta(days=1))
    squat = gym.new_strength("Przysiad")
    for reps, kg in [(10, 40), (8, 45), (8, 47.5)]:
        squat.add_set(reps, kg)
    w.add_exercise(squat)
    w.add_exercise(gym.new_cardio("Bieg", "bieg", 5, 30))
    gym.log_workout(w)

    w = gym.new_workout(julia.id, "Cardio", last_monday + timedelta(days=5))
    w.add_exercise(gym.new_cardio("Rower", "rower", 15, 40))
    gym.log_workout(w)

    if monday < today:
        w = gym.new_workout(mateusz.id, "Push", monday)
        bench = gym.new_strength("Wyciskanie leżąc")
        for reps, kg in [(8, 72.5), (6, 77.5), (4, 80)]:
            bench.add_set(reps, kg)
        w.add_exercise(bench)
        gym.log_workout(w)
