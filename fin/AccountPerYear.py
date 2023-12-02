class AccountPerYear:

    def __init__(self, file_path, df, account_name, account_category, account_number, account_type, year):
        self.file_path = file_path
        self.df = df
        self.name = account_name
        self.category = account_category
        self.number = account_number
        self.type = account_type
        self.year = year

    def __str__(self):
        return f'{self.category} {self.name} {self.number} {self.year}'

    def get_label(self):
        return self.name  + '_' +  self.category

    def equals(self, number_or_label):
        return self.number == number_or_label or self.get_label() == number_or_label


class AccountsPerYear:

    def __init__(self):
        self.accounts: [AccountPerYear] = []

    def add_account(self, account: AccountPerYear):
        self.accounts += [account]

    def get_account(self, number_or_label):
        for account in self.accounts:
            if account.equals(number_or_label):
                return account
        return None

    def __len__(self):
        return len(self.accounts)
