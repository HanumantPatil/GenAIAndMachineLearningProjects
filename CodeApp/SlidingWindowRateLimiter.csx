
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Concurrent;


public interface IRateLimiter
{
    bool IsAllowed(int userId);
}

class SlidingWindowRateLimiter: IRateLimiter
{
    private readonly int _maxRequests;
    private readonly TimeSpan _windowSize;
    private readonly ConcurrentDictionary<int, Queue<DateTime>> _userRequestTimestamps;

    // Helper class for common window sizes
    public static class Windows
    {
        public static readonly TimeSpan OneSecond = TimeSpan.FromSeconds(1);
        public static readonly TimeSpan OneMinute = TimeSpan.FromMinutes(1);
        public static readonly TimeSpan OneHour = TimeSpan.FromHours(1);
    }

    public SlidingWindowRateLimiter(int maxRequests, TimeSpan windowSize)
    {
        _maxRequests = maxRequests;
        _windowSize = windowSize;
        _userRequestTimestamps = new ConcurrentDictionary<int, Queue<DateTime>>();
    }

    public bool IsAllowed(int userId)
    {
        var now = DateTime.UtcNow;
        var windowStart = now - _windowSize;
        var timestamps = _userRequestTimestamps.GetOrAdd(userId, new Queue<DateTime>());
        lock (timestamps)
        {
            // Remove timestamps that are outside the current window
            while (timestamps.Count > 0 && timestamps.Peek() < windowStart)
            {
                timestamps.Dequeue();
            }
            if (timestamps.Count < _maxRequests)
            {
                timestamps.Enqueue(now);
                return true;
            }
            else
            {
                return false;
            }
        }
    }
}

// Example usage - 5 requests per 5 seconds window
var rateLimiter = new SlidingWindowRateLimiter(5, TimeSpan.FromSeconds(5));

Console.WriteLine("Sliding Window Rate Limiter Demo");
Console.WriteLine("Limit: 5 requests per 5 seconds");
Console.WriteLine("=====================================");

// Simulate requests
for (int i = 1; i <= 10; i++)
{
    bool allowed = rateLimiter.IsAllowed(1); // User ID 1
    Console.WriteLine($"Request {i}: {(allowed ? "✓ Allowed" : "✗ Denied")}");
    Thread.Sleep(500); // Wait 0.5 seconds between requests
}

Console.WriteLine("\nNote: After 5 seconds, old requests slide out of the window and new requests are allowed.");

// dotnet script SlidingWindowRateLimiter.csx
