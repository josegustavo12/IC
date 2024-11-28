// tutorial3.cpp
// Tutorial3 loads the XDSL file and prints the information
// about the structure (nodes and arcs) and the parameters 
// (conditional probabilities of the nodes) of the network.

#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile.h"
#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile_license.h"

#include <cstdio>

static void PrintNodeInfo(DSL_network &net, int nodeHandle);


int Tutorial3()
{
    printf("Starting Tutorial3...\n");

    DSL_errorH().RedirectToFile(stdout);

    // load the network created by Tutorial1
    DSL_network net;
    int res = net.ReadFile("tutorial1.xdsl");
    if (DSL_OKAY != res)
    {
        printf(
            "Network load failed, did you run Tutorial1 before Tutorial3?\n");
        return res;
    }

    for (int h = net.GetFirstNode(); h >= 0; h = net.GetNextNode(h))
    {
        PrintNodeInfo(net, h);
    }

    printf("\nTutorial3 complete.\n");
    return DSL_OKAY;
}


// PrintMatrix displays each probability entry in the matrix in the separate 
// line, preceeded by the information about node and parent outcomes the entry 
// relates to.
// The coordinates of the matrix are ordered as P1,...,Pn,S
// where Pi is the outcome index of i-th parent and S is the outcome of the node 
// for which this matrix is the CPT.
static void PrintMatrix(
    DSL_network &net, const DSL_Dmatrix &mtx, 
    const DSL_idArray &outcomes, const DSL_intArray &parents)
{
    int dimCount = mtx.GetNumberOfDimensions();
    DSL_intArray coords(dimCount);
    coords.FillWith(0);

    // elemIdx and coords will be moving in sync
    for (int elemIdx = 0; elemIdx < mtx.GetSize(); elemIdx++)
    {
        const char *outcome = outcomes[coords[dimCount - 1]];
        printf("    P(%s", outcome);

        if (dimCount > 1)
        {
            printf(" | ");
            for (int parentIdx = 0; parentIdx < dimCount - 1; parentIdx++)
            {
                if (parentIdx > 0) printf(",");
                DSL_node *parentNode = net.GetNode(parents[parentIdx]);
                const DSL_idArray &parentOutcomes = 
                    *parentNode->Def()->GetOutcomeIds();
                printf("%s=%s", 
                    parentNode->GetId(), parentOutcomes[coords[parentIdx]]);
            }
        }

        double prob = mtx[elemIdx];
        printf(")=%g\n", prob);

        mtx.NextCoordinates(coords);
    }
}


// PrintNodeInfo displays node attributes: 
//   name, outcome ids, parent ids, children ids, CPT probabilities
static void PrintNodeInfo(DSL_network &net, int nodeHandle)
{
    DSL_node *node = net.GetNode(nodeHandle);
    printf("Node: %s\n", node->GetName());

    printf("  Outcomes:");
    const DSL_idArray &outcomes = *node->Def()->GetOutcomeIds();
    for (const char* oid : outcomes)
    {
        printf(" %s", oid);
    }
    printf("\n");

    const DSL_intArray &parents = net.GetParents(nodeHandle);
    if (!parents.IsEmpty())
    {
        printf("  Parents:");
        for (int p: parents)
        {
            printf(" %s", net.GetNode(p)->GetId());
        }
        printf("\n");
    }

    const DSL_intArray &children = net.GetChildren(nodeHandle);
    if (!children.IsEmpty())
    {
        printf("  Children:");
        for (int c: children)
        {
            printf(" %s", net.GetNode(c)->GetId());
        }
        printf("\n");
    }

    const DSL_nodeDef *def = node->Def();
    int defType = def->GetType();
    printf("  Definition type: %s\n", def->GetTypeName());
    if (DSL_CPT == defType || DSL_TRUTHTABLE == defType)
    {
        const DSL_Dmatrix &cpt = *def->GetMatrix();
        PrintMatrix(net, cpt, outcomes, parents);
    }
}
