library(rSMILE)
source("License.R")

# Tutorial6 creates a dynamic Bayesian network (DBN),
# performs the inference, then saves the model to disk.

createCptNode = function(net, id, name, outcomes, xPos, yPos) {
    handle <- net$addNode(net$NodeType$CPT, id)
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

updateAndShowTemporalResults = function(net) {
    net$updateBeliefs()
    sliceCount <- net$getSliceCount()
    handles <- net$getAllNodes()
    for (h in handles) {
        if (net$getNodeTemporalType(h) == net$NodeTemporalType$PLATE) {
            outcomeCount <- net$getOutcomeCount(h)
            cat(sprintf("Temporal beliefs for %s:\n", net$getNodeId(h)))
            v <- net$getNodeValue(h)
            for (sliceIdx in 0:(sliceCount-1)) {
                cat(sprintf("\tt=%d:", sliceIdx))
                for (i in 0:(outcomeCount-1)) {
                    cat(sprintf(" %f", v[(sliceIdx*outcomeCount+i)+1]))
                }
                cat("\n")
            }
        }
    }
    cat("\n")
}

cat("Starting Tutorial6...\n")
net <- Network()

loc <- createCptNode(net, "Location", "Location", c("Pittsburgh", "Sahara"), 160, 360)
rain <- createCptNode(net, "Rain", "Rain",c("true", "false"), 380, 240)
umb <- createCptNode(net, "Umbrella", "Umbrella", c("true", "false"), 300, 100)

net$setNodeTemporalType(rain, net$NodeTemporalType$PLATE)
net$setNodeTemporalType(umb, net$NodeTemporalType$PLATE)

net$addArc(loc, rain)
net$addTemporalArc(rain, rain, 1)
net$addArc(rain, umb)

rainDef <- c( 0.7,
              0.3,
              0.01,
              0.99 )
              
net$setNodeDefinition(rain, rainDef)
              
rainDefTemporal <- c( 0.7,
                      0.3,
                      0.3,
                      0.7,
                      0.001,
                      0.999,
                      0.01,
                      0.99 )
                      
net$setNodeTemporalDefinition(rain, 1, rainDefTemporal)

umbDef <- c( 0.9,
             0.1,
             0.2,
             0.8 )
             
net$setNodeDefinition(umb, umbDef)

net$setSliceCount(5)

cat("Performing update without evidence.\n")
updateAndShowTemporalResults(net)

cat("Setting Umbrella[t=1] to true and Umbrella[t=3] to false.\n")
net$setTemporalEvidence(umb, 1, 0)
net$setTemporalEvidence(umb, 3, 1)
updateAndShowTemporalResults(net)

net$writeFile("tutorial6.xdsl")
cat("Tutorial6 complete: Network written to tutorial6.xdsl\n")
