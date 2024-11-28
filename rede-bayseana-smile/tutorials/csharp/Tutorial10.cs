using System;
using Smile;
using Smile.Learning;

// Tutorial10 loads Credit10k.csv file
// and runs multiple structure learning algorithms
// using the loaded dataset.
// Use the link below to download the Credit10k.csv file:
// https://support.bayesfusion.com/docs/Examples/Learning/Credit10K.csv

namespace SmileNetTutorial
{
    class Tutorial10
    {
        public static void Run()
        {
            Console.WriteLine("Starting Tutorial10...");
            DataSet ds = new DataSet();
            try
            {
                ds.ReadFile("Credit10k.csv");
            } catch (SmileException)
            {
                Console.WriteLine("Dataset load failed");
                return;
            }
            Console.WriteLine("Dataset has {0} variables (columns) and {1} records (rows)", 
                ds.VariableCount, ds.RecordCount);
            BayesianSearch bayesSearch = new BayesianSearch();
            bayesSearch.IterationCount = 50;
            bayesSearch.RandSeed = 9876543;
            Network net1;
            try
            {
                net1 = bayesSearch.Learn(ds);
            } catch (SmileException)
            {
                Console.WriteLine("Bayesian Search failed");
                return;
            }
            Console.WriteLine("1st Bayesian Search finished, structure score: {0}", 
                bayesSearch.LastScore);
            net1.WriteFile("tutorial10-bs1.xdsl");

            Network net2;
            bayesSearch.RandSeed = 3456789;
            try
            {
                net2 = bayesSearch.Learn(ds);
            }
            catch (SmileException)
            {
                Console.WriteLine("Bayesian Search failed");
                return;
            }
            Console.WriteLine("2nd Bayesian Search finished, structure score: {0}", 
                bayesSearch.LastScore);
            net2.WriteFile("tutorial10-bs2.xdsl");

            int idxAge = ds.FindVariable("Age");
            int idxProfession = ds.FindVariable("Profession");
            int idxCreditWorthiness = ds.FindVariable("CreditWorthiness");
            if (idxAge < 0 || idxProfession < 0 || idxCreditWorthiness < 0)
            {
                Console.WriteLine("Can't find dataset variables for background knowledge");
                Console.WriteLine("The loaded file may not be Credit10k.csv");
                return;
            }

            BkKnowledge backgroundKnowledge = new BkKnowledge();
			backgroundKnowledge.MatchData(ds);
            backgroundKnowledge.AddForbiddenArc(idxAge, idxCreditWorthiness);
            backgroundKnowledge.AddForcedArc(idxAge, idxProfession);
            bayesSearch.BkKnowledge = backgroundKnowledge;
            Network net3;
            try
            {
                net3 = bayesSearch.Learn(ds);
            }
            catch (SmileException)
            {
                Console.WriteLine("Bayesian Search failed");
                return;
            }
            Console.WriteLine("3rd Bayesian Search finished, structure score: {0}", 
                bayesSearch.LastScore);
            net3.WriteFile("tutorial10-bs3.xdsl");

            Network net4;
            TAN tan = new TAN();
            tan.RandSeed = 777999;
            tan.ClassVariableId = "CreditWorthiness";
            try
            {
                net4 = tan.Learn(ds);
            }
            catch (SmileException)
            {
                Console.WriteLine("TAN failed");
                return;
            }
            Console.WriteLine("Tree-augmented Naive Bayes finished");
            net4.WriteFile("tutorial10-tan.xdsl");

            PC pc = new PC();
            Pattern pattern;
            try
            {
                pattern = pc.Learn(ds);
            } catch (SmileException)
            {
                Console.WriteLine("PC failed");
                return;
            }
            Network net5 = pattern.MakeNetwork(ds);
            Console.WriteLine("PC finished, proceeding to parameter learning");
            net5.WriteFile("tutorial10-pc.xdsl");
            EM em = new EM();
            DataMatch[] matching;
            try
            {
                matching = ds.MatchNetwork(net5);
            }
            catch (SmileException)
            {
                Console.WriteLine("Can't automatically match network with dataset");
                return;
            }
            em.UniformizeParameters = false;
            em.RandomizeParameters = false;
            em.EqSampleSize = 0;
            try
            {
                em.Learn(ds, net5, matching);
            }
            catch (SmileException)
            {
                Console.WriteLine("EM failed");
                return;
            }
            Console.WriteLine("EM finished");
            net5.WriteFile("tutorial10-pc-em.xdsl");

            Console.WriteLine("Tutorial10 complete");
        }
    }
}
