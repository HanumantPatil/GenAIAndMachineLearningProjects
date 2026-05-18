
// Framework to solve the problem in LLD
// VendingMachine
// Functional Requirements:
// 1. The vending machine should be able to dispense products based on user selection.
// 2. User should be able to insert money into the vending machine.
// 3. User should be able to select a product and receive it if they have inserted enough money.

// Machine: 
// Dispense products based on user selection
// Maintain Inventory of products
// Retun the change
// Handle Insufficient balance
// Inventory out of stock
// Machine should genrate the receipt for the transaction
// Machine should be able to handle multiple transactions
// multiple payment mode 

// Non-Functional Requirements:
// 1. The vending machine should be user-friendly and easy to operate.
// 2. The vending machine should be reliable and have minimal downtime.
// 3. The vending machine should be extensible to accommodate future enhancements.
// differnt payment mode: cash, card, mobile payment
// Thread safety: if multiple users are using the machine at the same time, it should handle concurrent transactions without any issues.
// Error handling: the machine should handle errors gracefully, such as invalid product selection,
// insufficient funds, or out-of-stock items, and provide appropriate feedback to the user.

// Identifying core entity
// Vending Machine
// user
// product
// Invertory -- Map of product and quantity
// Slot -- represents a specific location in the vending machine where a product is stored
// Coin -- represents the money inserted by the user
// Note -- represents the money inserted by the user
// Payment -- represents the payment made by the user, which can be in the form of coins, notes, or card payments
// State -- represents the current state of the vending machine, such as idle, accepting payment, dispensing product, etc.
        // Idle state
        // HasMoney state
        // ProductSelected state
        // Dispensing state
        // OutOfStock state
// 
// User Action/methods
        // inser money
        // select product
        // Dispense product
        // cancel transaction

using System;

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Description { get; set; }
    public decimal Price { get; set; } = 0;
}

class Slot
{
    public int Id { get; set; }
    public Product Product { get; set; }
    public int Quantity { get; set; }
}

class Inventory
{
    private Dictionary<int, Slot> slots = new Dictionary<int, Slot>();
    public void AddProduct(Product product, int quantity)
    {
        if (slots.ContainsKey(product.Id))
        {
            slots[product.Id].Quantity += quantity;
        }
        else
        {
            slots[product.Id] = new Slot { Id = product.Id, Product = product, Quantity = quantity };
        }
    }
    public bool IsProductAvailable(int productId)
    {
        return slots.ContainsKey(productId) && slots[productId].Quantity > 0;
    }
    public void DispenseProduct(int productId)
    {
        if (IsProductAvailable(productId))
        {
            slots[productId].Quantity--;
        }
        else
        {
            throw new Exception("Product is out of stock.");
        }
    }
    public decimal GetProductPrice(int productId)
    {
        if (slots.ContainsKey(productId))
        {
            return slots[productId].Product.Price;
        }
        else
        {
            throw new Exception("Product not found.");
        }
    }

    public enum PaymentMode
    {
        Cash,
        Card,
        MobilePayment
    }
    public enum coin
    {
        Penny = 1,
        Nickel = 5,
        Dime = 10,
        Quarter = 25
    }
    interface IState
    {
        void InsertMoney(decimal amount);
        void SelectProduct(int productId);
        void DispenseProduct();
        void CancelTransaction();
    }

    public class  HasMoneyState : IState
    {
        
    }

    public class IdleState : IState
    {

    }
    public class ProductSelectedState : IState
    {
    }
    public class DispensingState : IState
    {
    }
    public class OutOfStockState : IState
    {
    }

    class VendingMachine
    {
        private Inventory inventory;
        private IState currentState;
        public VendingMachine()
        {
            inventory = new Inventory();
            currentState = new IdleState();
        }
        public void InsertMoney(decimal amount)
        {
            currentState.InsertMoney(amount);
        }
        public void SelectProduct(int productId)
        {
            currentState.SelectProduct(productId);
        }
        public void DispenseProduct()
        {
            currentState.DispenseProduct();
        }
        public void CancelTransaction()
        {
            currentState.CancelTransaction();
        }
    }

