package tutorials;

import smile.*;
import smile.learning.*;

// Tutorial9 loads Credit10k.csv file
// and runs multiple structure learning algorithms
// using the loaded dataset.
// Use the link below to download the Credit10k.csv file:
// https://support.bayesfusion.com/docs/Examples/Learning/Credit10K.csv

public class Tutorial10 {
    public static void run() {
        System.out.println("Starting Tutorial9...");
        DataSet ds = new DataSet();
        try
        {
            ds.readFile("Credit10k.csv");
        } catch (SMILEException ex)
        {
            System.out.println("Dataset load failed");
            return;
        }
        System.out.printf("Dataset has %d variables (columns) and %d records (rows)\n", 
            ds.getVariableCount(), ds.getRecordCount());
        BayesianSearch bayesSearch = new BayesianSearch();
        bayesSearch.setIterationCount(50);
        bayesSearch.setRandSeed(9876543);
        Network net1;
        try
        {
            net1 = bayesSearch.learn(ds);
        } catch (SMILEException ex)
        {
            System.out.println("Bayesian Search failed");
            return;
        }
        System.out.printf("1st Bayesian Search finished, structure score: %f\n", 
            bayesSearch.getLastScore());
        net1.writeFile("tutorial9-bs1.xdsl");

        Network net2;
        bayesSearch.setRandSeed(3456789);
        try
        {
            net2 = bayesSearch.learn(ds);
        }
        catch (SMILEException ex)
        {
            System.out.println("Bayesian Search failed");
            return;
        }
        System.out.printf("2nd Bayesian Search finished, structure score: %f\n", 
            bayesSearch.getLastScore());
        net2.writeFile("tutorial9-bs2.xdsl");

        int idxAge = ds.findVariable("Age");
        int idxProfession = ds.findVariable("Profession");
        int idxCreditWorthiness = ds.findVariable("CreditWorthiness");
        if (idxAge < 0 || idxProfession < 0 || idxCreditWorthiness < 0)
        {
            System.out.println("Can't find dataset variables for background knowledge");
            System.out.println("The loaded file may not be Credit10k.csv");
            return;
        }

        BkKnowledge backgroundKnowledge = new BkKnowledge();
		backgroundKnowledge.matchData(ds);
        backgroundKnowledge.addForbiddenArc(idxAge, idxCreditWorthiness);
        backgroundKnowledge.addForcedArc(idxAge, idxProfession);
        bayesSearch.setBkKnowledge(backgroundKnowledge);
        Network net3;
        try
        {
            net3 = bayesSearch.learn(ds);
        }
        catch (SMILEException ex)
        {
            System.out.println("Bayesian Search failed");
            return;
        }
        System.out.printf("3rd Bayesian Search finished, structure score: %f\n", 
            bayesSearch.getLastScore());
        net3.writeFile("tutorial9-bs3.xdsl");

        Network net4;
        TAN tan = new TAN();
        tan.setRandSeed(777999);
        tan.setClassVariableId("CreditWorthiness");
        try
        {
            net4 = tan.learn(ds);
        }
        catch (SMILEException ex)
        {
            System.out.println("TAN failed");
            return;
        }
        System.out.println("Tree-augmented Naive Bayes finished");
        net4.writeFile("tutorial9-tan.xdsl");

        PC pc = new PC();
        Pattern pattern;
        try
        {
            pattern = pc.learn(ds);
        } catch (SMILEException ex)
        {
            System.out.println("PC failed");
            return;
        }
        Network net5 = pattern.makeNetwork(ds);
        System.out.println("PC finished, proceeding to parameter learning");
        net5.writeFile("tutorial9-pc.xdsl");
        EM em = new EM();
        DataMatch[] matching;
        try
        {
            matching = ds.matchNetwork(net5);
        }
        catch (SMILEException ex)
        {
            System.out.println("Can't automatically match network with dataset");
            return;
        }
        em.setUniformizeParameters(false);
        em.setRandomizeParameters(false);
        em.setEqSampleSize(0);
        try
        {
            em.learn(ds, net5, matching);
        }
        catch (SMILEException ex)
        {
            System.out.println("EM failed");
            return;
        }
        System.out.println("EM finished");
        net5.writeFile("tutorial9-pc-em.xdsl");

        System.out.println("Tutorial10 complete");
    }
}
