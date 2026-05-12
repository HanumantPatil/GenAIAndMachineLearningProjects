using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CodeApp
{
    public interface IPayment
    {
        public void Pay(decimal amount);
    }

    public class GrowPayment : IPayment
    {
        public void Pay(decimal amount)
        {
            Console.WriteLine("Grow Payment.....");
        }
    }

    public class StribePayment
    {
        public void StribePay(decimal amount)
        {
            Console.WriteLine("Stribe pay.....");
        }
    }

   public class AdapterPayment : IPayment
    {
        StribePayment payment;

       public AdapterPayment(StribePayment payment)
        {
            this.payment = payment;
        }

        public void Pay(decimal amount)
        {
            payment.StribePay(amount);
        }
    }

    // Adapter Design Pattern is a structural design pattern that allows incompatible interfaces to work together.
    internal class AdapterDesignPattern
    {
        public void Execute()
        {
            IPayment payment1 = new AdapterPayment(new StribePayment());
            payment1.Pay(100);
        }
    }

}
