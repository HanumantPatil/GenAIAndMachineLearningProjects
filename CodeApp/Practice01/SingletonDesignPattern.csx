
using System;

class Logger
{
    private static Logger _instance;
    private Logger() { }

    public static Logger GetLoggerInstance()
    {
        if (_instance == null)
        {
            Console.WriteLine("Creating new instance of Logger");
            _instance = new Logger();
        }
        return _instance;
    }

}
// run the code dotnet script Practice01\SingletonDesignPattern.csx

Logger.GetLoggerInstance();

class ThreadSafeSingleton
{
    private static ThreadSafeSingleton _instance;
    private static readonly object _lock = new object();

    private ThreadSafeSingleton() { }
    public static ThreadSafeSingleton GetInstance()
    {
        if (_instance == null)
        {
            lock (_lock)
            {
                if (_instance == null)
                {
                    Console.WriteLine("Creating new instance of ThreadSafeSingleton");
                    _instance = new ThreadSafeSingleton();
                }
            }
        }
        return _instance;
    }
}

// Call the thread safe singleton with multiple threads to see the effect
for (int i = 0; i < 1000; i++)
{
    // Create multiple threads to call the GetInstance method

    ThreadSafeSingleton.GetInstance();
}


class EagerSingleton
{
    private static readonly EagerSingleton _instance = new EagerSingleton();
    private EagerSingleton() { }
    public static EagerSingleton GetInstance()
    {
        Console.WriteLine("Returning instance of EagerSingleton");
        return _instance;
    }
}

// Call the eager singleton
EagerSingleton.GetInstance();

class BillPughSingleton
{
    private BillPughSingleton() { }
    private static class SingletonHelper
    {
        internal static readonly BillPughSingleton _instance = new BillPughSingleton();
    }
    public static BillPughSingleton GetInstance()
    {
        Console.WriteLine("Returning instance of BillPughSingleton");
        return SingletonHelper._instance;
    }
}

// Call the BillPughSingleton

BillPughSingleton.GetInstance();