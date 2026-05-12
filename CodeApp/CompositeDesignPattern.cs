using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CodeApp
{
    // File, Folder 
    // 

    public interface IFileSystemItem
    {
        string GetSize();
        void ls();
    }
    public class File : IFileSystemItem
    {
        public string GetSize()
        {
            return "10KB";
        }
        public void ls()
        {
            Console.WriteLine("File");
        }
    }
    public class Folders : IFileSystemItem
    {
        public string GetSize()
        {
            return "100MB";
        }
        public void ls()
        {
            Console.WriteLine("Folder");
        }

    }
    internal class CompositeDesignPattern
    {
    }
}