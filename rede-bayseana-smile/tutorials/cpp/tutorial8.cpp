// tutorial8.cpp
// Tutorial8 loads continuous model from the XDSL file written by Tutorial7,
// then adds discrete nodes to create a hybrid model. Inference is performed
// and model is saved to disk.

#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile.h"
#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile_license.h"

#include <cstdio>

static int CreateCptNode(
    DSL_network& net, const char* id, const char* name,
    std::initializer_list<const char*> outcomes, int xPos, int yPos);

static void UpdateAndShowStats(DSL_network &net);


int Tutorial8()
{
    printf("Starting Tutorial8...\n");

    DSL_errorH().RedirectToFile(stdout);

    DSL_network net;
    int res = net.ReadFile("tutorial7.xdsl");
    if (DSL_OKAY != res)
    {
        printf(
            "Network load failed, did you run Tutorial7 before Tutorial8?\n");
        return res;
    }

    int toa = net.FindNode("toa");
    if (toa < 0)
    {
        printf("Outside air temperature node not found.\n");
        return toa;
    }

    CreateCptNode(net, 
        "zone", "Climate Zone", { "Temperate", "Desert" },
        60, 20);

    auto eq = net.GetNode(toa)->Def<DSL_equation>();
    eq->SetEquation("toa=If(zone=\"Desert\",Normal(22,5),Normal(11,10))");

    int perceived = CreateCptNode(net,
        "perceived", "Perceived Temperature", { "Hot", "Warm", "Cold" },
        60, 300);
    net.AddArc(toa, perceived);

    res = net.GetNode(perceived)->Def()->SetDefinition({
        0   , // P(perceived=Hot |toa in -10..0)
        0.02, // P(perceived=Warm|toa in -10..0)
        0.98, // P(perceived=Cold|toa in -10..0)
        0.05, // P(perceived=Hot |toa in 0..10)
        0.15, // P(perceived=Warm|toa in 0..10)
        0.80, // P(perceived=Cold|toa in 0..10)
        0.10, // P(perceived=Hot |toa in 10..20)
        0.80, // P(perceived=Warm|toa in 10..20)
        0.10, // P(perceived=Cold|toa in 10..20)
        0.80, // P(perceived=Hot |toa in 20..30)
        0.15, // P(perceived=Warm|toa in 20..30)
        0.05, // P(perceived=Cold|toa in 20..30)
        0.98, // P(perceived=Hot |toa in 30..40)
        0.02, // P(perceived=Warm|toa in 30..40)
        0     // P(perceived=Cold|toa in 30..40)
    });
    if (DSL_OKAY != res)
    {
        return res;
    }

    net.GetNode("zone")->Val()->SetEvidence("Temperate");
    printf("Results in temperate zone:\n");
    UpdateAndShowStats(net);

    net.GetNode("zone")->Val()->SetEvidence("Desert");
    printf("Results in desert zone:\n");
    UpdateAndShowStats(net);

    res = net.WriteFile("tutorial8.xdsl");
    if (DSL_OKAY != res)
    {
        return res;
    }

    printf("Tutorial8 complete: Network written to tutorial8.xdsl\n");
    return DSL_OKAY;
}


static void ShowStats(DSL_network& net, int nodeHandle)
{
    DSL_node* node = net.GetNode(nodeHandle);
    const char* nodeId = node->GetId();

    auto eqVal = node->Val<DSL_equationEvaluation>();
    if (eqVal->IsEvidence())
    {
        double v;
        eqVal->GetEvidence(v);
        printf("%s has evidence set (%g)\n", nodeId, v);
        return;
    }

    const DSL_Dmatrix& discBeliefs = eqVal->GetDiscBeliefs();
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
        const DSL_equation::IntervalVector& iv = eqDef->GetDiscIntervals();
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
        if (net.GetNode(h)->Def()->GetType() == DSL_EQUATION)
        { 
           ShowStats(net, h);
        }
    }
}


static int CreateCptNode(
    DSL_network& net, const char* id, const char* name,
    std::initializer_list<const char*> outcomes, int xPos, int yPos)
{
    int handle = net.AddNode(DSL_CPT, id);
    DSL_node* node = net.GetNode(handle);
    node->SetName(name);
    node->Def()->SetNumberOfOutcomes(outcomes);
    DSL_rectangle& position = node->Info().Screen().position;
    position.center_X = xPos;
    position.center_Y = yPos;
    position.width = 85;
    position.height = 55;
    return handle;
}

