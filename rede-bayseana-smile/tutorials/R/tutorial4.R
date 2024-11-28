library(rSMILE)
source("License.R")

# Tutorial4 loads the XDSL file file created by Tutorial1
# and adds decision and utility nodes, which transforms 
# a Bayesian Network (BN) into an Influence Diagram (ID).

createNode = function(net, nodeType, id, name, outcomes, xPos, yPos) {
    handle <- net$addNode(nodeType, id)
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

cat("Starting Tutorial4...\n")
net <- Network()

net$readFile("tutorial1.xdsl")

s <- net$getNode("Success")

i <- createNode(net, net$NodeType$DECISION, "Invest", "Investment decision", 
    c("Invest", "DoNotInvest"), 160L, 240L)

g <- createNode(net, net$NodeType$UTILITY, "Gain", "Financial Gain", NULL, 60, 200)

net$addArc(i, g)
net$addArc(s, g)

gainDefinition <- c(10000, # Utility(Invest=I, Success=S)
                    -5000, # Utility(Invest=I, Success=F)
                    500,   # Utility(Invest=D, Success=S)
                    500)   # Utility(Invest=D, Success=F)


net$setNodeDefinition(g, gainDefinition)

net$writeFile("tutorial4.xdsl")                   

cat("Tutorial4 complete: Influence diagram written to tutorial4.xdsl.\n")
