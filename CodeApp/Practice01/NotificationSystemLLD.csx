using System;
// Question prompt: LLD Code for Notification System for interview prespective simpler code covering system in c#


//For an LLD interview, the most important thing is demonstrating SOLID principles and the use of appropriate Design Patterns.
//This solution uses two primary patterns:

//Strategy Pattern: To handle different types of notifications (Email, SMS, Push) interchangeably.

//Factory Pattern: To instantiate the correct notification strategy without hardcoding dependencies in the main service.

// ==========================================
// 1. Models & Enums
// ==========================================

public enum NotificationType
{
    Email,
    SMS,
    Push
}

public class User
{
    public string Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public string PhoneNumber { get; set; } = string.Empty;
    public string DeviceToken { get; set; } = string.Empty;

}

public class NotificationRequest
{
    public User TargetUser { get; set; }
    public string Message { get; set; }
    public NotificationType Type { get; set; }
}

// Strategy Design Pattern
public interface INotificationSender
{
    void Send(User user, string message);
}

public class EmailSender : INotificationSender
{
    public void Send(User user, string message)
    {
        Console.WriteLine($"Sending Email to {user.Email}: {message}");
    }
}

public class SMSSender : INotificationSender
{
    public void Send(User user, string message)
    {
        Console.WriteLine($"Sending SMS to {user.PhoneNumber}: {message}");
    }
}

class PushSender : INotificationSender
{
    public void Send(User user, string message)
    {
        Console.WriteLine($"Sending Push Notification to {user.DeviceToken}: {message}");
    }
}

// Factory Design Pattern
public class NotificationFactory
{
    public INotificationSender GetSender(NotificationType type)
    {
        return type switch
        {
            NotificationType.Email => new EmailSender(),
            NotificationType.SMS => new SMSSender(),
            NotificationType.Push => new PushSender(),
            _ => throw new NotSupportedException("Notification type not supported")
        };
    }
}

// ==========================================
// 4. Notification Service (Facade / Core logic)
// ==========================================

public class NotificationService
{
    private readonly NotificationFactory _factory;

    // Dependency Injection of the factory
    public NotificationService(NotificationFactory factory)
    {
        _factory = factory;
    }

    public void SendNotification(NotificationRequest request)
    {
        try
        {
            // 1. Validate request (skipping for brevity)
            // 2. Get the correct sender strategy via the factory
            INotificationSender sender = _factory.GetSender(request.Type);

            // execute the sending logic
            sender.Send(request.TargetUser, request.Message);

            // 4. Log success to a database
        }
        catch (Exception ex)
        {
            // Handle exceptions (logging, retry mechanisms, etc.)
            Console.WriteLine($"Error sending notification: {ex.Message}");

            // 4. Log success to a database
        }
    }
}

// ==========================================
// 5. Client Execution
// ==========================================


// 1. Setup mock data
User user = new User
{
    Id = "AB:000001",
    Name = "John Doe",
    Email = "alice@example.com",
    PhoneNumber = "1234567890",
    DeviceToken = "device_token_123"
};

var fctory = new NotificationFactory();
var service = new NotificationService(fctory);


// 2. Create requests
var emailRequest = new NotificationRequest
{
    TargetUser = user,
    Message = "Hello via Email!",
    Type = NotificationType.Email
};

var smsRequest = new NotificationRequest
{
    TargetUser = user,
    Message = "Hello via SMS!",
    Type = NotificationType.SMS
};
var pushRequest = new NotificationRequest
{
    TargetUser = user,
    Message = "Hello via Push Notification!",
    Type = NotificationType.Push
};

// 3. Process requests
service.SendNotification(emailRequest);
service.SendNotification(smsRequest);
service.SendNotification(pushRequest);



// command to call the programpt: dotnet script Practice01\NotificationSystemLLD.csx