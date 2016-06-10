import numpy as np
import sys

GRAPHICS=True
if GRAPHICS:
    import pygame

# pond rad
R = 400.0
duck_speed = np.pi*R
dog_speed = float(sys.argv[1])*R*np.pi
dt = 0.001
maxfps=90
size = 1000
touch_dist = 1
fudge_angle = 0.2

dog_dv = dog_speed*dt
duck_dv = duck_speed*dt

origin = np.array([size/2.0,size/2.0])

run_away=False
run_away_vec = np.array([0.0,0.0]) 

def duck_p(dog_pos,duck_pos):
    # make a dash for the edge
    # return duck_pos+duck_dv*np.array([1,0])

    # run away from dog
    #vec = duck_pos-dog_pos
    #return duck_dv*vec/np.linalg.norm(vec)

    # run from dog until we're within spitting distance of edge -- then gun it
    # vec = duck_pos-dog_pos
    # strat_chg_dist = 30
    # if np.linalg.norm(duck_pos) + strat_chg_dist >= R:
    #     theta = np.arctan2(duck_pos[1],duck_pos[0])
    #     return duck_dv*np.array([np.cos(theta),np.sin(theta)])
    # else:
    #     return duck_dv*vec/np.linalg.norm(vec)

    # try figuring out when we can beat the dog, then do above strat
    #vec = duck_pos-dog_pos
    #dog_theta = np.arctan2(dog_pos[1],dog_pos[0])
    #dog_dtheta = dog_dv/(2*np.pi*R)
    #my_theta = np.arctan2(duck_pos[1],duck_pos[0])
    #if np.linalg.norm(duck_pos) > R/15:
    #    if (R-np.linalg.norm(duck_pos))/duck_dv < np.abs(dog_theta-my_theta)/dog_dtheta - (5*touch_dist/(2*np.pi*R))/dog_dtheta:
    #        return duck_dv*np.array([np.cos(my_theta),np.sin(my_theta)])
    #    else:
    #        return duck_dv*vec/np.linalg.norm(vec)
    #else:
    #    return duck_dv*vec/np.linalg.norm(vec)
    
    # per Max's request: move towards point halfway between dog and closest point on wall
    # modified a bit, now gradually move more radially by changing average weighting. New low bound duck_speed ~ 52.
    #my_theta = np.arctan2(duck_pos[1],duck_pos[0])
    #vec1 = duck_pos-dog_pos
    #vec2 = -(duck_pos - R*np.array([np.cos(my_theta),np.sin(my_theta)]))
    
    #vec1 /= np.linalg.norm(vec1)
    #vec2 /= np.linalg.norm(vec2)

    #radf = np.linalg.norm(duck_pos)/R
    #vec3 = ((1-radf)*vec1+radf*vec2)
    #vec3 /= np.linalg.norm(vec3)
    #dog_theta = np.arctan2(dog_pos[1],dog_pos[0])
    #dog_dtheta = dog_dv/(2*np.pi*R)
    
    #if np.linalg.norm(duck_pos) > R/30:
    #    if (R-np.linalg.norm(duck_pos))/duck_dv < np.abs(dog_theta-my_theta)/dog_dtheta - (5*touch_dist/(2*np.pi*R))/dog_dtheta:
    #        return duck_dv*vec2 
    #    else:
    #        return duck_dv*vec3
    #else:
    #    return duck_dv*vec1

    # from Jonathan -- go in a cirlce at radius < R when we have a bigger thetadot than dog. When opposite dog, dash for edge
    #r = 
    #if np.linalg.norm(duck_pos) < r:
    #    return duck_dv*np.array([1,0])
    #else:
    #    if (dog_pos
    #        return duck_dv

    # actual optimal solution, similar to Jonathan's, but with different end behavior
    r=R/4.60334
    dog_theta = np.arctan2(dog_pos[1],dog_pos[0])
    my_theta = np.arctan2(duck_pos[1],duck_pos[0])
    my_dtheta = duck_dv/r

    global run_away, run_away_vec

    if run_away:
        return duck_pos+duck_dv*run_away_vec
    else:
        if np.linalg.norm(duck_pos) < r-0.1:
            return duck_pos+duck_dv*np.array([1,0])
        else:
            if -fudge_angle < np.pi + my_theta - dog_theta < 0:
                # we're basically opposite the dog, and fudged a bit to make sure dog can't backtrack
                # make a dash for the exit at 90 deg
                run_away=True
                run_away_vec[0] = -np.sin(my_theta)
                run_away_vec[1] = np.cos(my_theta)
            # go around circle
            return r*np.array([np.cos(my_theta+my_dtheta),np.sin(my_theta+my_dtheta)])





def dog_p(dog_pos,duck_pos,dog_theta,dog_dtheta):
    dtheta = np.array([0,dog_dtheta,-dog_dtheta])

    vec = [R*np.array([np.cos(dog_theta+dth),np.sin(dog_theta+dth)]) for dth in dtheta]
    

    #pick whichever way is closer to the duck
    c = np.argmin([np.linalg.norm(x-duck_pos) for x in vec])
    return vec[c],dog_theta+dtheta[c]

# these are centered at the origin, for display the origin is shifted to the center of the window
duck_pos = np.array([0.0,0.0])
dog_pos = np.array([0,R])

t=0

dog_theta = np.arctan2(dog_pos[1]-origin[1],dog_pos[0]-origin[0])
dog_dtheta = dog_dv/R

if GRAPHICS:
    pygame.init()
    screen = pygame.display.set_mode((size,size))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None,30)
done = False
duck_path = []
while not done:
    if GRAPHICS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done=True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done=True
            # other interactivity?

    duck_path.append((int((duck_pos[0]+origin[0])), int(duck_pos[1]+origin[1])))

    if GRAPHICS:
        # display stuff
        screen.fill((0,0,0))
        text = font.render("t = %6.4f"%t,True,(255,255,255))
        screen.blit(text,(20,20))
        pygame.draw.circle(screen,(0,0,255),(int(origin[0]),int(origin[1])),int(R),5)
        pygame.draw.circle(screen,(255,0,0),(int(dog_pos[0]+origin[0]),int(dog_pos[1]+origin[1])),20,0)
        pygame.draw.circle(screen,(0,255,0),(int(duck_pos[0]+origin[0]),int(duck_pos[1]+origin[1])),20,0)
        if len(duck_path) > 1:
            pygame.draw.lines(screen,(0,255,0),False,duck_path,2)

    if np.linalg.norm(duck_pos) > R:
        print("Duck wins.")
        done=True
    elif np.linalg.norm(duck_pos-dog_pos) < touch_dist:
        print("Dog wins.")
        done=True
    if t>100:
        #time out
        print("Timeout.")
        done=True
    #print("Duck pos: %6.4f %6.4f"%(duck_pos[0],duck_pos[1]))
    #print("Dog pos:  %6.4f %6.4f"%(dog_pos[0],dog_pos[1]))   
    #print("t:        %6.4f"%t)
    t+=dt 
    
    dog_pos,dog_theta = dog_p(dog_pos,duck_pos,dog_theta,dog_dtheta)
    duck_pos = duck_p(dog_pos,duck_pos)
    
    if GRAPHICS:
        pygame.display.flip()
        clock.tick(maxfps)
    
    
