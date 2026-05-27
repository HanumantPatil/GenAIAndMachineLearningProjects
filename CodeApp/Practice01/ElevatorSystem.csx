// Question prompt: LLD Code for Elevator System for interview perspective simpler code covering system in c#


using System;

//This is a classic Low - Level Design(LLD) interview question.The goal here isn't to write production-ready,
//multithreaded hardware integration code, but rather to demonstrate your ability to use Object-Oriented Programming (OOP) principles,
//define clear states, and implement a logical scheduling algorithm.

//For a standard interview, the LOOK or SCAN algorithm is the expected approach.Instead of First-Come-First-Serve (which leads to the elevator jumping erratically),
//the elevator should continue in its current direction until all requests in that direction are fulfilled, then switch directions.

//Here is a simplified, interview - ready C# implementation using a single elevator to demonstrate the core logic.

//1.Enums and Models
//First, define the core states and data structures.

using System.Collections.Generic;
using System.Linq;
using System.Threading;

public enum Direction
{
    Up,
    Down,
    Idle
}

public class Request
{
    public int TargetFloor { get; set; }
    public Request(int targetFloor)
    {
        TargetFloor = targetFloor;
    }
}

//2.The Elevator Class(Core Logic)
//This class maintains its state and uses two SortedSet collections.SortedSet naturally orders our floor requests, 
//    making it perfect for the LOOK algorithm.The "Up" queue is sorted ascending (1, 2, 3), and 
//    the "Down" queue is sorted descending (10, 9, 8).

public class Elevator
{
    public int CurretFloor { get; private set; } = 0; // Satart at ground floor
    public Direction CurrentDirection { get; private set; } = Direction.Idle;

    // Up request sorted lowest to highest
    private readonly SortedSet<int> _upRequest -new SortedSet<int>();

    // Down request sorted highest to lowest using a custom comparer
    private readonly SortedSet<int> _downRequest = new SortedSet<int>(Comparer<int>.Create((x, y) => y.CompareTo(x)));

    public void AddRequest(Request request)
    {
        if (request.TargetFloor == CurretFloor)
        {
            Console.WriteLine($"Already on floor {CurretFloor}. No action needed.");
            return;
        }

    }

}

