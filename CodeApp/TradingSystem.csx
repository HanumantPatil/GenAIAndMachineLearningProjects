/*
 * 
 * 
 * Buy/Sell orders
 * Order Book
 * Price-time priority
 * partial fills, Full fills, cancellations
 * Trade Execution
 * Matching engine
 * 
 * 
 * Trading System
 * user 
 * order
 * oreder type 
 * order status
 * matching engine
 * oreder book
 * Trading System
 * 
 * 
 * 
 * 
 */
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.DateTime;
using System.DateTimeOffset;

public enum OrderType
{
    Buy,
    Sell
}
enum OrderStatus
{
    Open,
    PartiallyFilled,
    Filled,
    Cancelled
}
public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
}
public class Order
{
    public int Id { get; set; }
    public User User { get; set; }
    public OrderType Type { get; set; }
    public decimal Price { get; set; }
    public int Quantity { get; set; }
    public OrderStatus Status { get; set; }
    public DateTimeOffset CreatedAt { get; set; }
}

public class Trade
{
    public int Id { get; set; }
    public Order BuyOrder { get; set; }
    public Order SellOrder { get; set; }
    public decimal Price { get; set; }
    public int Quantity { get; set; }
    public DateTimeOffset ExecutedAt { get; set; }
}

public class OrderBook
{
    public List<Order> BuyOrders { get; set; }
    public List<Order> SellOrders { get; set; }    
    public decimal Price { get; set; } = 0;
    //Max heap and min heap for buy and sell orders respectively

    public int Quantity { get; set; }
    public void AddOrder(Order order)
    {
        if (order.Type == OrderType.Buy)
        {
            BuyOrders.Add(order);
            //Add to max heap
        }
        else
        {
            SellOrders.Add(order);
            //Add to min heap
        }
    }



}
public class MatchingEngine
{
    public List<Trade> Trades { get; set; }
    public void MatchOrders(OrderBook orderBook)
    {
        //Match orders based on price-time priority
        //Execute trades and update order status
    }
}