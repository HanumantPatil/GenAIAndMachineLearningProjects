//2.Reverse a String(Two Pointers)
//Problem: Write a function that reverses a string in-place.
//Time Complexity: O(N)
// https://gemini.google.com/app/878813159e6466af?is_sa=1&is_sa=1&android-min-version=301356232&ios-min-version=322.0&campaign_id=bkws&utm_source=sem&utm_source=google&utm_medium=paid-media&utm_medium=cpc&utm_campaign=bkws&utm_campaign=2024enIN_gemfeb&pt=9008&mt=8&ct=p-growth-sem-bkws&gclsrc=aw.ds&gad_source=1&gad_campaignid=20357620749&gbraid=0AAAAApk5BhnfNmeB-7srvVOPsfbU2TEj9&gclid=CjwKCAiAlrXJBhBAEiwA-5pgwlPJAZozAmyXaPBaa3ltULg5zUdkqgfpZI5SVbFbRLJyfGI4grJPWxoCwq8QAvD_BwE

using System;

void ReverseString(char[] s)
{
    int left = 0;
    int right = s.Length - 1;

    while(left< right)
    {
        char temp = s[left];
        s[left++] = s[right];
        s[right--] = temp;
    }
}

// Example usage:
char[] s = { 'h', 'e', 'l', 'l', 'o' };
ReverseString(s);
Console.WriteLine(new string(s));

// Call the script 
// dotnet script DSA\ReverseStringTwoPointer.csx