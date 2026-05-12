using System;

public interface IPayment
{
    void Pay(decimal amount);
}

public class GrowPayment : IPayment
{
    public void Pay(decimal amount)
    {
        Console.WriteLine($"Grow Payment: ${amount}");
    }
}

public class StribePayment
{
    public void StribePay(decimal amount)
    {
        Console.WriteLine($"Stribe pay: ${amount}");
    }
}

public class AdapterPayment : IPayment
{
    private StribePayment payment;

    public AdapterPayment(StribePayment payment)
    {
        this.payment = payment;
    }

    public void Pay(decimal amount)
    {
        payment.StribePay(amount);
    }
}

// Test the Adapter Design Pattern
Console.WriteLine("=== Testing Adapter Design Pattern ===");
Console.WriteLine();

// Using GrowPayment directly (implements IPayment)
IPayment growPayment = new GrowPayment();
growPayment.Pay(100);

// Using StribePayment through adapter
IPayment stripeAdapter = new AdapterPayment(new StribePayment());
stripeAdapter.Pay(200);

Console.WriteLine();
Console.WriteLine("=== Test Complete ===");
