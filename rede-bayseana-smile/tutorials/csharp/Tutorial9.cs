using System;
using System.Collections.Generic;
using Smile;

// Tutorial9 loads HeparII.xdsl file
// and runs multiple diagnostic algorithms
// Use the link below to download the HeparII.xdsl file:
// https://support.bayesfusion.com/docs/Examples/Discrete%20Bayesian%20Networks/HeparII.xdsl

namespace SmileNetTutorial
{
    class Tutorial9
    {
        public static void Run()
        {
            Console.WriteLine(System.IO.Directory.GetCurrentDirectory());
            Console.WriteLine("Starting Tutorial9...");
            Network net = new Network();
            net.ReadFile("HeparII.xdsl");
            Console.WriteLine("Hepar model loaded");
            PrintDiagTypes(net);

            Console.WriteLine("Creating diagnostic network object");
            DiagNetwork diag = new DiagNetwork(net);
            PrintFaultIndices(diag);

            int pursuedFaultIdx = diag.GetPursuedFault();
            Console.WriteLine("The default (most likely) pursued fault is at index {0}: {1}={2}", 
                pursuedFaultIdx,
                diag.GetFaultNodeId(pursuedFaultIdx), diag.GetFaultOutcomeId(pursuedFaultIdx));

            Console.WriteLine("Running diagnosis with no instantiated observations");
            DiagResults diagResults = diag.Update();
            PrintDiagResults(net, diagResults);

            Console.WriteLine("Running diagnosis with three observations");
            diag.InstantiateObservation("jaundice", "present");
            diag.InstantiateObservation("nausea", "absent");
            diag.InstantiateObservation("obesity", "present");
            diagResults = diag.Update();
            PrintDiagResults(net, diagResults);

            Console.WriteLine("Running diagnosis with two observations and " 
                + "focusing on Hyperbilirubinemia");
            diag.ReleaseObservation("nausea");
            diag.InstantiateObservation("obesity", "absent");
            int hyperbilirubinemiaIdx = diag.GetFaultIndex("Hyperbilirubinemia", "present");
            diag.SetPursuedFault(hyperbilirubinemiaIdx);
            diagResults = diag.Update();
            PrintDiagResults(net, diagResults);

            Console.WriteLine("Switching algorithm to cross-entropy, "
                + "observations and pursued fault unchanged");
            diag.SingleFaultAlgorithm = DiagNetwork.SingleFaultAlgorithmType.Crossentropy;
            diagResults = diag.Update();
            PrintDiagResults(net, diagResults);

            Console.WriteLine("Running diagnosis with two observations and " 
                + "focusing on both Hyperbilirubinemia and Steatosis");
            int steatosisIdx = diag.GetFaultIndex("Steatosis", "present");
            diag.SetPursuedFaults(new int[] { steatosisIdx, hyperbilirubinemiaIdx });
            diagResults = diag.Update();
            PrintDiagResults(net, diagResults);

            Console.WriteLine("Swtiching algorithm to L2 distance, "
                + "observations and pursued faults unchanged");
            diag.MultiFaultAlgorithm = DiagNetwork.MultiFaultAlgorithmType.L2NormalizedDistance;
            diagResults = diag.Update();
            PrintDiagResults(net, diagResults);

            Console.WriteLine("Tutorial9 complete.");
        }

        public static void PrintDiagTypes(Network net)
        {
            Console.WriteLine("Network has {0} nodes", net.GetNodeCount());
            Console.WriteLine("{0,-20} {1,-30} {2,-30}", 
                "Node Id", "Diagnostic Type", "Fault Outcomes");
            string[] nodeIds = net.GetAllNodeIds();
            foreach (string nodeId in nodeIds)
            {
                Network.NodeDiagType diagType = net.GetNodeDiagType(nodeId);
                List<string> faultOutcomes = new List<string>();
                if (diagType == Network.NodeDiagType.Fault)
                {
                    foreach (string outcomeId in net.GetOutcomeIds(nodeId))
                    {
                        if (net.IsFaultOutcome(nodeId, outcomeId))
                        {
                            faultOutcomes.Add(outcomeId);
                        }
                    }
                }
                Console.WriteLine("{0,-20} {1,-30} {2,-30}", nodeId, diagType,
                    (faultOutcomes.Count != 0) ? string.Join(", ", faultOutcomes) : "n/a");
            }
        }

        public static void PrintFaultIndices(DiagNetwork diag)
        {
            int faultCount = diag.FaultCount;
            Console.WriteLine("Diagnostic network has {0} faults (node/outcome pairs)", 
                faultCount);
            Console.WriteLine("{0,-12} {1,-20} {2,-20}", 
                "Fault Index", "Fault Node Id", "Fault Outcome Id");
            for (int fIdx = 0; fIdx < faultCount; fIdx++)
            {
                Console.WriteLine("{0,-12} {1,-20} {2,-20}", fIdx, 
                    diag.GetFaultNodeId(fIdx), diag.GetFaultOutcomeId(fIdx));
            }
        }

        public static void PrintFaultInfo(Network net, FaultInfo fault)
        {
            Console.WriteLine("{0,-20} {1,-20} {2,-24} {3,-8}", 
                net.GetNodeId(fault.Node), net.GetOutcomeId(fault.Node, fault.Outcome), 
                fault.Probability, fault.IsPursued ? "Yes" : "No");
        }

        public static void PrintObservationInfo(Network net, ObservationInfo observation)
        {
            Console.WriteLine("{0,-20} {1,-24} {2,-8} {3,-20}", 
                net.GetNodeId(observation.Node), observation.Measure,
                observation.Cost, observation.InfoGain);
        }

        public static void PrintDiagResults(Network net, DiagResults diagResults)
        {
            Console.WriteLine("Diag results start\n\nFaults:");
            Console.WriteLine("{0,-20} {1,-20} {2,-24} {3,-8}", 
                "Node Id", "Outcome Id", "Probability", "Is Pursued");
            foreach (FaultInfo faultInfo in diagResults.Faults)
            {
                PrintFaultInfo(net, faultInfo);
            }
            Console.WriteLine("\nObservations:");
            Console.WriteLine("{0,-20} {1,-24} {2,-8} {3,-20}", 
                "Node Id", "Measure", "Cost", "InfoGain");
            foreach (ObservationInfo observationInfo in diagResults.Observations)
            {
                PrintObservationInfo(net, observationInfo);
            }
            Console.WriteLine("\nDiag results end\n");
        }
    }
}
