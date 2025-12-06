const codeSamples = {
    oop: {
        title: "Object-Oriented Programming (Java)",
        code: `public class BankAccount {
    private String accountNumber;
    private double balance;
    private String accountHolder;
    
    // Constructor
    public BankAccount(String accountNumber, String accountHolder) {
        this.accountNumber = accountNumber;
        this.accountHolder = accountHolder;
        this.balance = 0.0;
    }
    
    // Deposit method
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println("Deposited: $" + amount);
        } else {
            System.out.println("Invalid deposit amount");
        }
    }
    
    // Withdraw method - POTENTIAL ISSUE: No overdraft check
    public void withdraw(double amount) {
        balance -= amount;
        System.out.println("Withdrawn: $" + amount);
    }
    
    // Get balance
    public double getBalance() {
        return balance;
    }
    
    // Transfer method
    public void transfer(BankAccount target, double amount) {
        if (amount > 0 && this.balance >= amount) {
            this.withdraw(amount);
            target.deposit(amount);
        } else {
            System.out.println("Transfer failed: insufficient funds");
        }
    }
}`,
        defects: [
            "No overdraft protection in withdraw method",
            "Missing input validation in constructor",
            "Potential floating-point precision issues with double",
            "No synchronization for thread safety"
        ],
        questions: [
            {
                question: "What happens if you withdraw more money than the account balance?",
                options: ["Transaction fails", "Overdraft occurs", "Exception thrown", "Balance becomes negative"]
            },
            {
                question: "How is the initial balance set when creating a new account?",
                options: ["Passed as parameter", "Always zero", "Random value", "Set by bank rules"]
            }
        ]
    },

    functional: {
        title: "Functional Programming (JavaScript)",
        code: `// Functional programming approach for bank operations
const createAccount = (accountNumber, accountHolder) => ({
    accountNumber,
    accountHolder,
    balance: 0
});

const deposit = (account, amount) => ({
    ...account,
    balance: account.balance + Math.max(0, amount)
});

const withdraw = (account, amount) => ({
    ...account,
    balance: account.balance - amount  // ISSUE: No balance check
});

const transfer = (fromAccount, toAccount, amount) => {
    const updatedFrom = withdraw(fromAccount, amount);
    const updatedTo = deposit(toAccount, amount);
    
    return [updatedFrom, updatedTo];
};

// Account operations pipeline
const processTransactions = (account, transactions) => {
    return transactions.reduce((acc, transaction) => {
        if (transaction.type === 'deposit') {
            return deposit(acc, transaction.amount);
        } else if (transaction.type === 'withdraw') {
            return withdraw(acc, transaction.amount);
        }
        return acc;
    }, account);
};

// Example usage
const account = createAccount('123456', 'John Doe');
const transactions = [
    { type: 'deposit', amount: 1000 },
    { type: 'withdraw', amount: 200 },
    { type: 'withdraw', amount: 1500 }  // POTENTIAL: Over-withdrawal
];`,
        defects: [
            "No balance validation in withdraw function",
            "Immutability not enforced in all cases",
            "Missing error handling for invalid transactions",
            "Potential performance issues with object spreading"
        ],
        questions: [
            {
                question: "What programming principle is demonstrated by the spread operator usage?",
                options: ["Immutability", "Inheritance", "Polymorphism", "Encapsulation"]
            },
            {
                question: "What happens when processing the third transaction (withdraw 1500)?",
                options: ["Error thrown", "Balance becomes negative", "Transaction skipped", "Account frozen"]
            }
        ]
    },

    procedural: {
        title: "Procedural Programming (C)",
        code: `#include <stdio.h>
#include <string.h>

#define MAX_ACCOUNTS 100
#define MAX_NAME_LENGTH 50

struct BankAccount {
    char accountNumber[20];
    char accountHolder[MAX_NAME_LENGTH];
    double balance;
};

struct BankAccount accounts[MAX_ACCOUNTS];
int accountCount = 0;

// Function to create new account
int createAccount(char* accNum, char* holder) {
    if (accountCount >= MAX_ACCOUNTS) {
        return -1; // Error: array full
    }
    
    strcpy(accounts[accountCount].accountNumber, accNum);
    strcpy(accounts[accountCount].accountHolder, holder);
    accounts[accountCount].balance = 0.0;
    
    return accountCount++;
}

// Function to deposit money
void deposit(int accountIndex, double amount) {
    if (amount > 0) {
        accounts[accountIndex].balance += amount;
        printf("Deposited: $%.2f\\n", amount);
    }
}

// Function to withdraw money - ISSUE: No balance check
void withdraw(int accountIndex, double amount) {
    accounts[accountIndex].balance -= amount;
    printf("Withdrawn: $%.2f\\n", amount);
}

// Function to transfer money
void transfer(int fromIndex, int toIndex, double amount) {
    if (amount > 0 && accounts[fromIndex].balance >= amount) {
        withdraw(fromIndex, amount);
        deposit(toIndex, amount);
        printf("Transfer completed\\n");
    } else {
        printf("Transfer failed\\n");
    }
}

// Function to find account by number
int findAccount(char* accNum) {
    for (int i = 0; i < accountCount; i++) {
        if (strcmp(accounts[i].accountNumber, accNum) == 0) {
            return i;
        }
    }
    return -1; // Not found
}`,
        defects: [
            "Global array with fixed size limit",
            "No bounds checking in string operations",
            "Withdraw function allows negative balances",
            "Missing error handling in createAccount",
            "Potential memory safety issues"
        ],
        questions: [
            {
                question: "What is the maximum number of accounts this system can handle?",
                options: ["50", "100", "200", "Unlimited"]
            },
            {
                question: "What happens when strcpy is used with long names?",
                options: ["Automatic truncation", "Buffer overflow", "Compilation error", "Runtime warning"]
            }
        ]
    }
};