
// 
using System;
using System.Threading;
using System.Collections.Generic;
using System.Linq;


public interface IRateLimiter
{
    bool IsAllowed(int userId);
}

class TokenBucket : IRateLimiter
{
    private class Bucket
    {
        public int Tokens { get; set; }
        public DateTime LastRefill { get; set; }
        public int Capacity { get; set; }

        public Bucket(int capacity)
        {
            Tokens = capacity;
            LastRefill = DateTime.UtcNow;
            Capacity = capacity;
        }
    }

    private Dictionary<string, Bucket> buckets = new Dictionary<string, Bucket>();
    private int capacity;
    private int refillRate;

    public TokenBucket(int capacity, int refillRate)
    {
        this.capacity = capacity;
        this.refillRate = refillRate;
    }

    public bool IsAllowed(int userId)
    {
        var now = DateTime.UtcNow;
        if (!buckets.ContainsKey(userId.ToString()))
        {
            buckets[userId.ToString()] = new Bucket(capacity);
        }
        var bucket = buckets[userId.ToString()];
        // Refill tokens based on elapsed time
        var elapsed = (now - bucket.LastRefill).TotalSeconds;
        var tokensToAdd = (int)(elapsed * refillRate);
        bucket.Tokens = Math.Min(bucket.Capacity, bucket.Tokens + tokensToAdd);
        bucket.LastRefill = now;
        // Check if there are tokens available
        if (bucket.Tokens > 0)
        {
            bucket.Tokens--;
            return true;
        }
        return false;
    }
}

// Example usage
var rateLimiter = new TokenBucket(5, 1); // 5 tokens capacity, 1 token per second refill
for (int i = 0; i < 10; i++)
{
    Console.WriteLine(rateLimiter.IsAllowed(1)); // User ID 1
    Thread.Sleep(500); // Wait for 0.5 seconds
}

// dotnet script RateLimiter.csx