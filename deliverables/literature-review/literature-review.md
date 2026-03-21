# How can UAV swarm AI be used in search and rescue operations: A literature review.

## Introduction

In recent years there has been an increase in the use of Unmanned Aerial Vehicles (UAV) in search and rescue (SAR) operations (Ops). Compared to human SAR personel a single human piloted UAV can search an area quickly, cheap and without endangering SAR personnel. Using a swarm of UAV's for SAR Ops might offer an even bigger advantage. This literature review aims to provide a basis for technical research and to answer the question: "How can UAV swarm AI be used in search and rescue operations?" To answer this question research has been divided into multiple sub questions.

- What is drone swarm AI?
    - What is a drone?
    - What is swarm AI?
- What are search and rescue operations (SAR Ops)?
- How are drones currently used in SAR Ops?
    - What are the constraints of a drone in SAR Ops?
    - How does a drone detect a target?
    - How does a rescuer receive information from a drone?
- How do drones form a swarm AI?
    - How does a drone cummunicate with another drone?
    - How can the position of a drone relative to ... be determined?
        - the environment
        - another drone
    - Which computations are deployed where?
- What is an easily deployable and fast navigation/exploration algorithm for multiple explorers?
- What are the constraints of a drone swarm AI in SAR Ops?
- How can a drone swarm AI detect a target?
    - How can a drone swarm AI not detect the same target as multiple seperate targets 
- How can a drone swarm ... a central intelligent system and rescuer?
    - receive instructions from
    - relay relevant information to

## Key concepts

### UAV

A UAV, commonly referred to as drone is an aircraft that can fly without a pilot onboard. For this literature review it is important to make a distinction between different types of drones and what function they are best used for. Another factor is the legal requirements for operating each type of drone. Requirements and regulations will not be explored further in this review but they will be used for drone classification. The European Union Aviation Safety Agency (EASA) classifies drones based on maximum take of mass (MTOM, the total weight of the drone) and function.

- 'Open' category - low risk [[1](https://www.easa.europa.eu/en/domains/drones-air-mobility/operating-drone/open-category-low-risk-civil-drones)]
    - The 'open' category is the main reference for the majority of leisure drone activities and low-risk commercial activities.
    - <img src="./images/open-drone-categories.png" alt="open category table">
- Specific category - medium risk [[2](https://www.easa.europa.eu/en/domains/drones-air-mobility/operating-drone/specific-category-civil-drones)]
    - BVLOS – Beyond Visual Line Of Sight
    - When using a drone with MTOM > 25 kg
    - flying higher than 120m above ground level
    - when dropping material
    - when operating drone in an urban environment with a MTOM> 4 kg or without a class identification label
- Certified category - high risk [[3](https://www.easa.europa.eu/en/domains/drones-air-mobility/operating-drone/certified-category-civil-drones)]
    - International unmanned cargo aircraft flight
    - Rural or urban drone operations using pre-defined routes carrying passengers or cargo

The EASA also categorises drones based on how they fly. [[4](https://www.easa.europa.eu/en/domains/drones-air-mobility/drones-evtol-designs)]

- A fixed-wing drone is essentially a drone with aerodynamic wings that remain fixed during flight for passive lift, similar to a regular airplane. They can stay in the air longer, carry heavier payloads, and exhibit better power efficiency. Control surfaces built into the wing (such as rudders, elevators, and ailerons) enable rotation around three perpendicular axes: vertical (yaw), lateral (pitch), and longitudinal (roll).
- A single-rotor drone (also known as a single-rotor helicopter or gyroplane) features a single large rotor for lift and propulsion. Similar to traditional helicopters, it has a smaller tail rotor to maintain stability and control yaw movement. Single-rotor drones can stay in the air longer and carry heavier payloads compared to multi-rotor designs
- Multi-rotor drones have more than two rotors. They are versatile and widely used for various applications, including mapping, surveillance, and photography.
- Lift and Cruise / Vectored Thrust drones (also known as hybrid drones) feature a combination of rotors and fixed wing and thus merge the benefits of both, offering both endurance and vertical capabilities. This may be achieved by tilting rotors (“vectored thrust”) or independent sets of rotors that point in different directions (“lift and cruise”).

### Swarm AI

A drone swarm is a group of drones that operates in a coordinated manner for: path planning, task assignment, formation control, etc. The collaboration of multiple drones is heavily inspired by nature. In a colony of ants or a hive of bees tasks are assigned to each individual. In a flock of birds each bird uses a very simple set of rules to maintain formation. The rise of Artificial Intelligence (AI) and Machine Learning (ML) can elevate drone swarms to an even more complex level of coordination that goes beyond following basic programs. [[5](https://www.iiisci.org/journal/PDV/sci/pdfs/SA882GF25.pdf)],[[6](https://link.springer.com/article/10.1186/s44147-025-00582-3)]

### SAR Ops

**Search**: An operation normally coordinated by a rescue coordination centre or rescue subcentre using available personnel and facilities to locate persons in distress. [[7](https://www.pilot18.com/wp-content/uploads/2017/10/Pilot18.com-ICAO-Annex-12-Search-and-Rescue.pdf)]

**Rescue**: An operation to retrieve persons in distress, provide for their initial medical or other needs, and deliver them to a place of safety.  [[7](https://www.pilot18.com/wp-content/uploads/2017/10/Pilot18.com-ICAO-Annex-12-Search-and-Rescue.pdf)]

## Technical Research

- materials
    - 1 x Loco Swarm bundle - Crazyflie 2.1+
        - 8 x Loco positioning nodes
        - 10 x Loco positioning deck
        - 10 x Crazyflie 2.1+
        - 3 x Crazyradio 2.0
        - 20 x 350mAh LiPo battery
        - 10 x 500mA LiPo USB charger
    - 8 x AI deck 1.1
    - 8 x Flow deck v2
    - a central computation unit (computer, laptop, raspberry pi)
    - a screen for frontend information (included in computation device or seerate in case of raspberry pi)
- Crazyflie sepcs/limitations
    - controllable range = 1km -> maximum perimeter is circle where r = 1km
    - drone body size = 7cm x 7cm
    - average drone fly time 7 minutes
    - recommended to not fly outdoors
    - controllable by
        - on device programming/instructions
        - controller based
        - phone based
        - radio based
    - danger of hitting obstacles, walls
- location
    - large indoor space with no obstacles (like: Kortrijk sports centre, Kortrijk expo, Depart kortrijk, Bruges sportsinnovation campus, Kortrijk weide parking 3 storage unit and maybe Kortrijk weide energy lab)
- target
    - recgonlizable object (like: trafic cone or sports cones)
    - human (acting in distress)
- proof of concept
    - a rescuer uses a frontend app to ... with the predifined materials at a predifined location-like
        - set a searchable perimeter
        - set a number of missing targets
        - send out the drone swarm to search the missing targets withtin the searchable perimeter
        - recall the drone swarm
        - receive information from the central compute instance
    - the central compute instance
        - houses the frontend application
        - houses the navigation/exploration algorithm for multiple explorers
        - receives ...
            - the drones' locations
            - found targets' locations
            - drone images of the found targets'
            and uses this information to
            - display in the frontend app
            - make new navigation/movement decisions
        - sends
            - instructions to the drones on where to move
    - a drone in the swarm
        - receives instructions from the central compute instance
        - runs an ai model to detect targets using the ai deck
            - it inspects a certain area with it's camera
        - runs the flow deck software to determine it's postion based on movement
        - (extra) communcates with other drones for better relative positioning

## List + summary of similar studies (their approach, technological choices, etc.).

## Required technologies of my use case

## Comparison of technology choices: strengths and weaknesses.

## Extensive discussion of the (new) technology you will use.

### what could be different under different material constraints

## Sources

1. https://www.easa.europa.eu/en/domains/drones-air-mobility/operating-drone/open-category-low-risk-civil-drones
2. https://www.easa.europa.eu/en/domains/drones-air-mobility/operating-drone/specific-category-civil-drones
3. https://www.easa.europa.eu/en/domains/drones-air-mobility/operating-drone/certified-category-civil-drones
4. https://www.easa.europa.eu/en/domains/drones-air-mobility/drones-evtol-designs
5. https://www.iiisci.org/journal/PDV/sci/pdfs/SA882GF25.pdf (abstract)
6. https://link.springer.com/article/10.1186/s44147-025-00582-3 (abstract)
7. https://www.pilot18.com/wp-content/uploads/2017/10/Pilot18.com-ICAO-Annex-12-Search-and-Rescue.pdf (page 11)

PS

nog te gebruiken
- https://www.sciencedirect.com/science/article/pii/S2212420925000238
- https://www.sciencedirect.com/science/article/pii/S095741742100378X
- https://www.mdpi.com/2072-4292/15/13/3266
- file:///home/roel/Downloads/978-981-15-5827-6_33.pdf