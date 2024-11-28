library(rSMILE)
source("License.R")

# Tutorial5 loads the XDSL file created by Tutorial4,
# then performs the series of inference calls,
# changing evidence each time.

indexToCoords = function(index, dimSizes) {
    prod <- 1L
    coords <- integer(length=length(dimSizes))
    for (i in length(dimSizes):1) {
        coords[i] <- floor(index / prod) %% dimSizes[[i]]
        prod <- prod * dimSizes[[i]]
    }
    return(coords)
}

printGainMatrix = function(net, mtx, parents) {
    dimCount <- 1 + length(parents)
    
    dimSizes <- sapply(parents, function(x) net$getOutcomeCount(x))
    dimSizes[length(dimSizes)+1] <- 1
    
    for (elemIdx in 0:(length(mtx)-1)) {
        coords <- indexToCoords(elemIdx, dimSizes)
        cat("    Utility(");
        if (dimCount > 1) {
            parentIds <- sapply(parents, function(x) net$getNodeId(x))
            outcomeIds <- sapply(1:length(parents), 
                function(x) net$getOutcomeId(parents[x], coords[x]))
            
            cat(paste(parentIds, outcomeIds, sep="=", collapse=","))
        }
        cat(sprintf(")=%f\n", mtx[elemIdx+1]))
    }
}

printFinancialGain = function(net) {
    expectedUtility <- net$getNodeValue("Gain")
    utilParents <- net$getValueIndexingParents("Gain")
    printGainMatrix(net, expectedUtility, utilParents)
}

changeEvidenceAndUpdate = function(net, nodeId, outcomeId) {
    if (!is.null(outcomeId)) {
        net$setEvidence(nodeId, outcomeId)
    } else {
        net$clearEvidence(nodeId)
    }
    net$updateBeliefs()
    printFinancialGain(net)
}

cat("Starting Tutorial5...\n")
net <- Network()

net$readFile("tutorial4.xdsl")

cat("No evidence set.\n")
net$updateBeliefs()
printFinancialGain(net)

cat("Setting Forecast=Good.\n")
changeEvidenceAndUpdate(net, "Forecast", "Good")

cat("Adding Economy=Up.\n")
changeEvidenceAndUpdate(net, "Economy", "Up")

cat("Tutorial5 complete.\n")
