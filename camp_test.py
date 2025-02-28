####################################################################################
# Import and run CAMP test - application programming example for the camp library  #
####################################################################################

# THIS SCRIPT SHOWS HOW THE CAMP LIBRARY CAN BE USED TO GENERATE MOTION PROFILES 
# FOR A TRANSPORT TASK

from camp.planner_apf.planner_apf import run_planner2D_apf
from camp.simulation.simulation_task_2D import simulate_task2D
import camp.regression.regression_utilities as rUtils
import camp.regression.convolutional_utilities as cUtils
import json
import numpy as np


FIT_TYPE = "convolve"  # "spline" | "convolve"

### Read the JSON file with the motion planner configurations
with open(
    "C:/Users/Cameron Haas/Isochronic/CAMP_test_workspace/config/planner_config_apf0.json",
    "r",
) as file:
    planner_config_test = json.load(file)

### Read the JSON file with the carrier configurations
with open(
    "C:/Users/Cameron Haas/Isochronic/CAMP_test_workspace/scenarios/dual_transport_scenario1.json",
    "r",
) as file:
    task_config_test = json.load(file)

### Read the JSON file with the simulator configurations
with open(
    "C:/Users/Cameron Haas/Isochronic/CAMP_test_workspace/config/sim_config0.json",
    "r",
) as file:
    sim_config_test = json.load(file)

print("CAMP started with APF method.")
print("Generating motion behavior...")

### Call the planner function
(
    task_success,
    task_time,
    task_motion_description,
    task_trajectory_type,
    task_part_statuses,
) = run_planner2D_apf(planner_config=planner_config_test, task_config=task_config_test)

print("Motion planner completed with success flag: ", task_success)

### Smooth the motion description

# apply the smoothing spline approach
if FIT_TYPE == "spline":
    print("Fitting splines to motion data...")

    pos_splines, smoothed_task_motion_description, padded_task_motion_description = (
        rUtils.fit_smoothing_splines_on_pos(
            motion_description=task_motion_description,
            downsample_rate=1,
            padding_length=50, 
            clamp_length=25,
            dt=0.005,
            lam=[
                0.03,
                0.03,
                0.008,
                0.008,
                0.005,
                0.005,
                0.03,
                0.03,
                0.008,
                0.008,
                0.005,
                0.005,
            ],
            write_statistics=True,
            create_figures=True,
            output_path=planner_config_test["debug_config"]["log_output_folder"]
            + planner_config_test["debug_config"]["log_run_name"]
            + "/fitting/",
        )
    )

    print("Finished fitting splines.")

# apply the convolutional filter approach
elif FIT_TYPE == "convolve":

    a_max = np.hstack(
        (
            np.array(task_config_test["carrier0"]["q_max"])[:, 2],
            np.array(task_config_test["carrier1"]["q_max"])[:, 2],
        )
    )

    j_max = np.hstack(
        (
            np.array(task_config_test["carrier0"]["q_max"])[:, 3],
            np.array(task_config_test["carrier1"]["q_max"])[:, 3],
        )
    )

    smoothed_task_motion_description, padded_task_motion_description = cUtils.apply_convolutional_jerk_limits(
        motion_description=task_motion_description,
        dt=0.005,
        a_max=a_max, 
        j_max=j_max, 
        write_statistics=False,
        create_figures=False,
        output_path=planner_config_test["debug_config"]["log_output_folder"]
        + planner_config_test["debug_config"]["log_run_name"]
        + "/fitting/",
    )

    print("Finished applying convolutional filter.")

else:
    raise ValueError(f"Invalid FIT_TYPE {FIT_TYPE} specified")

### Call the simulator function
print("Simulating with smoothed joint profiles...")

trajectory_status = simulate_task2D(
    smoothed_task_motion_description,
    sim_config_test,
    task_config_test,
    task_trajectory_type,
    task_part_statuses,
)

print(f"Simulation completed with status code {trajectory_status}.")

print("CAMP finished.")
