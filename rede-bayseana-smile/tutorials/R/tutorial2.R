library(rSMILE)
source("License.R")

printPosteriors = function(net, nodeHandle) {
    nodeId <- net$getNodeId(nodeHandle)
    if (net$isEvidence(nodeHandle)) {
        cat(sprintf("%s has evidence set (%s)\n", 
            nodeId, 
            net$getOutcomeId(nodeHandle, net$getEvidence(nodeHandle))))
     
    } else {
        posteriors <- net$getNodeValue(nodeHandle)
        for (i in 0:(length(posteriors)-1)) {
            cat(sprintf("P(%s=%s)=%f\n", 
                nodeId, net$getOutcomeId(nodeHandle, i),posteriors[i+1]))
        }
    }
}

printAllPosteriors = function(net) {
    nodes <- net$getAllNodes()
    for (h in nodes) {
        printPosteriors(net, h)
    }
    cat("\n")
}

changeEvidenceAndUpdate = function(net, nodeId, outcomeId) {
    if (is.null(outcomeId)) {
        net$clearEvidence(nodeId)
    } else {
        net$setEvidence(nodeId, outcomeId)
    }
    net$updateBeliefs()
    printAllPosteriors(net)
}

cat("Starting Tutorial2...\n")
net <- Network()

# load the network created by Tutorial1
net$readFile("tutorial1.xdsl")

cat("Posteriors with no evidence set:\n")
net$updateBeliefs()
printAllPosteriors(net)

cat("Setting Forecast=Good.\n");
changeEvidenceAndUpdate(net, "Forecast", "Good");

cat("Adding Economy=Up.\n");
changeEvidenceAndUpdate(net, "Economy", "Up");

cat("Changing Forecast to Poor, keeping Economy=Up.\n");
changeEvidenceAndUpdate(net, "Forecast", "Poor");

cat("Removing evidence from Economy, keeping Forecast=Poor.\n");
changeEvidenceAndUpdate(net, "Economy", NULL);

cat("Tutorial2 complete.\n");
