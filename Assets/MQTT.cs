using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using HslCommunication.MQTT;
using System.Text;
using TMPro;

public class MQTT : MonoBehaviour
{

    public TMP_Text BridgePosition;
    public TMP_Text TrolleyPosition;
    public TMP_Text HoistPosition;
    public TMP_Text Load;
    public TMP_Text WatchDogStatus;
    public TMP_Text SwayStatus;
    public TMP_Text InchingStatus;
    public TMP_Text RopeAngleStatus;
    public TMP_Text MicroSpeedStatus;

    public string inching;
    public string microspeed;
    public string ropeanglefeaturesbypass;
    public string swaycontrol;
    public int swaycontrol_slinglength;
    public float hoist_position;
    public float bridge_position;
    public float trolley_position;
    public int test;

    private float minBridge = 0f;
    private float maxBridge = 19800f;
    private float minTrolley = 0f;
    private float maxTrolley = 9000f;
    private float minHook = 0.4f;
    private float maxHook = 4.35f;

    MqttClient mqttClient;
    public string IP;
    // Start is called before the first frame update


    void Start()
    {
        mqttClient = new MqttClient(new MqttConnectionOptions()
        {
            ClientId= "Unity",
            IpAddress= IP,
            Credentials=new MqttCredential("67b8aef0b3cf56e74edcccbe97612b2d", "mqtt"),
        });
        
    // connect to server
        HslCommunication.OperateResult connect=mqttClient.ConnectServer();
        if (connect.IsSuccess)
            Debug.Log("connect successful");
        else
            Debug.Log("connect failure");
        // add subscription
        //HslCommunication.OperateResult sub = mqttClient.SubscribeMessage("/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.Controls.Watchdog");
        HslCommunication.OperateResult Inching = mqttClient.SubscribeMessage("/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.RadioSelection.Inching");
        HslCommunication.OperateResult MicroSpeed = mqttClient.SubscribeMessage("/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.RadioSelection.MicroSpeed");
        HslCommunication.OperateResult RopeAngleFeaturesBypass = mqttClient.SubscribeMessage("/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.RadioSelection.RopeAngleFeaturesBypass");
        HslCommunication.OperateResult SwayControl = mqttClient.SubscribeMessage("/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.RadioSelection.SwayControl");
        HslCommunication.OperateResult SwayControl_SlingLength_mm = mqttClient.SubscribeMessage("/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.RadioSelection.SwayControl_SlingLength_mm");
        HslCommunication.OperateResult Hoist_Position = mqttClient.SubscribeMessage("/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.Status.Hoist.Position.Position_m");
        HslCommunication.OperateResult Bridge_Position = mqttClient.SubscribeMessage("/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.Status.Bridge.Position.Position_m");
        HslCommunication.OperateResult Trolley_Position = mqttClient.SubscribeMessage("/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.Status.Trolley.Position.Position_m");
        HslCommunication.OperateResult Test = mqttClient.SubscribeMessage("/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/2/2");
        //if (sub.IsSuccess)
        //{
        //    Debug.Log("subscribe successful");
        //}
        //else 
        //{
        //    Debug.Log("subscribe failure");
        //}
        mqttClient.OnMqttMessageReceived += (MqttClient client, string topic, byte[] payload) =>
        {
            if (topic == "/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.RadioSelection.Inching")
            { inching = Encoding.UTF8.GetString(payload); Debug.Log(1); }
            else if (topic == "/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.RadioSelection.MicroSpeed")
            {
                microspeed = Encoding.UTF8.GetString(payload); Debug.Log(2);
            }
            else if (topic == "/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.RadioSelection.RopeAngleFeaturesBypass")
            {
                ropeanglefeaturesbypass = Encoding.UTF8.GetString(payload); Debug.Log(3);
            }
            else if (topic == "/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.RadioSelection.SwayControl")
            {
                swaycontrol = Encoding.UTF8.GetString(payload); Debug.Log(4);
            }
            else if (topic == "/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.RadioSelection.SwayControl_SlingLength_mm")
            {
                swaycontrol_slinglength = int.Parse(Encoding.UTF8.GetString(payload)); Debug.Log(5);
            }
            else if (topic == "/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.Status.Hoist.Position.Position_m")
            {
                hoist_position = float.Parse(Encoding.UTF8.GetString(payload)); Debug.Log(6);
            }
            else if (topic == "/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.Status.Bridge.Position.Position_m")
            {
                bridge_position = float.Parse(Encoding.UTF8.GetString(payload)); Debug.Log(7);
            }
            else if (topic == "/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/7/SCF.PLC.DX_Custom_V.Status.Trolley.Position.Position_m")
            {
                trolley_position = float.Parse(Encoding.UTF8.GetString(payload)); Debug.Log(8);
            }
                if (topic == "/iot/1031/pub/67b8aef0b3cf56e74edcccbe97612b2d/2/2")
                {
                    test = int.Parse(Encoding.UTF8.GetString(payload)); Debug.Log(9);
            }


                //Debug.Log("Time:" + System.DateTime.Now.ToString());

                //Debug.Log("Payload:" + Encoding.UTF8.GetString(payload));
            };
        }

                                



                                    void Update()
                                    {
                                        //HslCommunication.OperateResult connect = mqttClient.PublishMessage(new MqttApplicationMessage()
                                        //{
                                        //    Topic = "/iot/1031/sub/67b8aef0b3cf56e74edcccbe97612b2d",                                                         // topic
                                        //    QualityOfServiceLevel = MqttQualityOfServiceLevel.AtMostOnce,           //  real-time data
                                        //    Payload = Encoding.UTF8.GetBytes("Test data")                          // publish data
                                        //});
                                        //if (connect.IsSuccess)
                                        //{
                                        //    //Debug.Log("publish successful");
                                        //}
                                        //else
                                        //{
                                        //    //Debug.Log("publish failure");
                                        //}

                                    }
                                }
