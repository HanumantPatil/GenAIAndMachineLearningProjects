// See https://aka.ms/new-console-template for more information
using CodeApp;

// Test Adapter Design Pattern
var adapterPattern = new AdapterDesignPattern();
adapterPattern.Execute();

// test isSubSequence function
Console.WriteLine(isSubSequence("abc", "ahbgdc"));

Console.WriteLine("Hello, World!");

// what is complexity of the following function
// 
bool isSubSequence(string s , string t)
{
    int sLen = s.Length;
    int tLen = t.Length;
    if (sLen == 0) return true;
    if (tLen == 0) return false;
    int sIndex = 0;
    int tIndex = 0;
    while (tIndex < tLen)
    {
        if (s[sIndex] == t[tIndex])
        {
            sIndex++;
            if (sIndex == sLen)
            {
                return true;
            }
        }
        tIndex++;
    }
    return false;
}