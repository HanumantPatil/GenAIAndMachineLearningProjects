// Builder Design Pattern Example

using System;

public class ImmutableToy
{
    public string Model { get; }
    public string Head { get; }
    // Internal constructor accessible to builder
    internal ImmutableToy(string model, string head)
    {
        Model = model;
        Head = head;
    }
}

public class ToyBuilder
{
    private string _model, _head;

    public ToyBuilder SetModel(string model)
    {
        this._model = model;
        return this;
    }

    public ToyBuilder SetHead(string head)
    {
        this._head = head;
        return this;
    }

    public ImmutableToy Build()
    {
        return new ImmutableToy(_model, _head);
    }
}

// Usage 
var toy = new ToyBuilder().SetModel("HP").SetHead("HP Head").Build();

Console.WriteLine($"Toy Model: {toy.Model}, Head: {toy.Head}");