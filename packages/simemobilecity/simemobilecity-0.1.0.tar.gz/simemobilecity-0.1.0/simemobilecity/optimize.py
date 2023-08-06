################################################################################
# Optimize Class                                                               #
#                                                                              #
"""Optimization class for predicting charging station placement."""
################################################################################


import sys
import copy
import random

import simemobilecity.utils as utils


class Optimize:
    """Run optimization

    Parameters
    ----------
    topo : Topology
        Topology object
    """
    def __init__(self, topo):
        # Initialize
        self._topo = topo


    ##################
    # Public Methods #
    ##################
    def run(self, file_out, traj, crit={"dist": 0.15, "occ": 0.15}, max_cp=2, min_dist=150, trials=1000):
        """Run optimization.

        Parameters
        ----------
        file_out : string
            file link for output object file
        traj : dictionary
            Simulation trajectory of the mc code - includes the **cs** and
            **dist** entry
        crit : dictionary, optional
            Critical values of failures at which to optimize charging station capacities
        max_cp : integer, optional
            Maximal number of charging stations to add to a node
        min_dist : float, optional
            Minimal distance for adding new charging stations
        trials : integer, optional
            Number of trials for choosing random node

        Returns
        -------
        cs : dictionary
            Dictionary of node ids and capacity for the charging stations
        """
        # Initialize
        num_weeks = traj["inp"]["weeks"]
        num_days = traj["cs"].get_num_days()
        num_hours = traj["cs"].get_num_hours()
        num_users = traj["cs"].get_num_users()
        num_nodes = traj["cs"].get_num_nodes()

        progress_form = "%"+str(len(str(num_nodes)))+"i"

        # Process charging station capacities
        cap = copy.deepcopy(traj["inp"]["cs"])

        # Extract failing probabilities
        extract = traj["cs"].extract(range(num_days), range(num_hours), range(num_users), is_norm=False)
        distances = traj["dist"].extract(range(num_days), range(num_hours), range(num_users), is_norm=False)

        # Warning for missing charging station capacities
        if not len(cap)==traj["cs"].get_num_nodes():
            print("Warning - Number of charging station capcity list is not equal to number of charging stations in given trajectory. Missing ones will be ignored.")

        # Run through nodes
        run_id = 0
        for node, data in extract.items():
            run_id += 1
            if node in cap.keys():
                # Calculate total number of sessions for node
                tot_sessions = data["success"]+data["fail"]["dist"]+data["fail"]["occ"]
                for failure, thresh in crit.items():
                    # Check if critical value is reached
                    fail_prob = data["fail"][failure]/tot_sessions if data["fail"][failure] else 0
                    if fail_prob > thresh:
                        # Calculate number of charging points to add
                        add_cp = int((1+fail_prob)*cap[node])
                        add_cp = add_cp if add_cp<max_cp else max_cp

                        # Occupancy optimization - Add for charging points
                        if failure=="occ":
                            # Add charging points with number of mean failures
                            cap[node] += add_cp

                        # Distance fail - Add
                        elif failure=="dist":
                            # Calculate mean failure distance
                            mean_dist = distances[node]["fail"]["dist"]/data["fail"]["dist"] if data["fail"][failure] else 0
                            # Check if mean distance is larger than given minimum
                            if mean_dist>min_dist:
                                # Get nodes within radius
                                node_r = self._topo.radius(node, mean_dist)
                                node_r_min = self._topo.radius(node, min_dist)
                                # Remove nodes within minimal distance
                                node_r = [x for x in node_r if x not in node_r_min]
                                # Check if list has elements
                                if node_r:
                                    # Run through half the number of failed attempts
                                    for i in range(int(add_cp/2)):
                                        # Iterate random choices
                                        for j in range(trials):
                                            # Choose random node
                                            node_rand = random.choice(node_r)
                                            # Check if already charginng station
                                            if node_rand not in cap.keys():
                                                # Add new charging station
                                                cap[node_rand] = 2
                                                # End trials if successfull
                                                break

            # Progress
            sys.stdout.write("Finished node "+progress_form%(run_id)+"/"+progress_form%(num_nodes)+"...\r")
            sys.stdout.flush()
        print()

        # Save trajectory
        if file_out:
            utils.save(cap, file_out)

        return cap
