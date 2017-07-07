import numpy as np
import random

# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    
    #Record starting point of rover so we can return there after all samples collected
    if Rover.start_pos is None:
        Rover.start_pos = Rover.pos
    
    #if all samples are found, return to starting location
    if Rover.samples_located == 6 and Rover.samples_collected == 6:
        print("Congrats, Good job! All rocks are found and collected")
        Rover.throttle = 0
        Rover.brake = Rover.brake_set

    #Check if there are any rocks visible
    elif Rover.rock_map.any()== True and len(Rover.rock_ang) > 0:
        print('Rock I am here')
        print(Rover.rock_dists)
        if Rover.near_sample:
            Rover.brake = 10
        elif Rover.vel > 0.5:
            Rover.throtte = 0
        elif Rover.vel < 0.5:
            Rover.throttle = Rover.throttle_set
        #if there is a rock, move towards it
        Rover.steer = np.clip(np.mean(Rover.rock_ang * 180/np.pi), -15, 15)

    elif Rover.nav_angles is not None:
        # Check for Rover.mode status
        if Rover.mode == 'forward': 
            # Check the extent of navigable terrain
            if len(Rover.nav_angles) >= Rover.stop_forward:  
                # If mode is forward, navigable terrain looks good 
                # and velocity is below max, then throttle
                if Rover.vel < Rover.max_vel:
                    # Set throttle value to throttle setting
                    Rover.throttle = Rover.throttle_set
                else: # Else coast
                    Rover.throttle = 0
                Rover.brake = 0
                # Set steering to average angle clipped to the range +/- 15
                if random.random() > 0.02:
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi) +15, -15, 15)
                else:
                    Rover.mode = 'random'
            # If there's a lack of navigable terrain pixels then go to 'stop' mode
            elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                    Rover.throttle = 0
                    # Set brake to stored brake value
                    Rover.brake = Rover.brake_set
                    Rover.steer = 0
                    Rover.mode = 'stop'

        # If we're already in "stop" mode then make different decisions
        elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
            if Rover.vel > 0.2:
                Rover.throttle = 0
                Rover.brake = Rover.brake_set
                Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
            elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                if len(Rover.nav_angles) < Rover.go_forward:
                    Rover.throttle = 0
                    # Release the brake to allow turning
                    Rover.brake = 0
                    # Turn range is +/- 10 degrees, when stopped the next line will induce 4-wheel turning
                    Rover.steer = -10 #
                # If we're stopped but see sufficient navigable terrain in front then go!
                if len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                    Rover.throttle = Rover.throttle_set
                    # Release the brake
                    Rover.brake = 0
                    # Set steer to mean angle
                    Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi)+15, -15, 15)
                    Rover.mode = 'forward'
        elif Rover.mode == 'random':
            if random.random() > 0.9:
                Rover.mode = 'forward'
            else:
                Rover.throttle = 0
                Rover.brake = 0
                Rover.steer = -5
    
    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0
        
    # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True
    
    return Rover

