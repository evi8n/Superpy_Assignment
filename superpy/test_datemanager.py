import os
import datetime
from main import DateManager


class TestDateManager:
    def setup_method(self):
        self.date_file = "test_date.txt"
        self.date_manager = DateManager(self.date_file)

    def teardown_method(self):
        if os.path.exists(self.date_file):
            os.remove(self.date_file)

    def test_load_current_date_existing_file(self):
        test_date = datetime.date(2022, 1, 1)
        with open(self.date_file, "w") as file:
            file.write(test_date.strftime("%Y-%m-%d"))

        assert self.date_manager.load_current_date() == test_date

    def test_advance_time(self):
        current_date = datetime.date(2023, 6, 1)
        self.date_manager.current_date = current_date

        self.date_manager.advance_time(2)

        assert self.date_manager.current_date == datetime.date(2023, 6, 3)

    def test_save_current_date(self):
        current_date = datetime.date(2023, 7, 1)
        self.date_manager.current_date = current_date
        self.date_manager.save_current_date()

        assert os.path.exists(self.date_file)
        with open(self.date_file, "r") as file:
            saved_date_str = file.read().strip()
        assert saved_date_str == current_date.strftime("%Y-%m-%d")

    def test_get_current_date(self):
        current_date = datetime.date(2023, 8, 1)
        self.date_manager.current_date = current_date

        assert self.date_manager.get_current_date() == current_date

    def test_reset_date(self):
        test_date = datetime.date(2023, 12, 2)
        with open(self.date_file, "w") as file:
            file.write(test_date.strftime("%Y-%m-%d"))

        self.date_manager.reset_date()

        assert self.date_manager.current_date == datetime.date.today()

        with open(self.date_file, "r") as file:
            saved_date_str = file.read().strip()
        assert saved_date_str == datetime.date.today().strftime("%Y-%m-%d")
