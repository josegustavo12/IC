#include "include/smile.h"
#include "include/smile_license.h"

#include <iostream>


// g++ -std=c++11 HelloSmile.cpp -I./include -L./lib -lsmile -o HelloSmile
// g++ HelloSmile.cpp -I./include -L./lib -lsmile -o HelloSmile

int main(){
    DSL_errorH().RedirectToFile(stdout);
    DSL_network net;
    int res = net.ReadFile("data/bn_from_circuit.xdsl");
    if (DSL_OKAY != res){
        return res;
    }
    net.GetNode("Forecast")->Val()->SetEvidence("Moderate");
    net.UpdateBeliefs();
    DSL_node* sn = net.GetNode("Success");
    const DSL_Dmatrix& beliefs = *sn->Val()->GetMatrix();
    const DSL_idArray& outcomes = *sn->Def()->GetOutcomeIds();
    for (int i = 0; i < outcomes.GetSize(); i++)
    {
    printf("%s=%g\n", outcomes[i], beliefs[i]);
    }
    return DSL_OKAY;
}