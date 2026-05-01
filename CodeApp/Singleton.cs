namespace CodeApp;

/// <summary>
/// Thread-safe Singleton implementation using the Bill Pugh pattern.
/// This pattern leverages the CLR's guarantee that static constructors are thread-safe
/// and only executed once, providing lazy initialization without explicit locking.
/// </summary>
internal sealed class Singleton
{
    private Singleton()
    {
        // Private constructor prevents external instantiation
    }

    /// <summary>
    /// Gets the single instance of the Singleton class.
    /// Thread-safe and lazy-initialized via nested class.
    /// </summary>
    public static Singleton Instance => Nested.instance;

    /// <summary>
    /// Nested class for lazy initialization.
    /// The CLR guarantees that static constructors are executed only once
    /// and are thread-safe, making this pattern highly efficient.
    /// </summary>
    private static class Nested
    {
        // Explicit static constructor to tell C# compiler
        // not to mark type as beforefieldinit
        static Nested()
        {
        }

        internal static readonly Singleton instance = new();
    }
}
