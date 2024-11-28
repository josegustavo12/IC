library(rSMILE)
source("License.R")

# Tutorial3 loads the XDSL file and prints the information
# about the structure (nodes and arcs) and the parameters 
# (conditional probabilities of the nodes) of the network.

indexToCoords = function(index, dimSizes) {
    prod <- 1L
    coords <- integer(length=length(dimSizes))
    for (i in length(dimSizes):1) {
        coords[i] <- floor(index / prod) %% dimSizes[[i]]
        prod <- prod * dimSizes[[i]]
    }
    return(coords)
}

printCptMatrix = function(net, nodeHandle) {
    cpt <- net$getNodeDefinition(nodeHandle)
    parents <- net$getParents(nodeHandle)
    dimCount <- 1 + length(parents)
    
    dimSizes <- sapply(parents, function(x) net$getOutcomeCount(x))
    dimSizes[length(dimSizes)+1] <- net$getOutcomeCount(nodeHandle)
    
    for (elemIdx in 0:(length(cpt)-1)) {
        coords <- indexToCoords(elemIdx, dimSizes)
        outcome <- net$getOutcomeId(nodeHandle, coords[dimCount])
        cat("    P(", outcome, sep="");
        if (dimCount > 1) {
            cat(" | ")
            parentIds <- sapply(parents, function(x) net$getNodeId(x))
            outcomeIds <- sapply(1:length(parents), 
                function(x) net$getOutcomeId(parents[x], coords[x]))
            
            cat(paste(parentIds, outcomeIds, sep="=", collapse=","))
        }
        prob <- cpt[elemIdx + 1]
        cat(sprintf(")=%f\n", prob))
    }
}

printNodeInfo = function(net, nodeHandle) {
    cat(sprintf("Node id/name: %s/%s\n", 
        net$getNodeId(nodeHandle), 
        net$getNodeName(nodeHandle)))
    cat("  Outcomes: ")
    cat(paste(net$getOutcomeIds(nodeHandle), collapse=" "))
    cat("\n")
    
    parentIds <- net$getParentIds(nodeHandle)
    if (length(parentIds) > 0) {
        cat("  Parents: ")
        cat(paste(parentIds, collapse=" "))
        cat("\n")
    }
    
    childIds <- net$getChildIds(nodeHandle)
    if (length(childIds) > 0) {
        cat("  Children: ")
        cat(paste(childIds, collapse=" "))
        cat("\n")
    }
    
    printCptMatrix(net, nodeHandle)
}

cat("Starting Tutorial3...\n")
net <- Network()

# load the network created by Tutorial1
net$readFile("tutorial1.xdsl")

nodes <- net$getAllNodes()

for (h in nodes) {
    printNodeInfo(net, h)
}

cat("Tutorial3 complete.\n")
