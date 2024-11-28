// tutorial7.cpp
// Tutorial7 creates a network with three equation-based nodes
// performs the inference, then saves the model to disk.

#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile.h"
#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile_license.h"

#include <cstdio>


static int CreateEquationNode(
    DSL_network &net, const char *id, const char *name,
    const char *equation, double loBound, double hiBound,
    int xPos, int yPos);

static void UpdateAndShowStats(DSL_network &net);

static void SetUniformIntervals(DSL_network &net, int nodeHandle, int count);

int Tutorial7()
{
    printf("Starting Tutorial7...\n");

    DSL_errorH().RedirectToFile(stdout);

    DSL_network net;
    net.EnableRejectOutlierSamples(true);
    int tra = CreateEquationNode(net,
        "tra", "Return Air Temperature",
        "tra=24", 23.9, 24.1,
        280, 100);
    int u_d = CreateEquationNode(net, 
        "u_d", "Damper Control Signal",
        "u_d = Bernoulli(0.539)*0.8 + 0.2", 0, 1,
        160, 100);
    int toa = CreateEquationNode(net, 
        "toa", "Outside Air Temperature",
        "toa=Normal(11,15)", -10, 40,
        60, 100);
    int tma = CreateEquationNode(net, 
        "tma", "Mixed Air Temperature",
        "tma=toa*u_d+(tra-tra*u_d)", 10, 30,
        110, 200);

    SetUniformIntervals(net, toa, 5);
    SetUniformIntervals(net, tma, 4);

    printf("Results with no evidence:\n");
    UpdateAndShowStats(net);

    net.GetNode(toa)->Val()->SetEvidence(28.5);
    printf("Results with outside air temperature set to 28.5:\n");
    UpdateAndShowStats(net);
    
    net.GetNode(toa)->Val()->ClearEvidence();
    printf("Results with mixed air temperature set to 21:\n");
    net.GetNode(tma)->Val()->SetEvidence(21.0); // ensure it's a double value
    UpdateAndShowStats(net);

    int res = net.WriteFile("tutorial7.xdsl");
    if (DSL_OKAY != res)
    {
        return res;
    }

    printf("Tutorial7 complete: Network written to tutorial7.xdsl\n");
    return DSL_OKAY;
}


static int CreateEquationNode(
	DSL_network &net, const char *id, const char *name,
    const char *equation, double loBound, double hiBound,
    int xPos, int yPos)
{
    int handle = net.AddNode(DSL_EQUATION, id);
    DSL_node *node = net.GetNode(handle);
    node->SetName(name);
    auto eq = node->Def<DSL_equation>();
    eq->SetEquation(equation);
    eq->SetBounds(loBound, hiBound);
    DSL_rectangle &position = node->Info().Screen().position;
    position.center_X = xPos;
    position.center_Y = yPos;
    position.width = 85;
    position.height = 55;
    return handle;
}


static void ShowStats(DSL_network &net, int nodeHandle)
{
    DSL_node* node = net.GetNode(nodeHandle);
    const char *nodeId = node->GetId();

    auto eqVal = node->Val<DSL_equationEvaluation>();
    if (eqVal->IsEvidence())
    {
        double v;
        eqVal->GetEvidence(v);
        printf("%s has evidence set (%g)\n", nodeId, v);
        return;
    }

    const DSL_Dmatrix &discBeliefs = eqVal->GetDiscBeliefs();
    if (discBeliefs.IsEmpty())
    {
        double mean, stddev, vmin, vmax;
        eqVal->GetStats(mean, stddev, vmin, vmax);
        printf("%s: mean=%g stddev=%g min=%g max=%g\n",
            nodeId, mean, stddev, vmin, vmax);
    }
    else
    {
        auto eqDef = node->Def<DSL_equation>();
        const DSL_equation::IntervalVector &iv = eqDef->GetDiscIntervals();
        printf("%s is discretized.\n", nodeId);
        double loBound, hiBound;
        eqDef->GetBounds(loBound, hiBound);
        double lo = loBound;
        for (int i = 0; i < discBeliefs.GetSize(); i++)
        {
            double hi = iv[i].second;
            printf("\tP(%s in %g..%g)=%g\n", nodeId, lo, hi, discBeliefs[i]);
            lo = hi;
        }
    }
}


static void UpdateAndShowStats(DSL_network &net)
{
    net.UpdateBeliefs();
    for (int h = net.GetFirstNode(); h >= 0; h = net.GetNextNode(h))
    {
        ShowStats(net, h);
    }
    printf("\n");
}


static void SetUniformIntervals(DSL_network &net, int nodeHandle, int count)
{
    auto eq = net.GetNode(nodeHandle)->Def<DSL_equation>();
    double lo, hi;
    eq->GetBounds(lo, hi);
    DSL_equation::IntervalVector iv(count);
    for (int i = 0; i < count; i++)
    {
        iv[i].second = lo + (i + 1) * (hi - lo) / count;
    }
    eq->SetDiscIntervals(iv);
}
