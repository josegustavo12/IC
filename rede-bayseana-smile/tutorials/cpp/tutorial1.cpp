// tutorial1.cpp
// Tutorial1 creates a simple network with three nodes,
// then saves it as XDSL file to disk.

//g++ tutorial1.cpp -I/home/josegustavo/Documentos/IC/rede-bayseana/include -L/home/josegustavo/Documentos/IC/rede-bayseana/lib -lsmile -o tutorial && ./tutorial


//g++ -I/home/josegustavo/Documentos/IC/rede-bayseana/include -o tutorial1 tutorial1.cpp

#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile.h"
#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile_license.h"

#include <cstdio>

static int CreateCptNode(
    DSL_network& net, const char* id, const char* name,
    std::initializer_list<const char*> outcomes, int xPos, int yPos);


int Tutorial1()
{
    printf("Starting Tutorial1...\n");

    // show errors and warnings in the console
    DSL_errorH().RedirectToFile(stdout);

    DSL_network net;

    int e = CreateCptNode(net, "Economy", "State of the economy", 
        { "Up", "Flat", "Down" }, 160, 40);

    int s = CreateCptNode(net, "Success", "Success of the venture", 
        { "Success", "Failure" }, 60, 40);
    
    int f = CreateCptNode(net, "Forecast", "Expert forecast", 
        { "Good", "Moderate", "Poor" }, 110, 140);

    net.AddArc(e, s);
    net.AddArc(s, f);
    net.AddArc(e, f);

    int res = net.GetNode(e)->Def()->SetDefinition({
        0.2, // P(Economy=U)
        0.7, // P(Economy=F)
        0.1  // P(Economy=D)
    });
    if (DSL_OKAY != res)
    {
        return res;
    }

    res = net.GetNode(s)->Def()->SetDefinition({
        0.3, // P(Success=S|Economy=U)
        0.7, // P(Success=F|Economy=U)
        0.2, // P(Success=S|Economy=F)
        0.8, // P(Success=F|Economy=F)
        0.1, // P(Success=S|Economy=D)
        0.9  // P(Success=F|Economy=D)
    });
    if (DSL_OKAY != res)
    {
        return res;
    }

    res = net.GetNode(f)->Def()->SetDefinition({
        0.70, // P(Forecast=G|Success=S,Economy=U)
        0.29, // P(Forecast=M|Success=S,Economy=U)
        0.01, // P(Forecast=P|Success=S,Economy=U)
        0.65, // P(Forecast=G|Success=S,Economy=F)
        0.30, // P(Forecast=M|Success=S,Economy=F)
        0.05, // P(Forecast=P|Success=S,Economy=F)
        0.60, // P(Forecast=G|Success=S,Economy=D)
        0.30, // P(Forecast=M|Success=S,Economy=D)
        0.10, // P(Forecast=P|Success=S,Economy=D)
        0.15, // P(Forecast=G|Success=F,Economy=U)
        0.30, // P(Forecast=M|Success=F,Economy=U)
        0.55, // P(Forecast=P|Success=F,Economy=U)
        0.10, // P(Forecast=G|Success=F,Economy=F)
        0.30, // P(Forecast=M|Success=F,Economy=F)
        0.60, // P(Forecast=P|Success=F,Economy=F)
        0.05, // P(Forecast=G|Success=F,Economy=D)
        0.25, // P(Forecast=G|Success=F,Economy=D)
        0.70  // P(Forecast=G|Success=F,Economy=D)
    });
    if (DSL_OKAY != res)
    {
        return res;
    }

    res = net.WriteFile("tutorial1.xdsl");
    if (DSL_OKAY != res)
    {
        return res;
    }

    printf("Tutorial1 complete: Network written to tutorial1.xdsl\n");
    return DSL_OKAY;
}


static int CreateCptNode(
	DSL_network &net, const char *id, const char *name, 
    std::initializer_list<const char *> outcomes, int xPos, int yPos)
{
    int handle = net.AddNode(DSL_CPT, id);
    DSL_node *node = net.GetNode(handle);
    node->SetName(name);
    node->Def()->SetNumberOfOutcomes(outcomes);
    DSL_rectangle &position = node->Info().Screen().position;
    position.center_X = xPos;
    position.center_Y = yPos;
    position.width = 85;
    position.height = 55;
    return handle;
}
