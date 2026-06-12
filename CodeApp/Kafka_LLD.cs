using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


/*
 * 
 * Funtional requirements:
 * 
 * 1. Broker
 * 2. Topic
 * 3. Partition
 * 4. Producer
 * 5. Consumer
 * 6. Message
 * 7. Offset
 * 8. Worker
 * 
 * Producer features:
 * - produce publish messages to a topic
 * - messages are appended sequentially to the end of the topic's log
 * features of a topic:
 * - create topic with a specified number of partitions
 * - topic contains multiple partitions, each partition is an ordered, immutable sequence of messages that is continually appended to 
 * - messages in the partitions are assigned a sequential id number called the offset that uniquely identifies each message within the partition
 * 
 * Cosumer features:
 * - subscribe to one or more topics and consume published messages
 * - 
 * 
 * producer
 * cosumer
 * topic
 * partition
 * 
 * 
 */
namespace CodeApp
{
    public class Message
    {
        public string Key { get; set; }
        public string Value { get; set; }
        public DateTimeOffset Timestamp { get; set; }
    }
    public class Partition
    {
        public int Id { get; set; }
        public List<Message> Messages { get; set; }

        void AddMessage(Message message)
        {
            Messages.Add(message);
        }
    }
    public class Topic
    {
        public string Name { get; set; }
        public List<Partition> Partitions { get; set; }
        void CreateTopic(string name, int numPartitions)
        {
            Name = name;
            Partitions = new List<Partition>();
            for (int i = 0; i < numPartitions; i++)
            {
                Partitions.Add(new Partition { Id = i, Messages = new List<Message>() });
            }
        }
    }

    public class Broker
    {
        public string Name { get; set; }
        public List<Topic> Topics { get; set; }
        void CreateBroker(string name)
        {
            Name = name;
            Topics = new List<Topic>();
        }
        void AddTopic(Topic topic)
        {
            Topics.Add(topic);
        }

    }



    internal class Kafka_LLD
    {
    }
}
