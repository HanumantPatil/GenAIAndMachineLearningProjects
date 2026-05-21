
/*
 * 
  
  Elevator System
    An elevator system is a complex mechanism that allows people to move between different floors of a building. 
    It consists of several components, including the elevator car, the hoistway, the control system, and the safety mechanisms. 
    The elevator car is the compartment that passengers enter and exit, while the hoistway is the vertical shaft through which the elevator moves. 
    The control system manages the operation of the elevator, including its movement and stopping at different floors. 
    Safety mechanisms are in place to ensure the safe operation of the elevator, such as emergency brakes and door sensors.

    --> Elevator system
    --> Elevator car    
    press button to call the elevator
    --> Hoistway
    syestem  will assing u the nearest elevator to you
    --> Control system
    enter the elevator 
    press the button for the floor you want to go to
    

1. Functional Requirements:
    - The elevator system should be able to manage multiple elevators in a building.
    - The system should assign the nearest available elevator to a user when they press the call button.
    - The system should allow users to select their desired floor once they are inside the elevator.
    - The system should ensure that the elevator stops at the correct floors and opens the doors for passengers to enter and exit safely.
    - The system should have safety mechanisms in place, such as emergency brakes and door sensors, to prevent accidents.
    - Elevator can move up and down between floors.
    - Assign Best  Elevator to user based on their location and the current position of the elevators.
    - Enter Destination floor and move the elevator to that floor.
    - Handle edge cases such as multiple users calling the elevator at the same time, or an elevator being out of service.

request:
    - Direction : Up, Down, Idle
    - Floor Number : 1, 2, 3, 4, 5, etc.
    - Elevator ID : 1, 2, 3, etc.
Should be able assign bets elevator
Should use different elevator start strategy like nearest, least busy, etc.

 
 * 
 */
