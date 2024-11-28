// tutorial9.cpp
// Tutorial9 loads Credit10k.csv file
// and runs multiple structure learning algorithms
// using the loaded dataset.
// Use the link below to download the Credit10k.csv file:
// https://support.bayesfusion.com/docs/Examples/Learning/Credit10K.csv

#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile.h"
#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile_license.h"

#include <cstdio>
#include <utility>

using namespace std;

int Tutorial9()
{
	printf("Starting Tutorial9...\n");
	DSL_errorH().RedirectToFile(stdout);

	DSL_dataset ds;
    int res = ds.ReadFile("Credit10k.csv");
    if (DSL_OKAY != res)
    {
        printf("Dataset load failed\n");
        return res;
    }

    printf("Dataset has %d variables (columns) and %d records (rows)\n",
        ds.GetNumberOfVariables(), ds.GetNumberOfRecords());

    double bestScore;
    DSL_bs bayesSearch;
    bayesSearch.nrIteration = 50;

    DSL_network net1;
    bayesSearch.seed = 9876543;
    res = bayesSearch.Learn(ds, net1, NULL, NULL, &bestScore);
    if (DSL_OKAY != res)
    {
        printf("Bayesian Search failed (%d)\n", res);
        return res;
    }
    net1.SimpleGraphLayout();
    printf("1st Bayesian Search finished, structure score: %g\n", bestScore);
    net1.WriteFile("tutorial9-bs1.xdsl");

    DSL_network net2;
    bayesSearch.seed = 3456789;
    res = bayesSearch.Learn(ds, net2, NULL, NULL, &bestScore);
    if (DSL_OKAY != res)
    {
        printf("Bayesian Search failed (%d)\n", res);
        return res;
    }
    net2.SimpleGraphLayout();
    printf("2nd Bayesian Search finished, structure score: %g\n", bestScore);
    net2.WriteFile("tutorial9-bs2.xdsl");

    
    int idxAge = ds.FindVariable("Age");
    int idxProfession = ds.FindVariable("Profession");
    int idxCreditWorthiness = ds.FindVariable("CreditWorthiness");
    if (idxAge < 0 || idxProfession < 0 || idxCreditWorthiness < 0)
    {
        printf("Can't find dataset variables for background knowledge\n");
        printf("The loaded file may not be Credit10k.csv\n");
        return DSL_OUT_OF_RANGE;
    }
    DSL_network net3;
    bayesSearch.bkk.forbiddenArcs.push_back(make_pair(idxAge, idxCreditWorthiness));
    bayesSearch.bkk.forcedArcs.push_back(make_pair(idxAge, idxProfession));
    res = bayesSearch.Learn(ds, net3, NULL, NULL, &bestScore);
    if (DSL_OKAY != res)
    {
        printf("Bayesian Search finished (%d)\n", res);
        return res;
    }
    net3.SimpleGraphLayout();
    printf("3rd Bayesian Search complete, structure score: %g\n", bestScore);
    net3.WriteFile("tutorial9-bs3.xdsl");

    DSL_network net4;
    DSL_tan tan;
    tan.seed = 777999;
    tan.classvar = "CreditWorthiness";
    res = tan.Learn(ds, net4);
    if (DSL_OKAY != res)
    {
        printf("TAN failed (%d)\n", res);
        return res;
    }
    net4.SimpleGraphLayout();
    printf("Tree-augmented Naive Bayes finished\n");
    net4.WriteFile("tutorial9-tan.xdsl");

    DSL_pc pc;
    DSL_pattern pattern;
    res = pc.Learn(ds, pattern);
    if (DSL_OKAY != res)
    {
        printf("PC failed (%d)\n", res);
        return res;
    }
    
    DSL_network net5;
    pattern.ToNetwork(ds, net5);
    net5.SimpleGraphLayout();
    printf("PC finished, proceeding to parameter learning\n");
    net5.WriteFile("tutorial9-pc.xdsl");
    DSL_em em;
    string errMsg;
    vector<DSL_datasetMatch> matching;
    res = ds.MatchNetwork(net5, matching, errMsg);
    if (DSL_OKAY != res)
    {
        printf("Can't automatically match network with dataset: %s\n", errMsg.c_str());
        return DSL_OUT_OF_RANGE;
    }
    em.SetUniformizeParameters(false);
    em.SetRandomizeParameters(false);
    em.SetEquivalentSampleSize(0);
    res = em.Learn(ds, net5, matching);
    if (DSL_OKAY != res)
    {
        printf("EM failed (%d)\n", res);
        return res;
    }
    printf("EM finished\n");
    net5.WriteFile("tutorial9-pc-em.xdsl");

	printf("Tutorial9 complete\n");
	return DSL_OKAY;
}