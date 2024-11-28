library(rSMILE)
source("License.R")

# Tutorial10 loads Credit10k.csv file
# and runs multiple structure learning algorithms
# using the loaded dataset.
# Use the link below to download the Credit10k.csv file:
# https://support.bayesfusion.com/docs/Examples/Learning/Credit10K.csv

cat("Starting Tutorial10...\n")
ds <- DataSet()

ds$readFile("Credit10k.csv")
cat(sprintf("Dataset has %d variables (columns) and %d records (rows)\n", 
    ds$getVariableCount(), ds$getRecordCount()))
bayesSearch <- BayesianSearch()
bayesSearch$setIterationCount(50)
bayesSearch$setRandSeed(9876543)
net1 <- bayesSearch$learn(ds)
cat(sprintf("1st Bayesian Search finished, structure score: %f\n", 
    bayesSearch$getLastScore()))
net1$writeFile("tutorial10-bs1.xdsl")

bayesSearch$setRandSeed(3456789)
net2 <- bayesSearch$learn(ds)
cat(sprintf("2nd Bayesian Search finished, structure score: %f\n",
    bayesSearch$getLastScore()))
net2$writeFile("tutorial10-bs2.xdsl")

idxAge <- ds$findVariable("Age")
idxProfession <- ds$findVariable("Profession")
idxCreditWorthiness <- ds$findVariable("CreditWorthiness")

backgroundKnowledge <- BkKnowledge()
backgroundKnowledge$matchData(ds)
backgroundKnowledge$addForbiddenArc(idxAge, idxCreditWorthiness)
backgroundKnowledge$addForcedArc(idxAge, idxProfession)

bayesSearch$setBkKnowledge(backgroundKnowledge)
net3 <- bayesSearch$learn(ds)
cat(sprintf("3rd Bayesian Search finished, structure score: %f\n",
    bayesSearch$getLastScore()))
net2$writeFile("tutorial10-bs3.xdsl")

tan <- TAN()
tan$setRandSeed(777999)
tan$setClassVariableId("CreditWorthiness")
net4 <- tan$learn(ds)
cat("Tree-augmented Naive Bayes finished")
net4$writeFile("tutorial10-tan.xdsl")

pc <- PC()
pattern <- pc$learn(ds)
net5 <- pattern$makeNetwork(ds)
cat("PC finished, proceeding to parameter learning\n")
net5$writeFile("tutorial10-pc.xdsl")
em <- EM()
matching <- ds$matchNetwork(net5)
em$setUniformizeParameters(FALSE)
em$setRandomizeParameters(FALSE)
em$setEqSampleSize(0)
em$learn(ds, net5, matching)
cat("EM finished\n")
net5$writeFile("tutorial10-pc-em.xdsl")

cat("Tutorial10 complete.\n")
