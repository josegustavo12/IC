library(rSMILE)
source("License.R")

# Tutorial8 loads continuous model from the XDSL file written by Tutorial7,
# then adds discrete nodes to create a hybrid model. Inference is performed
# and model is saved to disk.

createCptNode = function(net, id, name, outcomes, xPos, yPos) {
    handle <- net$addNode(18, id)
    initialOutcomeCount <- net$getOutcomeCount(handle)
    count <- length(outcomes)
    net$setNodeName(handle, name)
    net$setNodePosition(handle, xPos, yPos, 85L, 55L)
    if (!is.null(outcomes)) {
        sapply(0:(initialOutcomeCount-1), 
            function(x) net$setOutcomeId(handle, x, outcomes[x+1]))
        if (initialOutcomeCount < count) {
            sapply(initialOutcomeCount:(count-1), 
                function(x) net$addOutcome(handle, outcomes[x+1]))
        }
    }

    return(handle)
}

showStats = function(net, nodeHandle) {
    nodeId <- net$getNodeId(nodeHandle)
    if (net$isEvidence(nodeHandle)) {
        v <- net$getContEvidence(nodeHandle)
        cat(sprintf("%s has evidence set (%g)\n", nodeId, v))
        return()
    }
    
    if (net$isValueDiscretized(nodeHandle)) {
        cat(sprintf("%s is discretized.\n", nodeId))
        iv <- net$getNodeEquationDiscretization(nodeHandle)
        bounds <- net$getNodeEquationBounds(nodeHandle)
        discBeliefs <- net$getNodeValue(nodeHandle)
        lo <- bounds[1]
        for(i in 0:(length(discBeliefs)-1)) {
            hi <- iv[[i+1]]$boundary
            cat(sprintf("\tP(%s in %g..%g)=%g\n", 
                nodeId, lo, hi, discBeliefs[i+1]))
            lo <- hi
        }
    } else {
        stats <- net$getNodeSampleStats(nodeHandle)
        cat(sprintf("%s: mean=%g stddev=%g min=%g max=%g\n", 
            nodeId, stats[1], stats[2], stats[3], stats[4]))
    }
}

updateAndShowStats = function(net) {
    net$updateBeliefs()
    nodes <- net$getAllNodes()
    for (h in nodes) {
        if(net$getNodeType(h) == net$NodeType$EQUATION) {
            showStats(net, h)
        } 
    }
    cat("\n")
}

cat("Starting Tutorial8...\n")
net <- Network()

net$readFile("tutorial7.xdsl")

createCptNode(net, "zone", "Climate Zone", c("Temperate", "Desert"), 60, 20)

toaHandle <- net$getNode("toa")
net$setNodeEquation(toaHandle, "toa=If(zone=\"Desert\",Normal(22,5),Normal(11,10))")

perceivedHandle <- createCptNode(net, "perceived", "Perceived Temperature", 
    c("Hot", "Warm", "Cold"), 60, 300)

net$addArc(toaHandle, perceivedHandle)

perceivedProbs = c( 0.00,
                    0.02,
                    0.98,
                    0.05,
                    0.15,
                    0.80,
                    0.10,
                    0.80,
                    0.10,
                    0.80,
                    0.15,
                    0.05,
                    0.98,
                    0.02,
                    0.00 )

net$setNodeDefinition(perceivedHandle, perceivedProbs)

net$setEvidence("zone", "Temperate")
cat("Results in temperate zone:\n")
updateAndShowStats(net)

net$setEvidence("zone", "Desert")
cat("Results in desert zone:\n")
updateAndShowStats(net)

net$writeFile("tutorial8.xdsl")

cat("Tutorial8 complete: Network written to tutorial8.xdsl\n")
