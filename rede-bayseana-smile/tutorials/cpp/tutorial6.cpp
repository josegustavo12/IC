// tutorial6.cpp
// Tutorial6 creates a dynamic Bayesian network (DBN),
// performs the inference, then saves the model to disk.

#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile.h"
#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile_license.h"

#include <cstdio>


static int CreateCptNode(
    DSL_network& net, const char* id, const char* name,
    std::initializer_list<const char*> outcomes, int xPos, int yPos);

static void UpdateAndShowTemporalResults(DSL_network &net);


int Tutorial6()
{
    printf("Starting Tutorial6...\n");

    DSL_errorH().RedirectToFile(stdout);
    
    DSL_network net;

    int loc = CreateCptNode(net, "Location", "Location",
        { "Pittsburgh", "Sahara" }, 160, 360);

    int rain = CreateCptNode(net, "Rain", "Rain",
        { "true", "false" }, 380, 240);

    int umb = CreateCptNode(net, "Umbrella", "Umbrella",
        { "true", "false" }, 300, 100);

    net.SetTemporalType(rain, dsl_temporalType::dsl_plateNode);
    net.SetTemporalType(umb, dsl_temporalType::dsl_plateNode);

    net.AddArc(loc, rain);
    net.AddTemporalArc(rain, rain, 1);
    net.AddArc(rain, umb);

    DSL_nodeDef *rainDef = net.GetNode(rain)->Def();
    int res = rainDef->SetDefinition({
        0.7,  // P(Rain=true |Location=Pittsburgh)
        0.3,  // P(Rain=false|Location=Pittsburgh)
        0.01, // P(Rain=true |Location=Sahara)
        0.99  // P(Rain=false|Location=Sahara)
    });
    if (DSL_OKAY != res)
    {
        return res;
    }

    res = rainDef->SetTemporalDefinition(1, {
        0.7,   // P(Rain=true |Location=Pittsburgh,Rain[t-1]=true)
        0.3,   // P(Rain=false|Location=Pittsburgh,Rain[t-1]=true)
        0.3,   // P(Rain=true |Location=Pittsburgh,Rain[t-1]=false)
        0.7,   // P(Rain=false|Location=Pittsburgh,Rain[t-1]=false)
        0.001, // P(Rain=true |Location=Sahara,Rain[t-1]=true)
        0.999, // P(Rain=false|Location=Sahara,Rain[t-1]=true)
        0.01,  // P(Rain=true |Location=Sahara,Rain[t-1]=false)
        0.99   // P(Rain=false|Location=Sahara,Rain[t-1]=false)
    });
    if (DSL_OKAY != res)
    {
        return res;
    }

    res = net.GetNode(umb)->Def()->SetDefinition({
        0.9, // P(Umbrella=true |Rain=true)
        0.1, // P(Umbrella=false|Rain=true)
        0.2, // P(Umbrella=true |Rain=false)
        0.8  // P(Umbrella=false|Rain=false)
    });
    if (DSL_OKAY != res)
    {
        return res;
    }

    net.SetNumberOfSlices(5);

    printf("Performing update without evidence.\n");
    UpdateAndShowTemporalResults(net);

    printf("Setting Umbrella[t=1] to true and Umbrella[t=3] to false.\n");
    res = net.GetNode(umb)->Val()->SetTemporalEvidence(1, 0);
    if (DSL_OKAY != res)
    {
        return res;
    }
    res = net.GetNode(umb)->Val()->SetTemporalEvidence(3, 1);
    if (DSL_OKAY != res)
    {
        return res;
    }
    UpdateAndShowTemporalResults(net);

    res = net.WriteFile("tutorial6.xdsl");
    if (DSL_OKAY != res)
    {
        return res;
    }
    
    printf("Tutorial6 complete: Network written to tutorial6.xdsl\n");
    return DSL_OKAY;
}


static void UpdateAndShowTemporalResults(DSL_network &net)
{
    net.UpdateBeliefs();
    int sliceCount = net.GetNumberOfSlices();
    for (int h = net.GetFirstNode(); h >= 0; h = net.GetNextNode(h))
    {
        if (net.GetTemporalType(h) == dsl_temporalType::dsl_plateNode)
        {
            DSL_node *node = net.GetNode(h);
            int outcomeCount = node->Def()->GetNumberOfOutcomes();
            printf("Temporal beliefs for %s:\n", node->GetId());
            const DSL_Dmatrix& mtx = *node->Val()->GetMatrix();
            for (int sliceIdx = 0; sliceIdx < sliceCount; sliceIdx++)
            {
                printf("\tt=%d:", sliceIdx);
                for (int i = 0; i < outcomeCount; i++)
                {
                    printf(" %f", mtx[sliceIdx * outcomeCount + i]);
                }
                printf("\n");
            }
        }
    }
    printf("\n");
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
