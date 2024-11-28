import pysmile

# Tutorial10 loads Credit10k.csv file
# and runs multiple structure learning algorithms
# using the loaded dataset.
# Use the link below to download the Credit10k.csv file:
# https://support.bayesfusion.com/docs/Examples/Learning/Credit10K.csv

class Tutorial10:
    def __init__(self):
        print("Starting tutorial10...")
        ds = pysmile.learning.DataSet()
        try:
            ds.read_file("Credit10k.csv")
        except pysmile.SMILEException:
            print("Dataset load failed")
            return
        print(f"Dataset has {ds.get_variable_count()} variables (columns) " 
            + f"and {ds.get_record_count()} records (rows)")
        bayes_search = pysmile.learning.BayesianSearch()
        bayes_search.set_iteration_count(50)
        bayes_search.set_rand_seed(9876543)
        try:
            net1 = bayes_search.learn(ds)
        except pysmile.SMILEException:
            print("Bayesian Search failed")
            return
        print(f"1st Bayesian Search finished, structure score: {bayes_search.get_last_score()}")
        net1.write_file("tutorial10-bs1.xdsl")

        bayes_search.set_rand_seed(3456789)
        try:
            net2 = bayes_search.learn(ds)
        except pysmile.SMILEException:
            print("Bayesian Search failed")
            return
        print(f"2nd Bayesian Search finished, structure score: {bayes_search.get_last_score()}")
        net2.write_file("tutorial10-bs2.xdsl")

        idx_age = ds.find_variable("Age")
        idx_profession = ds.find_variable("Profession")
        idx_credit_worthiness = ds.find_variable("CreditWorthiness")

        if idx_age < 0 or idx_profession < 0 or idx_credit_worthiness < 0:
            print("Can't find dataset variables for background knowledge")
            print("The loaded file may not be Credit10k.csv")
            return
        background_knowledge = pysmile.learning.BkKnowledge()
        background_knowledge.match_data(ds)
        background_knowledge.add_forbidden_arc(idx_age, idx_credit_worthiness)
        background_knowledge.add_forced_arc(idx_age, idx_profession)

        bayes_search.set_bk_knowledge(background_knowledge)
        try:
            net3 = bayes_search.learn(ds)
        except pysmile.SMILEException:
            print("Bayesian Search failed")
            return
        print(f"3rd Bayesian Search finished, structure score: {bayes_search.get_last_score()}")
        net3.write_file("tutorial10-bs3.xdsl")

        tan = pysmile.learning.TAN()
        tan.set_rand_seed(777999)
        tan.set_class_variable_id("CreditWorthiness")
        try:
            net4 = tan.learn(ds)
        except pysmile.SMILEException:
            print("TAN failed")
            return
        print("Tree-augmented Naive Bayes finished")
        net4.write_file("tutorial10-tan.xdsl")

        pc = pysmile.learning.PC()
        try:
            pattern = pc.learn(ds)
        except pysmile.SMILEException:
            print("PC failed")
            return
        net5 = pattern.make_network(ds)
        print("PC finished, proceeding to parameter learning")
        net5.write_file("tutorial10-pc.xdsl")
        em = pysmile.learning.EM()
        try:
            matching = ds.match_network(net5)
        except pysmile.SMILEException:
            print("Can't automatically match network with dataset")
            return
        em.set_uniformize_parameters(False)
        em.set_randomize_parameters(False)
        em.set_eq_sample_size(0)
        try:
            em.learn(ds, net5, matching)
        except pysmile.SMILEException:
            print("EM failed")
            return
        print("EM finished")
        net5.write_file("tutorial10-pc-em.xdsl")

        print("Tutorial10 complete.")
