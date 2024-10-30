// tutorial1.cpp
// Tutorial1 creates a simple network with three nodes,
// then saves it as XDSL file to disk.

// g++ -std=c++11 main.cpp tutorial?.cpp -I./smile -L./smile -lsmile  <<<<< ------- 

#include "include/smile.h"
#include "include/smile_license.h"
#include <cstdio>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>


static int CreateCptNode(
    DSL_network& net, const char* id, const char* name,
    std::initializer_list<const char*> outcomes, int xPos, int yPos);



void writeToFile(const std::vector<std::vector<std::string>>& vecOfVecs, const std::string& filename) {
    std::ofstream outFile(filename); // Open the file for writing
    if (!outFile.is_open()) { // Check if the file is opened successfully
        std::cerr << "Error opening file: " << filename << std::endl;
        return;
    }

    // Write the contents of the vector of vectors to the file
    for (const auto& innerVec : vecOfVecs) {
        for (const auto& str : innerVec) {
            outFile << str << " ";
        }
        outFile << std::endl; // Write newline after each inner vector
    }

    // Close the file
    outFile.close();
}



std::vector<std::vector<std::string>>  read_verilog(const std::string& verilogFilePath) {
    // Open the Verilog file
    std::ifstream verilogFile(verilogFilePath);
    // Vector where my data will be add
    std::vector<std::vector<std::string>> Data_Vector;
    std::vector<std::string> tempVector;


    // Check if the file is opened successfully
    if (!verilogFile.is_open()) {
        std::cerr << "Error opening file: " << verilogFilePath << std::endl;
        std::vector<std::vector<std::string>> null;
        return null;
    }

    // Read the Verilog file line by line
    std::string line;
   while (std::getline(verilogFile, line)) {
        // Find the first opening parenthesis
        size_t ParenthesisPos = line.find('(');
        if((ParenthesisPos != std::string::npos) && (ParenthesisPos < 5)){

            std::string LogicArgument = line.substr(0, ParenthesisPos);
            tempVector.push_back(LogicArgument);
            // std::cout << "LogicArgument: " << LogicArgument << std::endl;

            // std::cout << "Logic Argument: " << LogicArgument << std::endl;
            size_t current =  ParenthesisPos;
             while (current != std::string::npos + 1) { 
                size_t commaPos = line.find(',', current);
                if(commaPos == std::string::npos){
                     size_t ParenthesisPos_last = line.find(')', current);
                     std::string Argument = line.substr(current + 1, ParenthesisPos_last - current - 1);
                    // std::cout << "Argument: " << Argument << std::endl;
                     tempVector.push_back(Argument);
                     // std::cout << "Argument: " << Argument << std::endl; //get end argument
                     break;

                }
                std::string Argument = line.substr(current + 1, commaPos - current - 1);
                tempVector.push_back(Argument);
                // std::cout << "Argument: " << Argument << std::endl;
                current = commaPos + 1;
                
                
            
             }
            Data_Vector.push_back(tempVector);
            tempVector.clear();      
        }
        
    
    
    
    }

    // Close the file
    verilogFile.close();
    return Data_Vector;
}


int main()
{
    // "/home/lemy/project01.v"
    // "/home/lemy//Desktop/ISCAS./Verilog3/C880.v"
    std::string filePath = "verilog/C1355.v";
    printf("Starting Circuit Network..\n");
    std::vector<std::vector<std::string>> nodes = read_verilog(filePath);
    
     // show errors and warnings in the console
    DSL_errorH().RedirectToFile(stdout);

    DSL_network net;

     // Print the size of nodes (number of inner vectors)
    std::cout << "Size of nodes: " << nodes.size() << std::endl;

    std::map<std::string, int> dynamicVariables;
    
     for (const auto& vec : nodes) {
        int k = 0;
        int pass = 10;
        for (const auto& str : vec) {
            if(k == 1){
              int e = CreateCptNode(net, str.c_str(), "node", 
                                    { "0", "1"}, 60, 40); 
              
               dynamicVariables[str.c_str()] = e;  
            }
            k++;
            

        }
       
     
    }
    


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

    res = net.WriteFile("data/bn_from_circuit.xdsl");
    if (DSL_OKAY != res)
    {
        return res;
    } 

    printf("Network has been written to bn_from_circuit.xdsl\n");
    return DSL_OKAY;   
    return 0;
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
