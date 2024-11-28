library(rSMILE)
source("License.R")

# Tutorial9 loads HeparII.xdsl file
# and runs multiple diagnostic algorithms
# Use the link below to download the HeparII.xdsl file:
# https://support.bayesfusion.com/docs/Examples/Discrete%20Bayesian%20Networks/HeparII.xdsl

printDiagTypes <- function(net) {
    cat(sprintf("Network has %d nodes\n", net$getNodeCount()))
    cat(sprintf("%-20s %-30s %-30s\n", "Node Id", "Diagnostic Type", "Fault Outcomes"))
    nodeIds <- net$getAllNodeIds()
    for (nodeId in nodeIds) {
        diagType <- net$getNodeDiagType(nodeId)
        faultOutcomes <- character()
        if (diagType == net$NodeDiagType$FAULT) {
            outcomeIds <- net$getOutcomeIds(nodeId)
            for (outcomeId in outcomeIds) {
                if (net$isFaultOutcome(nodeId, outcomeId)) {
                    faultOutcomes <- c(faultOutcomes, outcomeId)
                }
            }
        }
        cat(sprintf("%-20s %-30s %-30s\n",
            nodeId, as.character(net$getNodeDiagType(nodeId)), 
            ifelse(diagType == net$NodeDiagType$FAULT, 
                paste(faultOutcomes, collapse = ", "), "n/a")))
    }
}

printFaultIndices <- function(diag) {
    faultCount <- diag$getFaultCount()
    cat(sprintf("Diagnostic network has %d faults (node/outcome pairs)\n", faultCount))
    cat(sprintf("%-12s %-20s %-20s\n", "Fault Index", "Fault Node Id", "Fault Outcome Id"))
    for (fIdx in 0:(faultCount-1)) {
        cat(sprintf("%-12d %-20s %-20s\n", fIdx, diag
            $getFaultNodeId(fIdx), diag$getFaultOutcomeId(fIdx)))
    }
}

printFaultInfo <- function(net, fault) {
    cat(sprintf("%-20s %-20s %-24s %-8s\n", 
        net$getNodeId(fault$node), net$getOutcomeId(fault$node, fault$outcome), 
        fault$probability, ifelse(fault$isPursued, "Yes", "No")))
}

printObservationInfo <- function(net, observation) {
    cat(sprintf("%-20s %-24s %-8s %-20s\n", net$getNodeId(observation$node),
        observation$measure, observation$cost, observation$infoGain))
}

printDiagResults <- function(net, diagResults) {
    cat("\n-- Diag results start\n\nFaults:\n")
    cat(sprintf("%-20s %-20s %-24s %-8s\n", 
        "Node Id", "Outcome Id", "Probability", "Is Pursued"))
    for (faultInfo in diagResults$faults) {
        printFaultInfo(net, faultInfo)
    }
    cat("\nObservations:\n")
    cat(sprintf("%-20s %-24s %-8s %-20s\n", 
        "Node Id", "Measure", "Cost", "InfoGain"))
    for (observationInfo in diagResults$observations) {
        printObservationInfo(net, observationInfo)
    }
    cat("\nDiag results end\n")
}

cat("Starting Tutorial9\n")
net <- Network()
net$readFile("HeparII.xdsl")
cat("Hepar model loaded\n")
printDiagTypes(net)

cat("Creating diagnostic network object\n")
diag <- DiagNetwork(net)
printFaultIndices(diag)

pursuedFaultIdx <- diag$getPursuedFault()
cat(sprintf("The default (most likely) pursued fault is at index %d: %s=%s\n",
    pursuedFaultIdx, 
    diag$getFaultNodeId(pursuedFaultIdx), diag$getFaultOutcomeId(pursuedFaultIdx)))

cat("Running diagnosis with no instantiated observations\n")
diagResults <- diag$update() 
printDiagResults(net, diagResults)

cat("Running diagnosis with three observations\n")
diag$instantiateObservation("jaundice", "present")
diag$instantiateObservation("nausea", "absent")
diag$instantiateObservation("obesity", "present")
diagResults <- diag$update() 
printDiagResults(net, diagResults)

cat("Running diagnosis with two observations and focusing on Hyperbilirubinemia\n")
diag$releaseObservation("nausea")
diag$instantiateObservation("obesity", "absent")
hyperbilirubinemiaIdx <- diag$getFaultIndex("Hyperbilirubinemia", "present")
diag$setPursuedFault(hyperbilirubinemiaIdx) 
diagResults <- diag$update() 
printDiagResults(net, diagResults)

cat("Switching algorithm to cross-entropy, observations and pursued fault unchanged")
diag$setSingleFaultAlgorithm(diag$SingleFaultAlgorithmType$CROSSENTROPY)
diagResults <- diag$update() 
printDiagResults(net, diagResults)

cat("Running diagnosis with two observations", 
    "and focusing on both Hyperbilirubinemia and Steatosis\n")
steatosisIdx <- diag$getFaultIndex("Steatosis", "present")
diag$setPursuedFaults(c(steatosisIdx, hyperbilirubinemiaIdx))
diagResults <- diag$update() 
printDiagResults(net, diagResults)

cat("Swtiching algorithm to L2 distance, observations and pursued faults unchanged")
diag$setMultiFaultAlgorithm(diag$MultiFaultAlgorithmType$L2_NORMALIZED_DISTANCE)
diagResults <- diag$update() 
printDiagResults(net, diagResults)

cat("Tutorial9 complete.\n")
