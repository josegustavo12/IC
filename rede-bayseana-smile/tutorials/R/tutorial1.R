library(rSMILE)
source("License.R")

createCptNode = function(net, id, name, outcomes, xPos, yPos) {
    handle <- net$addNode(net$NodeType$CPT, id)
    
    net$setNodeName(handle, name)
    net$setNodePosition(handle, xPos, yPos, 85L, 55L)
    outcomesCount <- length(outcomes)
    initialOutcomeCount <- net$getOutcomeCount(handle)
    i <- 0
    for (outcome in outcomes[1:initialOutcomeCount]) {
        net$setOutcomeId(handle, i, outcome)
        i <- i + 1
    }

    if ((initialOutcomeCount + 1) <= outcomesCount) {
        for (outcome in outcomes[(initialOutcomeCount + 1):(outcomesCount)]) {
            net$addOutcome(handle, outcome)
        }
    }
    
    return(handle)
}

cat("Starting Tutorial1...\n")

net <- Network()
e <- createCptNode(net, "Economy", "State of the economy",
    c("Up", "Flat", "Down"), 160L, 40L)

s <- createCptNode(net, "Success", "Success of the venture",
    c("Success","Failure"), 60L, 40L)

f <- createCptNode(net, "Forecast", "Expert forecast",
    c("Good","Moderate","Poor"), 110L, 140L)

net$addArc(e, s)
net$addArc(s, f)

net$addArc("Economy", "Forecast")
                   
economyDef <- c(0.2, # P(Economy=U)
                0.7, # P(Economy=F)
                0.1  # P(Economy=D)
               )
net$setNodeDefinition(e, economyDef)

successDef <- c(0.3, # P(Success=S|Economy=U)
                0.7, # P(Success=F|Economy=U)
                0.2, # P(Success=S|Economy=F)
                0.8, # P(Success=F|Economy=F)
                0.1, # P(Success=S|Economy=D)
                0.9  # P(Success=F|Economy=D)
               )
net$setNodeDefinition(s, successDef)

forecastDef <- c(0.70, # P(Forecast=G|Success=S,Economy=U)
                 0.29, # P(Forecast=M|Success=S,Economy=U)
                 0.01, # P(Forecast=P|Success=S,Economy=U)
                 
                 0.65, # P(Forecast=G|Success=S,Economy=F)
                 0.30, # P(Forecast=M|Success=S,Economy=F)
                 0.05, # P(Forecast=P|Success=S,Economy=F)
                 
                 0.60, # P(Forecast=G|Success=S,Economy=D)
                 0.30, # P(Forecast=M|Success=S,Economy=D)
                 0.10, # P(Forecast=P|Success=S,Economy=D)
                     
                 0.15, # P(Forecast=G|Success=F,Economy=U)
                 0.30, # P(Forecast=M|Success=F,Economy=U)
                 0.55, # P(Forecast=P|Success=F,Economy=U)
                     
                 0.10, # P(Forecast=G|Success=F,Economy=F)
                 0.30, # P(Forecast=M|Success=F,Economy=F)
                 0.60, # P(Forecast=P|Success=F,Economy=F)
                     
                 0.05, # P(Forecast=G|Success=F,Economy=D)
                 0.25, # P(Forecast=G|Success=F,Economy=D)
                 0.70  # P(Forecast=G|Success=F,Economy=D)
                )
net$setNodeDefinition(f, forecastDef)

net$writeFile("tutorial1.xdsl")

cat("Tutorial1 complete: Network written to tutorial1.xdsl\n")
