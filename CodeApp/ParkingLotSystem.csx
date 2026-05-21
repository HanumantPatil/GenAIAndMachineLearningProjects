/*
 * 
 * 
    Problem Statement: Design a parking lot system that can manage multiple parking lots, each with a certain capacity. 
    The system should allow cars to park and unpark, and it should keep track of the available spaces in each parking lot.

    Functionality Requirements:
        - Entry and Exit Gate 
        - vehicle types (e.g., car, motorcycle, truck) and corresponding parking space requirements
        - Floor management (e.g., assigning parking spaces based on vehicle type and availability)
        - Ticketing system (e.g., generating parking tickets with entry time, calculating parking fees based on duration)
        - Payment system (e.g., accepting payments for parking fees, providing change if necessary)
        - Assign parking spaces to vehicles based on their type and availability
        - Handle edge cases such as full parking lots, invalid vehicle types, and payment errors
        - Parking slot system should be designed to be scalable and maintainable, allowing for future enhancements such as integration with mobile apps for parking reservations and real-time availability updates.
        - Slot selection strategy (e.g., nearest available slot, random assignment, or a more complex algorithm based on usage patterns)

 * 
 * 
 * 
 
    Functional Requirements:
        - Should suppot multiple entry and exit gates for the parking lot
        - Should allocate parking spaces based on vehicle type and availability
        - Should generate parking tickets with entry time and calculate parking fees based on duration
        - multiple payment options (e.g., cash, credit card, mobile payment)
        - multiple vehicle types (e.g., car, motorcycle, truck) and corresponding parking space requirements
        - payment system should handle errors gracefully and provide clear feedback to users
        - multiple parking lots with different capacities should be supported, and the system should keep track of available spaces in each lot

    Non-Functional Requirements:
            - The system should be designed to be scalable and maintainable, allowing for future enhancements such as integration with mobile apps for parking reservations and real-time availability updates.
            - The system should be designed with security in mind, ensuring that sensitive information such as payment details is protected.
            - The system should be designed to handle high traffic volumes, especially during peak hours, without significant performance degradation.
            - Thread safety should be considered, especially if the system is expected to handle concurrent parking and unparking operations across multiple entry and exit gates.

    Core Entities:
        - Parking lot
        - Parking Floor
        - Parking lot
        - ticket 
        - vehical 
        - payment 
        - fee Stratergy 
        - Slot allocationt stratergy 
        - Entry gate 
        - Exit gate
        - Parking lot manager

    Relationships:
        - A parking lot can have multiple parking floors.
        - Each parking floor can have multiple parking spaces.
        - A vehicle can park in a parking space and receive a ticket.
        - The ticket contains information about the entry time and the assigned parking space.
        - When a vehicle unparks, the system calculates the parking fee based on the duration of the stay and the fee strategy.
        - The payment system processes the payment for the parking fee and provides feedback to the user.
 * 
 * 
 */


enum SlotType
{
    Compact,
    Regular,
    Large
}

enum TicketStatus
{
    Active,
    Paid,
    Expired
}

enum PaymentMethod
{
    Cash,
    CreditCard,
    MobilePayment
}
enum VehicleType
{
    Car,
    Motorcycle,
    Truck
}
// Core Entities
public class Vehicle
{
    public string LicensePlate { get; set; }
    public string OwnerName { get; set; }
    public VehicleType Type { get; set; }

}

public class ParkingSpace
{
    public string Id { get; set; }
    public SlotType Type { get; set; }
    public bool IsOccupied { get; set; } = false;
    public Vehicle ParkedVehicle { get; set; }

    public bool ParkVehicle(Vehicle vehicle)
    {
        if (IsOccupied || !IsCompatible(vehicle))
            return false;
        ParkedVehicle = vehicle;
        IsOccupied = true;
        return true;
    }
    public bool UnparkVehicle()
    {
        if (!IsOccupied)
            return false;
        ParkedVehicle = null;
        IsOccupied = false;
        return true;
    }
}
public class Ticket
{
    public string Id { get; set; }
    public Vehicle Vehicle { get; set; }
    public ParkingSpace ParkingSpace { get; set; }
    public DateTime EntryTime { get; set; }
    public TicketStatus Status { get; set; } = TicketStatus.Active;
    public DateTime ExitTime { get; set; }
    public double Amount { get; set; }
    public TicketStatus status { get; set; }
    public long GetDurationInMinutes()
    {
        return (long)(ExitTime - EntryTime).TotalMinutes;
    }
}

public interface IPricingStrategy
{
    double CalculateFee(Ticket ticket);
}

interface ISlotSelectionStrategy
{
    ParkingSpace SelectSlot(Vehicle vehicle, ParkingLot parkingLot);
}
public class HourlyPricingStrategy : IPricingStrategy
{
    private double hourlyRate;
    public HourlyPricingStrategy(double hourlyRate)
    {
        this.hourlyRate = hourlyRate;
    }
    public double CalculateFee(Ticket ticket)
    {
        long durationInMinutes = ticket.GetDurationInMinutes();
        return Math.Ceiling(durationInMinutes / 60.0) * hourlyRate;
    }
}

interface IParkingObserver
{
    void Update(ParkingLot parkingLot);
}

public class DisplayBoard : IParkingObserver
{
    public void Update(ParkingLot parkingLot)
    {
        Console.WriteLine($"Parking Lot: {parkingLot.Name}, Available Spaces: {parkingLot.GetAvailableSpaces()}");
    }
}


    public bool UnparkVehicle(Ticket ticket, IPricingStrategy pricingStrategy, out double fee)
    {
        fee = 0;
        if (ticket == null || ticket.Status != TicketStatus.Active)
            return false;
        ticket.ExitTime = DateTime.Now;
        fee = pricingStrategy.CalculateFee(ticket);
        ticket.Amount = fee;
        ticket.Status = TicketStatus.Paid;
        ticket.ParkingSpace.UnparkVehicle();
        NotifyObservers();
        return true;
    }
}

public class EntryGate
{
    public string Id { get; set; }
    public ParkingLot ParkingLot { get; set; }
    public ISlotSelectionStrategy SlotSelectionStrategy { get; set; }
    public EntryGate(string id, ParkingLot parkingLot, ISlotSelectionStrategy slotSelectionStrategy)
    {
        Id = id;
        ParkingLot = parkingLot;
        SlotSelectionStrategy = slotSelectionStrategy;
    }
    public bool ParkVehicle(Vehicle vehicle, out Ticket ticket)
    {
        return ParkingLot.ParkVehicle(vehicle, SlotSelectionStrategy, out ticket);
    }

    public bool UnparkVehicle(Ticket ticket, IPricingStrategy pricingStrategy, out double fee)
    {
        return ParkingLot.UnparkVehicle(ticket, pricingStrategy, out fee);
    }
    public Ticket GenrateTicket(Vehicle vehicle)
    {
        if (ParkVehicle(vehicle, out Ticket ticket))
            return ticket;
        return null;
    }
   

}

public class ExitGate
{
    public string Id { get; set; }
    public ParkingLot ParkingLot { get; set; }
    public ExitGate(string id, ParkingLot parkingLot)
    {
        Id = id;
        ParkingLot = parkingLot;
    }
    public bool UnparkVehicle(Ticket ticket, IPricingStrategy pricingStrategy, out double fee)
    {
        return ParkingLot.UnparkVehicle(ticket, pricingStrategy, out fee);
    }
}

public class NearestSlotSelectionStrategy : ISlotSelectionStrategy
{
    public ParkingSpace SelectSlot(Vehicle vehicle, ParkingLot parkingLot)
    {
        return parkingLot.ParkingSpaces
            .Where(ps => !ps.IsOccupied && IsCompatible(ps, vehicle))
            .OrderBy(ps => ps.Id) // Assuming Id can be used to determine proximity
            .FirstOrDefault();
    }
    private bool IsCompatible(ParkingSpace space, Vehicle vehicle)
    {
        switch (vehicle.Type)
        {
            case VehicleType.Car:
                return space.Type == SlotType.Compact || space.Type == SlotType.Regular;
            case VehicleType.Motorcycle:
                return space.Type == SlotType.Compact;
            case VehicleType.Truck:
                return space.Type == SlotType.Large;
            default:
                return false;
        }
    }
}

public class ParkingLot
{
    public string Name { get; set; }
    public List<ParkingSpace> ParkingSpaces { get; set; }
    private List<IParkingObserver> observers = new List<IParkingObserver>();
    public ParkingLot(string name, List<ParkingSpace> parkingSpaces)
    {
        Name = name;
        ParkingSpaces = parkingSpaces;
    }
    public void RegisterObserver(IParkingObserver observer)
    {
        observers.Add(observer);
    }
    public void UnregisterObserver(IParkingObserver observer)
    {
        observers.Remove(observer);
    }
    private void NotifyObservers()
    {
        foreach (var observer in observers)
        {
            observer.Update(this);
        }
    }
    public int GetAvailableSpaces()
    {
        return ParkingSpaces.Count(ps => !ps.IsOccupied);
    }

    public bool ParkVehicle(Vehicle vehicle, ISlotSelectionStrategy slotSelectionStrategy, out Ticket ticket)
    {
        ticket = null;
        var slot = slotSelectionStrategy.SelectSlot(vehicle, this);
        if (slot == null || !slot.ParkVehicle(vehicle))
            return false;
        ticket = new Ticket
        {
            Id = Guid.NewGuid().ToString(),
            Vehicle = vehicle,
            ParkingSpace = slot,
            EntryTime = DateTime.Now
        };
        NotifyObservers();
        return true;
    }
