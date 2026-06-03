
// get(Key)
// Put(Key, Value)


using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Concurrent;
using System.Collections.Generic;


public class LRUCache
{
    private int capacity;
    private Dictionary<int, LinkedListNode<CacheItem>> cacheMap;
    private LinkedList<CacheItem> lruList;
    public LRUCache(int capacity)
    {
        this.capacity = capacity;
        this.cacheMap = new Dictionary<int, LinkedListNode<CacheItem>>();
        this.lruList = new LinkedList<CacheItem>();
    }
    public int Get(int key)
    {
        if (cacheMap.ContainsKey(key))
        {
            var node = cacheMap[key];
            lruList.Remove(node);
            lruList.AddFirst(node);
            return node.Value.Value;
        }
        return -1; // Not found
    }
    public void Put(int key, int value)
    {
        if (cacheMap.ContainsKey(key))
        {
            var node = cacheMap[key];
            node.Value.Value = value;
            lruList.Remove(node);
            lruList.AddFirst(node);
        }
        else
        {
            if (cacheMap.Count >= capacity)
            {
                var lastNode = lruList.Last;
                cacheMap.Remove(lastNode.Value.Key);
                lruList.RemoveLast();
            }
            var newNode = new LinkedListNode<CacheItem>(new CacheItem { Key = key, Value = value });
            lruList.AddFirst(newNode);
            cacheMap[key] = newNode;
        }
    }
    private class CacheItem
    {
        public int Key { get; set; }
        public int Value { get; set; }
    }
}

// access lru cache from multiple threads
public class ThreadSafeLRUCache
{
    private readonly LRUCache _lruCache;
    private readonly object _lock = new object();
    public ThreadSafeLRUCache(int capacity)
    {
        _lruCache = new LRUCache(capacity);
    }
    public int Get(int key)
    {
        lock (_lock)
        {
            return _lruCache.Get(key);
        }
    }
    public void Put(int key, int value)
    {
        lock (_lock)
        {
            _lruCache.Put(key, value);
        }
    }
}

// Example usage
var cache = new ThreadSafeLRUCache(2);
cache.Put(1, 1);
cache.Put(2, 2);

// command to run the code in the terminal
cache.Put(3, 3);
// dotnet script LRU_Cache.csx

// get elevates 2 to most recently used
