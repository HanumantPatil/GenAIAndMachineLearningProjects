using System;



public interface IPayment
{
    void Pay();
}

public class CardPayment : IPayment
{
    public void Pay()
    {
        Console.WriteLine("Card Payment executed");
    }
}

public class UPIPayment : IPayment
{
    public void Pay()
    {
        Console.WriteLine("UPI Payment executed.");
    }
}


// Call all payment methods 
IPayment payment = new CardPayment();
payment.Pay();

IPayment payment1 = new UPIPayment();

payment1.Pay();


// Run Script comand dotnet script Practice01\DependancyInversionPrinciple.csx 


