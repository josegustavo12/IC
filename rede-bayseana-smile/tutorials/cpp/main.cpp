// main.cpp
// Run all SMILE tutorials.

// smile_license.h contains your personal license key
#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile.h"
#include "/home/josegustavo/Documentos/IC/rede-bayseana/include/smile_license.h"

// g++ main.cpp -I/home/josegustavo/Documentos/IC/rede-bayseana/include -L/home/josegustavo/Documentos/IC/rede-bayseana/lib -lsmile -o main && ./main



int Tutorial1();
int Tutorial2();
int Tutorial3();
int Tutorial4();
int Tutorial5();
int Tutorial6();
int Tutorial7();
int Tutorial8();
int Tutorial9();

int main()
{
    static int (* const f[])() = 
    { 
        Tutorial1, Tutorial2, Tutorial3, 
        Tutorial4, Tutorial5, Tutorial6,
        Tutorial7, Tutorial8, Tutorial9
    };
    for (int i = 0; i < sizeof(f) / sizeof(f[0]); i++)
    {
        int r = f[i]();
        if (r)
        {
            return r;
        }
    }
    return 0;
}
