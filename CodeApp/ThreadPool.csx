/*
 * 
 * Funtional requirements:
 * 
 * 1. 
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
using System.Threading;

public interface ITask
{
    void Execute();
}

public class ThreadPool : ITask
{
    private readonly Queue<ITask> _tasks = new Queue<ITask>();
    private readonly object _lock = new object();
    private bool _isRunning = false;
    public void Enqueue(ITask task)
    {
        lock (_lock)
        {
            _tasks.Enqueue(task);
            if (!_isRunning)
            {
                _isRunning = true;
                ThreadPool.QueueUserWorkItem(ProcessTasks);
            }
        }
    }
    private void ProcessTasks(object state)
    {
        while (true)
        {
            ITask task;
            lock (_lock)
            {
                if (_tasks.Count == 0)
                {
                    _isRunning = false;
                    return;
                }
                task = _tasks.Dequeue();
            }
            task.Execute();
        }
    }
}

