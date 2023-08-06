def printit():
    print("""
    
    
    
    #include "ns3/core-module.h"
    #include "ns3/network-module.h"
    #include "ns3/internet-module.h"
    #include "ns3/point-to-point-module.h"
    #include "ns3/applications-module.h"
    #include "ns3/csma-module.h"
    #include "ns3/network-application-helper.h"
    
    using namespace ns3;
    
    NS_LOG_COMPONENT_DEFINE ("3rd Lab Program");
    
    int 
    main (int argc, char *argv[])
    {
      CommandLine cmd;
      cmd.Parse (argc, argv);
      
      NS_LOG_INFO ("Create nodes");
      NodeContainer c;
      c.Create (4);
    
      CsmaHelper csma;
      csma.SetChannelAttribute ("DataRate", StringValue ("5Mbps"));
      csma.SetChannelAttribute ("Delay", TimeValue (MilliSeconds (0.0001)));
    
      NetDeviceContainer devs;
      devs = csma.Install (c);
    
      Ptr<RateErrorModel> em = CreateObject<RateErrorModel> ();
      em->SetAttribute ("ErrorRate", DoubleValue (0.00001));
      devs.Get (1)->SetAttribute ("ReceiveErrorModel", PointerValue (em));
    
      InternetStackHelper ipstack;
      ipstack.Install (c);
    
      Ipv4AddressHelper ip;
      ip.SetBase ("10.1.1.0", "255.255.255.0");
      Ipv4InterfaceContainer addresses = ip.Assign (devs);
    
      uint16_t port = 8080;
    
      Address sinkAddress (InetSocketAddress (addresses.GetAddress (1), port));
      PacketSinkHelper sink ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), port));
    
      ApplicationContainer apps = sink.Install (c.Get (1));
      apps.Start (Seconds (0.));
      apps.Stop (Seconds (20.));
    
      Ptr<Socket> ns3TcpSocket = Socket::CreateSocket (c.Get (0), TcpSocketFactory::GetTypeId ());
      ns3TcpSocket->TraceConnectWithoutContext ("CongestionWindow", MakeCallback (&CwndChange));
    
      Ptr<NetworkApplication> app = CreateObject<NetworkApplication> ();
      app->Setup (ns3TcpSocket, sinkAddress, 1040, 1000, DataRate ("50Mbps"));
      c.Get (0)->AddApplication (app);
      app->SetStartTime (Seconds (1.));
      app->SetStopTime (Seconds (20.));
    
      devs.Get (1)->TraceConnectWithoutContext ("PhyRxDrop", MakeCallback (&RxDrop));
    
      AsciiTraceHelper ascii;
      csma.EnableAsciiAll (ascii.CreateFileStream ("3lan.tr"));
      csma.EnablePcapAll (std::string ("3lan"), true);
    
      Simulator::Stop (Seconds (20));
      Simulator::Run ();
      Simulator::Destroy ();
    
      return 0;
    }
    
    
    
    """)