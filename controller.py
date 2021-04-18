import sys

class Bank:
    def __init__(self):
        self.bank_data = {}

    def add_entry(self, card_num, pin, account, amt):
        self.bank_data[card_num] = {"pin":pin, "account":{account:amt}}

    def add_account(self, card_num, account, amt):
        if card_num in self.bank_data:
            self.bank_data[card_num]["account"][account] = amt

    def check_pin(self, card_num, entered_pin):
        if card_num in self.bank_data and self.bank_data[card_num]["pin"] == entered_pin:
            return self.bank_data[card_num]["account"]
        else:
            return None

    def update_account(self, card_num, account, amt):
        if self.bank_data[card_num]["account"][account] in self.bank_data[card_num]["account"]:
            self.bank_data[card_num]["account"][account] = amt
            return True
        else:
            return False


class Controller:
    def __init__(self, bank, cash):
        self.Bank = bank
        self.accounts = None
        self.cash_bin = cash

    def swipe(self, card_num, pin):
        self.accounts = self.Bank.check_pin(card_num, pin)
        if self.accounts is None:
            return 0, "Invalid Card or Incorrect Pin!"
        else:
            return 1, "Welcome!"

    def account_select(self, acc):
        if acc in self.accounts:
            return True
        else:
            return False

    def account_actions(self, card_num, acc, action, amt=0):
        if action == "See Balance":
            return self.accounts[acc], 1
        elif action == "Withdraw":
            if self.accounts[acc] >= amt and self.cash_bin >= amt:
                new_balance = self.accounts[acc] - amt
                self.accounts[acc] = new_balance
                self.Bank.update_account(card_num, acc, new_balance)
                return self.accounts[acc], 1
            else:
                return self.accounts[acc], 0
        elif action == "Deposit":
            new_balance = self.accounts[acc] + amt
            self.cash_bin += amt
            self.accounts[acc] = new_balance
            self.Bank.update_account(card_num, acc, new_balance)
            return self.accounts[acc], 1
        else:
            return self.accounts[acc], 2

    # This is a method to test functionality
    def __call__(self, card_num, pin, acc, action_list):
        leave = False
        while leave is not True:
            v, m = self.swipe(card_num, pin)
            if v == 0:
                return "Invalid Card or Incorrect Pin!"
            check = self.account_select(acc)
            if check is False:
                return "Invalid Account!"
            for action in action_list:
                if action[0] == "Leave":
                    return "Gracefully departed"
                balance, bit = self.account_actions(card_num, acc, action[0], action[1])
                if bit == 0:
                    continue
                elif bit == 2:
                    return "Invalid action"
                else:
                    continue
            return "Actions completed"


if __name__ == "__main__":

    empty_bank = Bank()
    # Test Controller on Empty Bank
    empty_atm = Controller(empty_bank, 0)
    valid, message = empty_atm.swipe(0, 0)
    if valid == 0:
        print("Test Invalid Message on Empty ATM -- PASS")
    else:
        print("Test Invalid Message on Empty ATM -- FAIL")

    # Generating an interesting bank

    test_bank = Bank()
    test_bank.add_entry(123456789, 1234, "checking", 1000)
    test_bank.add_account(123456789, "savings", 1000)
    test_bank.add_entry(987654321, 7321, "checking", 5000)
    test_atm = Controller(test_bank, 10000)
    action_list1 = [("See Balance",0), ("Withdraw", 40), ("Withdraw", 1000), ("Deposit", 100)]

    # These next test should be a correctly executing test case
    if test_atm(987654321, 7321, "checking", action_list1) == "Actions completed":
        print("Test Success on Valid ATM -- PASS")
    else:
        print("Test Success on Valid ATM -- FAIL")

    # Tests whether ATM handles overdraft attempt without crashing
    if test_atm(123456789, 1234, "checking", action_list1) == "Actions completed":
        print("Test Overdraft handling -- PASS")
    else:
        print("Test Overdraft handling -- FAIL")

    # Test incorrect PIN number
    if test_atm(987654321, 1234, "checking", action_list1) == "Invalid Card or Incorrect Pin!":
        print("Test Incorrect Pin Number -- PASS")
    else:
        print("Test Incorrect Pin Number -- FAIL")

    # Test incorrect Account number
    if test_atm(876504321, 1234, "checking", action_list1) == "Invalid Card or Incorrect Pin!":
        print("Test Incorrect Acc Number -- PASS")
    else:
        print("Test Incorrect Acc Number -- FAIL")

    test_bank2 = Bank()
    test_bank2.add_entry(123456789, 1234, "checking", 1000)
    test_bank2.add_account(123456789, "savings", 1000)
    test_bank2.add_entry(987654321, 7321, "checking", 5000)
    test_atm2 = Controller(test_bank2, 10000)
    cash_bin_over_action = [("See Balance", 0), ("Withdraw", 30000)]

    # Tests cash bin excess handling on account balance
    if test_atm(987654321, 7321, "checking", cash_bin_over_action) == "Actions completed":
        print("Test cash bin excess handling -- PASS")
    else:
        print("Test cash bin excess handling -- Fail")

    exit_action = [("See Balance", 0), ("Leave", 0)]
    if test_atm(987654321, 7321, "checking", exit_action) == "Gracefully departed":
        print("Test exiting -- PASS")
    else:
        print("Test exiting -- Fail")