// tutorial2.cpp
// Tutorial2 loads the XDSL file created by Tutorial1,
// then performs the series of inference calls,
// changing evidence each time.

#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile.h"
#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile_license.h"

#include <cstdio>

static int ChangeEvidenceAndUpdate(
    DSL_network &net, const char *nodeId, const char *outcomeId);

static void PrintAllPosteriors(DSL_network &net);


int Tutorial2()
{
    printf("Starting Tutorial2...\n");

    DSL_errorH().RedirectToFile(stdout);

    // load the network created by Tutorial1
    DSL_network net;
    int res = net.ReadFile("tutorial1.xdsl");
    if (DSL_OKAY != res)
    {
        printf(
            "Network load failed, did you run Tutorial1 before Tutorial2?\n");
        return res;
    }

    printf("Posteriors with no evidence set:\n");
    net.UpdateBeliefs();
    PrintAllPosteriors(net);

    printf("\nSetting Forecast=Good.\n");
    ChangeEvidenceAndUpdate(net, "Forecast", "Good");

    printf("\nAdding Economy=Up.\n");
    ChangeEvidenceAndUpdate(net, "Economy", "Up");

    printf("\nChanging Forecast to Poor, keeping Economy=Up.\n");
    ChangeEvidenceAndUpdate(net, "Forecast", "Poor");

    printf("\nRemoving evidence from Economy, keeping Forecast=Poor.\n");
    ChangeEvidenceAndUpdate(net, "Economy", NULL);

    printf("\nTutorial2 complete.\n");
    return DSL_OKAY;
}


static void PrintPosteriors(DSL_network &net, int handle)
{
    DSL_node *node = net.GetNode(handle);
    const char* nodeId = node->GetId();
    const DSL_nodeVal* val = node->Val();
    if (val->IsEvidence())
    {
        printf("%s has evidence set (%s)\n", 
            nodeId, val->GetEvidenceId());
    }
    else
    {
        const DSL_idArray& outcomeIds = *node->Def()->GetOutcomeIds();
        const DSL_Dmatrix& posteriors = *val->GetMatrix();
        for (int i = 0; i < posteriors.GetSize(); i++)
        {
            printf("P(%s=%s)=%g\n", nodeId, outcomeIds[i], posteriors[i]);
        }
    }
}

static void PrintAllPosteriors(DSL_network &net)
{
    for (int h = net.GetFirstNode(); h >= 0; h = net.GetNextNode(h))
    {
        PrintPosteriors(net, h);
    }
}

static int ChangeEvidenceAndUpdate(
    DSL_network &net, const char *nodeId, const char *outcomeId)
{
    DSL_node* node = net.GetNode(nodeId);
    if (NULL == node)
    {
        return DSL_OUT_OF_RANGE;
    }

    int res;
    if (NULL != outcomeId)
    {
        res = node->Val()->SetEvidence(outcomeId);
    }
    else
    {
        res = node->Val()->ClearEvidence();
    }
    if (DSL_OKAY != res)
    {
        return res;
    }

    res = net.UpdateBeliefs();
    if (DSL_OKAY != res)
    {
        return res;
    }
    PrintAllPosteriors(net);
    return DSL_OKAY;
}
