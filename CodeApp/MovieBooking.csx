
/*
 * 
 * 
 * Functional requirements:
 *      1. Search for movie by city
 *      2. View Theatre and Show a movie is playing in
 *      3. View available seats for a show
 *      4. view avaible seats for a show
 *      5. Book a seat for a show
 *      6. make payment for the booking
 *      7. cancel a booking
 *      
 * Non-functional requirements:
 *      1. Double booking should not be allowed
 *      2. Idempotency for booking and payment(avoid duplicate processing)
 *      3. System should handle high concurrency
 *      4. System should be scalable to handle increasing load
 *   Core entitys:
 *   1. Movie
 *   2. Theatre
 *   3. Show
 *   4. Seat
 *   5. ShowSeat
 *   6. Booking
 *   7. seatstype
 *   8. Payment
 *   9. User
 *   10. Payment
 *   11. PaymentStatus
 *   
 *   
 *   API Endpoints:
 *   
 *   
 *      
 *      
 * 
 * 
 */


public class Movie
{
    public int Id { get; set; }
    public string Title { get; set; }
    public string Genre { get; set; }
    public int DurationMinutes { get; set; }
}

public class Theatre
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string City { get; set; }
    public List<Show> Shows { get; set; }
    public List<Seat> Seats { get; set; }
    public List<ShowSeat> ShowSeats { get; set; }
    public List<Screen> Screens { get; set; }
}

public class Show
{
    public int Id { get; set; }
    public Movie Movie { get; set; }
    public Theatre Theatre { get; set; }
    public DateTime StartTime { get; set; }
    public DateTime EndTime { get; set; }
    public List<ShowSeat> ShowSeats { get; set; }
}
public class Seat
{
    public int Id { get; set; }
    public string SeatNumber { get; set; }
    public SeatType Type { get; set; }
}
public class ShowSeat
{
    public int Id { get; set; }
    public Show Show { get; set; }
    public Seat Seat { get; set; }
    public bool IsBooked { get; set; }
    public double Price { get; set; } = 0;
}
public class Booking
{
    public int Id { get; set; }
    public User User { get; set; }
    public Show Show { get; set; }
    public List<ShowSeat> BookedSeats { get; set; }
    public Payment Payment { get; set; }
    public DateTime BookingTime { get; set; }
    public BookingStatus Status { get; set; }
    public Payment Payment { get; set; }
}
public enum BookingStatus
{
    Pending,
    Confirmed,
    Cancelled
}
public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
}
public class Screen
{
    public int Id { get; set; }
    public string ScreenName { get; set; } = string.Empty;
    public string ScreenDescription { get; set; }
    public string ScreenTitle { get; set; } = string.Empty;
    public Dictionary<SeatType, List<Seat>> SeatsByType { get; set; }
}

public enum SeatType
{
    Regular,
    Premium,
    VIP
}
public enum SeatStatus
{
    Available,
    Booked,
    Reserved
}
public enum PaymentStatus
{
    Pending,
    Completed,
    Failed,
    Refunded
}
public class Payment
{
    public int Id { get; set; }
    public double Amount { get; set; }
    public PaymentStatus Status { get; set; }
    public DateTime PaymentTime { get; set; }
}
public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
}

// Payment straterguy pattern
// Seat reservation straterguy pattern
// Factory pattern for creating different types of seats and payments
// Repository pattern for data access
// Service layer for business logic

public class SeatLock
{
    public int Id { get; set; }
    public int ShowSeatId { get; set; }
    public DateTime LockTime { get; set; }// TTL 
}

public class SeatLockService
{
    private readonly Dictionary<int, DateTime> _lockedSeats = new Dictionary<int, DateTime>();
    private readonly TimeSpan _lockDuration = TimeSpan.FromMinutes(5);
    private readonly object _lockObj = new object();
    public bool TryLockSeat(int showSeatId)
    {
        lock (_lockObj)
        {
            if (_lockedSeats.ContainsKey(showSeatId))
            {
                // Check if the lock has expired
                if (DateTime.UtcNow - _lockedSeats[showSeatId] > _lockDuration)
                {
                    // Lock has expired, remove it
                    _lockedSeats.Remove(showSeatId);
                }
                else
                {
                    // Seat is currently locked
                    return false;
                }
            }
            // Lock the seat
            _lockedSeats[showSeatId] = DateTime.UtcNow;
            return true;
        }
    }
    public void UnlockSeat(int showSeatId)
    {
        lock (_lockObj)
        {
            if (_lockedSeats.ContainsKey(showSeatId))
            {
                _lockedSeats.Remove(showSeatId);
            }
        }
    }
}

public class BookingService
{
    private readonly SeatLockService _seatLockService;
    public BookingService(SeatLockService seatLockService)
    {
        _seatLockService = seatLockService;
    }
    public bool BookSeats(int userId, int showId, List<int> seatIds)
    {
        // Try to lock all requested seats
        foreach (var seatId in seatIds)
        {
            if (!_seatLockService.TryLockSeat(seatId))
            {
                // If any seat cannot be locked, unlock all previously locked seats and return false
                foreach (var lockedSeatId in seatIds)
                {
                    _seatLockService.UnlockSeat(lockedSeatId);
                }
                return false;
            }
        }
        // Proceed with booking logic (e.g., create booking record, process payment, etc.)
        return true;
    }
}