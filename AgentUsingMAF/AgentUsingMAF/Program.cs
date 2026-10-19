using System;
using Azure.AI.Projects;
using Azure.Identity;
using Microsoft.Agents.AI;

AIAgent agent = new AIProjectClient(
        new Uri("https://pizza-agent001.services.ai.azure.com/api/projects/pizza-agent001-proj"),
        new AzureCliCredential())
    .AsAIAgent(
        model: "gpt-4o",
        instructions: "You are a friendly assistant. Keep your answers brief.");

Console.WriteLine(await agent.RunAsync("What is the largest city in India?"));
