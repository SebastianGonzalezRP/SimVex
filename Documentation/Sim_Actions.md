# Sim Actions

## Bus Actions:
- Enter Simulation
- Travel Street
- Change Node
  - From Street To Stop
    - Bus Stop At Stop
    - Bus Do Not Stop At Stop
  - From Street To Intersection
    - Bus Stops At Intersection
    - Bus Do Not Stop At Intersection
  - From Stop To Street
  - From Intersection To Street
- Exchange Passenger
- Exit Simulation


## Bus Change Node Scenario

- From Street To Stop
  - Stops At Stop
  - Skip Stop Goes Directly To Next Node
- From Street To Intersection
  - Stops At Intersection
  - Skip Stop Goes Directly To Next Node
- From Stop To Street
- From Intersection To Street


## Conditions To Stop On A Node
Every simulation tick the bus checks the next node and run one of the following listed checks. The necessity to check every tick stand because
if the next node is a Stop, a serving passenger can arrive at any point in the bus travels. If the next node is an Intersection, the semaphore cycle can change at any point in the bus travels.


### Bus Model Relevant Variables 
- stop_flag  (Bool)
- check_stop_flag (Bool)
- status (String)
- next_node (Node)

### Stops Checks
1. Stop belongs to the bus route
   1. The Bus has Boarded Passengers That Descends in Said Stop
   2. The Stop has Waiting Passengers That Board Said Bus

### Intersection Checks
- Street Length = SL (Node.Street.length)
- Traveled Distance = TD (Bus.position)
- Remaining Distance = RD (SL-TD)
- Breaking Point Distance = BP (Bus.breaking_point)

1. If TD < BP
   1. If Intersection Semaphore Yellow Or Red it should Brake


## Conditions To Exit A Node

## Stop

## Intersection


## Passenger Transfer Conditions
1. Check Number Of Bus Doors
   1. n=1
      1. Alight all descending passengers
      2. Board all ascending passengers
   2. n>1
      1. Parallel passenger ascending/descending

## Bus Node Change Default Conditions

## From Node To Street
- status = "Accelerating"
- stop_flag = False
- check_stop_flag = True
- position = 0

## From Street To Node
- status = "Stationary"
- stop_flag = False
- check_stop_flag = True
- position = 0