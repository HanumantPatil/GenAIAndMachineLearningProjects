

//Problem: Given an array of integers and a target sum, return the indices of the two numbers that add up to the target.
//Time Complexity: O(N)

//1.Two Sum(Arrays & Hashing)
//Problem: Given an array of integers and a target sum, return the indices of the two numbers that add up to the target.
//Time Complexity: O(N)

using System;
using System.Collections.Generic;

public int[] TwoSum(int[] nums, int target)
{
    var map = new Dictionary<int, int>();
    for (int i = 0; i < nums.Length; i++)
    {
        int complement = target - nums[i];
        if (map.ContainsKey(complement))
        {
            return new int[] { map[complement], i };
        }
        map[nums[i]] = i; // Store value and its index 
    }
    return new int[0];
}

// Example usage:
int[] nums = { 2, 7, 11, 15 };
int target = 26;
int[] result = TwoSum(nums, target);
Console.WriteLine($"Indices: {result[0]}, {result[1]}");

// Output: Indices: 2, 3 (since nums[2] + nums[3] = 11 + 15 = 26)

// 