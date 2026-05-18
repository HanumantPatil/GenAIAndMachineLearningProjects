// PrototypeDesignPattern.csx
using System;


// The Prototype Design Pattern is a creational pattern used to create new objects by copying (or "cloning") an existing object,
// rather than creating them from scratch using the new keyword.

// A shallow copy duplicates the top-level structure of an object but keeps references to nested objects.
// This means changes to nested data affect both the original and the copy.A deep copy recursively duplicates all nested layers,
// creating a completely independent object where changes to the copy do not alter the original

// A reference type class to demonstrate the difference between Shallow and Deep copy
public class Weapon
{
    public string Name { get; set; }
    public Weapon(string name)
    {
        Name = name;
    }
}
// 1. the prototype interface that defines the cloning methods
public interface IMonsterPrototype
{
    IMonsterPrototype Clone();
    IMonsterPrototype DeepClone();
}

// 2. the Concrete prototype

public class Goblin : IMonsterPrototype
{
    public string Name { get; set; }
    public int Health { get; set; }
    public Weapon EquippedWeapon { get; set; }
    public Goblin(string name, int health, string weaponName)
    {
        Name = name;
        Health = health;
        EquippedWeapon = new Weapon(weaponName);
    }
    // Shallow copy: copies value types, but only copies references for reference types (like Weapon)
    public IMonsterPrototype Clone()
    {
        return (IMonsterPrototype)this.MemberwiseClone();
    }
    // Deep copy: creates a new instance of the reference type (Weapon) to ensure that the cloned object has its own copy

    public IMonsterPrototype DeepClone()
    {
        Goblin clonedGoblin = (Goblin)this.MemberwiseClone();
        clonedGoblin.EquippedWeapon = new Weapon(this.EquippedWeapon.Name);
        return clonedGoblin;
    }

    public void Display()
    {
        Console.WriteLine($"Goblin Name: {Name}, Health: {Health}, Equipped Weapon: {EquippedWeapon.Name}");
    }
}


// Create our original prototype
Goblin originalGoblin = new Goblin("Grimtooth", 100, "Rusty Sword");
Console.WriteLine("Original Goblin:");
originalGoblin.Display();

// Test 1: Shallow Copy
Goblin shallowclone = (Goblin)originalGoblin.Clone();
shallowclone.Name = "Shallow Clone Goblin";

// Change the weapon name in the shallow clone to see if it affects the original goblin
shallowclone.EquippedWeapon.Name = "Iron Dagger";

Console.WriteLine("\n ---- After Shallow Clone Modification ----");
Console.WriteLine("Notce how modifying the clones wepon also modified the originals weapon because they share the same reference:");

Console.WriteLine("Shallow Clone:");
shallowclone.Display();
Console.WriteLine("Original Goblin:");
originalGoblin.Display();

// Test 2: Deep Copy
Goblin deepClone = (Goblin)originalGoblin.DeepClone();
deepClone.Name = "Deep Clone Goblin";
// Change the weapon name in the deep clone to see if it affects the original goblin
deepClone.EquippedWeapon.Name = "Steel Axe";

Console.WriteLine("\n ---- After Deep Clone Modification ----");
Console.WriteLine("Notice how modifying the deep clone's weapon does not affect the original goblin's weapon:");

Console.WriteLine("Deep Clone:");
deepClone.Display();
Console.WriteLine("Original Goblin:");
originalGoblin.Display();


// Run the script
// dotnet script Practice01\PrototypeDesignPattern.csx