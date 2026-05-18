using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using System.Text;
using System.Threading.Tasks;

namespace CodeApp
{

    /// <summary>
    /// Design Pattern: Chain of Responsibility
    /// This pattern allows an object to pass a request along a chain of potential handlers until the request is handled.
    /// </summary>
    public interface ILevelHandler
    {
        void NextHandler(ILevelHandler handler);
        bool CanHandle(int level);
        void ProcessRequest(int level, string message);
    }

    public class LevelOneHandler : ILevelHandler
    {
        public bool CanHandle(int level)
        {
            throw new NotImplementedException();
        }

        public void NextHandler(ILevelHandler handler)
        {
            throw new NotImplementedException();
        }

        public void ProcessRequest(int level, string message)
        {
            throw new NotImplementedException();
        }
    }
    public class LevelTwoHandler : ILevelHandler
    {
        public bool CanHandle(int level)
        {
            throw new NotImplementedException();
        }

        public void NextHandler(ILevelHandler handler)
        {
            throw new NotImplementedException();
        }

        public void ProcessRequest(int level, string message)
        {
            throw new NotImplementedException();
        }
    }
    public class LevelThreeHandler : ILevelHandler
    {
        public bool CanHandle(int level)
        {
            throw new NotImplementedException();
        }

        public void NextHandler(ILevelHandler handler)
        {
            throw new NotImplementedException();
        }

        public void ProcessRequest(int level, string message)
        {
            throw new NotImplementedException();
        }
    }
    internal class SupportTicketSystem
    {
    }
}
