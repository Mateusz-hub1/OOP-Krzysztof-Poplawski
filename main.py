from gymlog.gym_log import GymLog
from gymlog.menu import ConsoleMenu
from gymlog.records import PersonalRecordTracker
from gymlog.sample_data import load_sample_data


def main():
    gym = GymLog(PersonalRecordTracker())
    load_sample_data(gym)
    ConsoleMenu(gym).run()


if __name__ == "__main__":
    main()
