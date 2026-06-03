using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


/*
 * 
 * 1. user can create group
 * 2. user cab add expense to group
 * 3. Expense can be split equally, by percentage, or by exact amount.
 * 4. Sysytem keeps track of the balance of each user in the group (how much they owe or are owed)
 * 5. user can settle up with other users in the group (marking expenses as paid)
 * 
 * 
 * 
 */

public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
}
public class Group
{
    public int Id { get; set; }
    public string Name { get; set; }
    public List<User> Members { get; set; }
    public List<Expense> Expenses { get; set; }
}

public class Expense
{
    public int Id { get; set; }
    public string Description { get; set; }
    public decimal Amount { get; set; }
    public User PaidBy { get; set; }
    public List<Split> Splits { get; set; }
}

public class Split
{
    public User User { get; set; }
    public decimal Amount { get; set; }
}

public class BalanceManager
{
    public Dictionary<(int, int), decimal> CalculateBalances(Group group)
    {
        var balances = new Dictionary<(int, int), decimal>();
        foreach (var expense in group.Expenses)
        {
            foreach (var split in expense.Splits)
            {
                var key = (expense.PaidBy.Id, split.User.Id);
                if (!balances.ContainsKey(key))
                {
                    balances[key] = 0;
                }
                balances[key] += split.Amount;
            }
        }
        return balances;
    }
}

public class SettlementManager
{
    public void SettleUp(Group group, User fromUser, User toUser, decimal amount)
    {
        var balanceManager = new BalanceManager();
        var balances = balanceManager.CalculateBalances(group);
        var key = (fromUser.Id, toUser.Id);
        if (balances.ContainsKey(key) && balances[key] >= amount)
        {
            balances[key] -= amount;
            // Mark the expense as paid in the system (not implemented here)
        }
        else
        {
            throw new InvalidOperationException("Insufficient balance to settle up.");
        }
    }
}

public class ExpenseManager
{
    public void AddExpense(Group group, string description, decimal amount, User paidBy, List<Split> splits)
    {
        var expense = new Expense
        {
            Id = new Random().Next(1, 1000), // Just for example, use a better ID generation in production
            Description = description,
            Amount = amount,
            PaidBy = paidBy,
            Splits = splits
        };
        group.Expenses.Add(expense);
    }
}
