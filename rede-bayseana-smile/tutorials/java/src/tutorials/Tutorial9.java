package tutorials;

import smile.*;

import java.util.ArrayList;
import java.util.List;

// Tutorial9 loads HeparII.xdsl file
// and runs multiple diagnostic algorithms
// Use the link below to download the HeparII.xdsl file:
// https://support.bayesfusion.com/docs/Examples/Discrete%20Bayesian%20Networks/HeparII.xdsl

public class Tutorial9 {
    public static void run() {
        System.out.println("Starting diagnosis example");
        Network net = new Network();
        net.readFile("HeparII.xdsl");
        System.out.println("Hepar model loaded");
        printDiagTypes(net);

        System.out.println("Creating diagnostic network object");
        DiagNetwork diag = new DiagNetwork(net);
        printFaultIndices(diag);

        int pursuedFaultIdx = diag.getPursuedFault();
        System.out.printf("The default (most likely) pursued fault is at index %d: %s=%s\n", 
            pursuedFaultIdx, diag.getFaultNodeId(pursuedFaultIdx), 
            diag.getFaultOutcomeId(pursuedFaultIdx));

        System.out.println("Running diagnosis with no instantiated observations");
        DiagResults diagResults = diag.update();
        printDiagResults(net, diagResults);

        System.out.println("Running diagnosis with three observations");
        diag.instantiateObservation("jaundice", "present");
        diag.instantiateObservation("nausea", "absent");
        diag.instantiateObservation("obesity", "present");
        diagResults = diag.update();
        printDiagResults(net, diagResults);

        System.out.println("Running diagnosis with two observations and "
            + "focusing on Hyperbilirubinemia");
        diag.releaseObservation("nausea");
        diag.instantiateObservation("obesity", "absent");
        int hyperbilirubinemiaIdx = diag.getFaultIndex("Hyperbilirubinemia", "present");
        diag.setPursuedFault(hyperbilirubinemiaIdx);
        diagResults = diag.update();
        printDiagResults(net, diagResults);

        System.out.println("Switching algorithm to cross-entropy, " 
            + "observations and pursued fault unchanged");
        diag.setSingleFaultAlgorithm(DiagNetwork.SingleFaultAlgorithmType.CROSSENTROPY);
        diagResults = diag.update();
        printDiagResults(net, diagResults);

        System.out.println("Running diagnosis with two observations and " 
            + "focusing on both Hyperbilirubinemia and Steatosis");
        int steatosisIdx = diag.getFaultIndex("Steatosis", "present");
        diag.setPursuedFaults(new int[]{steatosisIdx, hyperbilirubinemiaIdx});
        diagResults = diag.update();
        printDiagResults(net, diagResults);

        System.out.println("Swtiching algorithm to L2 distance, " 
            + "observations and pursued faults unchanged");
        diag.setMultiFaultAlgorithm(DiagNetwork.MultiFaultAlgorithmType.L2_NORMALIZED_DISTANCE);
        diagResults = diag.update();
        printDiagResults(net, diagResults);
                
        System.out.println("Tutorial9 complete.");
    }

    public static void printDiagTypes(Network net) {
        System.out.printf("Network has %d nodes\n", net.getNodeCount());
        System.out.printf("%-20s %-30s %-30s\n", 
            "Node Id", "Diagnostic Type", "Fault Outcomes");
        String[] nodeIds = net.getAllNodeIds();
        for (String nodeId : nodeIds) {
            int diagType = net.getNodeDiagType(nodeId);
            List<String> faultOutcomes = new ArrayList<>();
            if (diagType == Network.NodeDiagType.FAULT) {
                for (String outcomeId : net.getOutcomeIds(nodeId)) {
                    if (net.isFaultOutcome(nodeId, outcomeId)) {
                        faultOutcomes.add(outcomeId);
                    }
                }
            }
            System.out.printf("%-20s %-30s %-30s\n", nodeId, diagType,
                (faultOutcomes.size() != 0) ? String.join(", ", faultOutcomes) : "n/a");
        }
    }

    public static void printFaultIndices(DiagNetwork diag) {
        int faultCount = diag.getFaultCount();
        System.out.printf("Diagnostic network has %d faults (node/outcome pairs)\n",
            faultCount);
        System.out.printf("%-12s %-20s %-20s\n", 
            "Fault Index", "Fault Node Id", "Fault Outcome Id");
        for (int fIdx = 0; fIdx < faultCount; fIdx++) {
            System.out.printf("%-12d %-20s %-20s\n", 
                fIdx, diag.getFaultNodeId(fIdx), diag.getFaultOutcomeId(fIdx));
        }
    }

    public static void printFaultInfo(Network net, FaultInfo fault) {
        System.out.printf("%-20s %-20s %-24s %-8s\n", 
            net.getNodeId(fault.node), net.getOutcomeId(fault.node, fault.outcome), 
            fault.probability, fault.isPursued ? "Yes" : "No");
    }

    public static void printObservationInfo(Network net, ObservationInfo observation) {
        System.out.printf("%-20s %-24s %-8s %-20s\n", 
            net.getNodeId(observation.node), observation.measure,
            observation.cost, observation.infoGain);
    }

    public static void printDiagResults(Network net, DiagResults diagResults) {
        System.out.println("Diag results start\n\nFaults:");
        System.out.printf("%-20s %-20s %-24s %-8s\n", 
            "Node Id", "Outcome Id", "Probability", "Is Pursued");
        for (FaultInfo faultInfo : diagResults.faults) {
            printFaultInfo(net, faultInfo);
        }
        System.out.println("\nObservations:");
        System.out.printf("%-20s %-24s %-8s %-20s\n", 
            "Node Id", "Measure", "Cost", "InfoGain");
        for (ObservationInfo observationInfo : diagResults.observations) {
            printObservationInfo(net, observationInfo);
        }
        System.out.println("\nDiag results end\n");
    }
}
