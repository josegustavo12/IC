library(rSMILE)
source("License.R")

# Tutorial7 creates a network with three equation-based nodes
# performs the inference, then saves the model to disk.

createEquationNode = function(net, id, name, equation, loBound, 
                              hiBound, xPos, yPos) {
    handle <- net$addNode(net$NodeType$EQUATION, id)
    net$setNodeName(handle, name)
    net$setNodeEquation(handle, equation)
    net$setNodeEquationBounds(handle, loBound, hiBound)
    net$setNodePosition(handle, xPos, yPos, 85, 55)

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

setUniformIntervals = function(net, nodeHandle, count) {
    bounds <- net$getNodeEquationBounds(nodeHandle)
    lo <- bounds[1]
    hi <- bounds[2]
    
    iv <- lapply(rep("DiscretizationInterval", count), new)
    num <- 1
    for(i in iv) {
        i$id <- ""
        i$boundary <- lo + num * (hi - lo) / count
        num <- num + 1
    }
    net$setNodeEquationDiscretization(nodeHandle, iv)
}

updateAndShowStats = function(net) {
    net$updateBeliefs()
    nodes <- net$getAllNodes()
    for (h in nodes) {
        showStats(net, h)
    }
    cat("\n")
}

cat("Starting Tutorial7...\n")
net <- Network()

net$setOutlierRejectionEnabled(TRUE)

createEquationNode(net, "tra", "Return Air Temperature", 
    "tra=24", 23.9, 24.1, 280, 100)

createEquationNode(net, "u_d", "Damper Control Signal", 
    "u_d = Bernoulli(0.539)*0.8 + 0.2", 0, 1, 160, 100)

toa <- createEquationNode(net, "toa", "Outside Air Temperature", 
    "toa=Normal(11,15)", -10, 40, 60, 100)

# tra, toa and u_d are referenced in equation
# arcs are created automatically
tma <- createEquationNode(net, "tma", "Mixed Air Temperature", 
    "tma=toa*u_d+(tra-tra*u_d)", 10, 30, 110, 200)

setUniformIntervals(net, toa, 5)
setUniformIntervals(net, tma, 4)

cat("Results with no evidence:\n")
updateAndShowStats(net)

net$setContEvidence(toa, 28.5)
cat("Results with outside air temperature set to 28.5:\n")
updateAndShowStats(net)

net$clearEvidence(toa)
cat("Results with mixed air temperature set to 21:\n")
net$setContEvidence(tma, 21.0)
updateAndShowStats(net)

net$writeFile("tutorial7.xdsl")
cat("Tutorial7 complete: Network written to tutorial7.xdsl\n")
