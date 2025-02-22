using System;
using MQTTnet;
using MQTTnet.Client;
using MQTTnet.Client.Options;
using System.Text;
using System.Threading.Tasks;

class Program
{
    private static IMqttClient _mqttClient;
    
    static async Task Main(string[] args)
    {
        var factory = new MqttFactory();
        _mqttClient = factory.CreateMqttClient();

        var options = new MqttClientOptionsBuilder()
            .WithClientId("SmartHomeClient")
            .WithTcpServer("broker.hivemq.com", 1883)
            .WithCleanSession()
            .Build();

        _mqttClient.UseConnectedHandler(async e =>
        {
            Console.WriteLine("Connected to MQTT Broker!");
            await _mqttClient.SubscribeAsync("home/devices/#");
        });

        _mqttClient.UseApplicationMessageReceivedHandler(e =>
        {
            string topic = e.ApplicationMessage.Topic;
            string payload = Encoding.UTF8.GetString(e.ApplicationMessage.Payload);
            Console.WriteLine($"Received message: {payload} on topic: {topic}");
        });

        await _mqttClient.ConnectAsync(options);
        Console.WriteLine("Press any key to exit...");
        Console.ReadKey();
    }
}
