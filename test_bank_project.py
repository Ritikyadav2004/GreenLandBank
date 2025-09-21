import unittest
from unittest.mock import patch, MagicMock
import bcrypt

# Import your main banking code as a module
import bank_system  # <-- rename your file as bank_system.py

class TestBankSystem(unittest.TestCase):

    def setUp(self):
        # Mock DB cursor and connection
        self.conn_mock = MagicMock()
        self.cur_mock = MagicMock()
        bank_system.conn = self.conn_mock
        bank_system.cur = self.cur_mock

    # ---------- Test Account Creation ----------
    @patch("builtins.input", side_effect=[
        "9876543210",  # mobile
        "123456",      # OTP
        "Ritik",       # name
        "01-01-2000",  # dob
        "Bhopal",      # address
        "123412341234",# Aadhaar
        "ritik@test.com",# email
        "1000",        # deposit
        "1234",        # pin
        "1"            # e-passbook option
    ])
    def test_account_creation(self, mock_input):
        self.cur_mock.fetchall.return_value = []
        bank_system.getinfo()
        self.cur_mock.execute.assert_called()  # DB insert called
        self.conn_mock.commit.assert_called()

    # ---------- Test Login Success ----------
    @patch("builtins.input", side_effect=["12345", "1234"])
    def test_login_success(self, mock_input):
        hashed_pin = bcrypt.hashpw(b"1234", bcrypt.gensalt())
        self.cur_mock.fetchall.return_value = [
            [None, "Ritik", "12345", 5000.0, None, "Bhopal", None, None, None, hashed_pin]
        ]
        bank_system.login()
        self.cur_mock.execute.assert_called()

    # ---------- Test Login Failure ----------
    @patch("builtins.input", side_effect=["12345", "0000"])
    def test_login_wrong_pin(self, mock_input):
        hashed_pin = bcrypt.hashpw(b"1234", bcrypt.gensalt())
        self.cur_mock.fetchall.return_value = [
            [None, "Ritik", "12345", 5000.0, None, "Bhopal", None, None, None, hashed_pin]
        ]
        bank_system.login()
        # Should not commit anything
        self.conn_mock.commit.assert_not_called()

    # ---------- Test Deposit ----------
    @patch("builtins.input", side_effect=["12345", "1234", "500"])
    def test_deposit(self, mock_input):
        hashed_pin = bcrypt.hashpw(b"1234", bcrypt.gensalt())
        self.cur_mock.fetchall.return_value = [
            [None, "Ritik", "12345", 1000.0, None, "Bhopal", None, None, None, hashed_pin]
        ]
        bank_system.run_program  # dummy reference (to avoid recursion)
        bank_system.main_menu    # dummy reference
        bank_system.conn.commit.reset_mock()
        # Call deposit part directly
        # Normally you'd extract it into a function
        # For now, just simulate
        # (If your deposit logic is in run_program, restructure later)

    # ---------- Test Withdraw ----------
    @patch("builtins.input", side_effect=["12345", "1234", "200"])
    def test_withdraw(self, mock_input):
        hashed_pin = bcrypt.hashpw(b"1234", bcrypt.gensalt())
        self.cur_mock.fetchall.return_value = [
            [None, "Ritik", "12345", 1000.0, None, "Bhopal", None, None, None, hashed_pin]
        ]
        # Simulate withdraw
        # Similar restructure needed for cleaner testing

    # ---------- Test Transfer Money ----------
    @patch("builtins.input", side_effect=["12345", "1234", "54321", "500"])
    def test_transfer_money(self, mock_input):
        hashed_pin = bcrypt.hashpw(b"1234", bcrypt.gensalt())
        self.cur_mock.fetchall.side_effect = [
            [[None, "Ritik", "12345", 1000.0, None, "Bhopal", None, None, None, hashed_pin]],  # sender
            [[None, "Aman", "54321", 2000.0, None, "Delhi", None, None, None, hashed_pin]]   # receiver
        ]
        bank_system.transferMoney()
        self.conn_mock.commit.assert_called()

if __name__ == "__main__":
    unittest.main()
