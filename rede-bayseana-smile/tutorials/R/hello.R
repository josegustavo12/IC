library(rSMILE)

# License.R is your licensing key
source("License.R")

net <- Network()
net$readFile("VentureBN.xdsl")
net$setEvidence("Forecast", "Moderate")
net$updateBeliefs()
beliefs <- net$getNodeValue("Success")
for (i in 1:length(beliefs)) {
    cat(sprintf("%s = %f\n", net$getOutcomeId("Success", i-1L), beliefs[i]))
}