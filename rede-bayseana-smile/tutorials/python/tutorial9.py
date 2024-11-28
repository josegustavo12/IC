import pysmile

# Tutorial9 loads HeparII.xdsl file
# and runs multiple diagnostic algorithms
# Use the link below to download the HeparII.xdsl file:
# https://support.bayesfusion.com/docs/Examples/Discrete%20Bayesian%20Networks/HeparII.xdsl

class Tutorial9:
    def __init__(self):
        print("Starting tutorial 9...")
        net = pysmile.Network()
        net.read_file("HeparII.xdsl")
        print("Hepar model loaded")
        print_diag_types(net)

        print("Creating diagnostic network object")
        diag = pysmile.DiagNetwork(net)
        print_fault_indices(diag)

        pursued_fault_idx = diag.get_pursued_fault()
        print(f"The default (most likely) pursued fault is at index {pursued_fault_idx}: " 
              + f"{diag.get_fault_node_id(pursued_fault_idx)}" 
              + f"={diag.get_fault_outcome_id(pursued_fault_idx)}")
        
        print("Running diagnosis with no instantiated observations")
        diag_results = diag.update() 
        print_diag_results(net, diag_results)

        print("Running diagnosis with three observations")
        diag.instantiate_observation("jaundice", "present")
        diag.instantiate_observation("nausea", "absent")
        diag.instantiate_observation("obesity", "present")
        diag_results = diag.update() 
        print_diag_results(net, diag_results)

        print("Running diagnosis with two observations and focusing on Hyperbilirubinemia")
        diag.release_observation("nausea")
        diag.instantiate_observation("obesity", "absent")
        hyperbilirubinemia_idx = diag.get_fault_index("Hyperbilirubinemia", "present")
        diag.set_pursued_fault(hyperbilirubinemia_idx)
        diag_results = diag.update() 
        print_diag_results(net, diag_results)

        print("Switching algorithm to cross-entropy, observations and pursued fault unchanged")
        diag.set_single_fault_algorithm(pysmile.SingleFaultAlgorithmType.CROSSENTROPY)
        diag_results = diag.update() 
        print_diag_results(net, diag_results)
    
        print("Running diagnosis with two observations and "
            + "focusing on both Hyperbilirubinemia and Steatosis")
        steatosis_idx = diag.get_fault_index("Steatosis", "present")
        diag.set_pursued_faults([steatosis_idx, hyperbilirubinemia_idx])
        diag_results = diag.update() 
        print_diag_results(net, diag_results)
        
        print("Swtiching algorithm to L2 distance, observations and pursued faults unchanged")
        diag.set_multi_fault_algorithm(pysmile.MultiFaultAlgorithmType.L2_NORMALIZED_DISTANCE)
        diag_results = diag.update() 
        print_diag_results(net, diag_results)

        print("Tutorial 9 complete.")            

def print_diag_types(net):
    print(f"Network has {net.get_node_count()} nodes")
    print("{:<20} {:<30} {:<30}".format("Node Id", "Diagnostic Type", "Fault Outcomes"))
    for node_id in net.get_all_node_ids():
        diag_type = net.get_node_diag_type(node_id)
        fault_outcomes = []
        if diag_type == pysmile.NodeDiagType.FAULT:
            for outcome_id in net.get_outcome_ids(node_id):
                if net.is_fault_outcome(node_id, outcome_id):
                    fault_outcomes.append(outcome_id)
        print("{:<20} {:<30} {:<30}".format(node_id, str(net.get_node_diag_type(node_id)), 
            str(fault_outcomes) if diag_type == pysmile.NodeDiagType.FAULT else "n/a"))

def print_fault_indices(diag):
    fault_count = diag.get_fault_count()
    print(f"Diagnostic network has {fault_count} faults (node/outcome pairs)")
    print("{:<12} {:<20} {:<20}".format("Fault Index", "Fault Node Id", "Fault Outcome Id"))
    for fidx in range(fault_count):
        print("{:<12} {:<20} {:<20}".format(
            fidx, diag.get_fault_node_id(fidx), diag.get_fault_outcome_id(fidx)))

def print_fault_info(net, fault):
    print("{:<20} {:<20} {:<24} {:<8}".format(
        net.get_node_id(fault.node), net.get_outcome_id(fault.node, fault.outcome),
        fault.probability, "Yes" if fault.is_pursued else "No"))

def print_observation_info(net, observation):
    print("{:<20} {:<24} {:<8} {:<20}".format(net.get_node_id(observation.node), 
        observation.measure, observation.cost, observation.info_gain))

def print_diag_results(net, diag_results):
    print("Diag results start\n\nFaults:")
    print("{:<20} {:<20} {:<24} {:<8}".format(
        "Node Id", "Outcome Id", "Probability", "Is Pursued"))
    for fault_info in diag_results.faults:
        print_fault_info(net, fault_info)
    print("\nObservations:")
    print("{:<20} {:<24} {:<8} {:<20}".format("Node Id", "Measure", "Cost", "InfoGain"))
    for observation_info in diag_results.observations:
        print_observation_info(net, observation_info)
    print("\nDiag results end\n")
