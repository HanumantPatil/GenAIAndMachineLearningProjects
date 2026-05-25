//3.Valid Parentheses(Stacks)
//Problem: Given a string containing just the characters(, ), {, }, [and], determine if the input string is valid(properly closed and nested).
//Time Complexity: O(N)

using System;

public bool IsValid(string s)
{
    var stack = new Stack<char>();

    foreach (char c in s)
    {
        if (c == '(')
        {
            stack.Push(')');
        }
        else if (c == '{')
        {
            stack.Push('}');
        }
        else if (c == '[')
        {
            stack.Push(']');
        }
        else if(stack.Count== 0 || stack.Pop() != c)
        {
            return false;
        }
    }
    return stack.Count == 0;
}

// Example usage:
string s = "({[])";
bool result = IsValid(s);
Console.WriteLine($"Is the string valid? {result}");
// Return script command  dotnet script DSA\ValidParentheses.csx