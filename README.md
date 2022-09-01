# Industrial Control System (ICS) Simulation and Monitoring Interfaces
- This project contains Python programs used to interface with ICS Programmable Logic Controllers
- Three ICS environments were constructed and montiored: Prison Cell Block, Waste Water Facility, Power Substation
- The environments were created to enable realistic ICS cyber secrity training scenarios with defender access to physical devices
- Pygame is leveraged to create a visual interface that alerts ICS engineers when there is a discrepency in sensor readings and corresponding actuator activation
- The images used to create the interface are not included in this repository for copyright reasons
- The programs will not run unless connected and exhanging IO with the Arduino enabled interface called the Ybox (code not included in this repo)
- The Ybox is a Bump-In-The-Wire device that monitors all IO from the PLC to the default Human Machine Interface (HMI) and the sensors/actuators
- With the Ybox and the custom interface scripts, an engineer should be able to detect if the PLC had been tampered with to provide false outputs to the default HMI
- See publication: [CATEGORIZATION OF CYBER TRAINING ENVIRONMENTS FOR INDUSTRIAL CONTROL SYSTEMS](https://link.springer.com/chapter/10.1007/978-3-319-70395-4_13)

## Prison Cell Block
- The Python interfaces with an OMRON CP1L PLC via the Arduino YBox
- The program enables interaction much like the offical software but is parallalized for reading and lock resources to integrate with physical button presses
- The program will not run or provide an interface without the Ybox device to act as an API to the PLC

## Wastewater Treatment Facility 
- Interfaces with an Allen-Bradley ControlLogix PLC and a PowerFlex 40 AC Variable Frequency Drive
- Simulates the regulation of oxygen flow for the facility through blower fans and oxygen vlaves
- Provides engineer interface and alerts if oxegen thresholds are not met

## Power Substation
- Interfaces with SEL-751A Feeder Protection Relay and a Schneider Electric PowerLogic PM5300 Power and Energy Meter
- Displays the status of the power substation and detects discrepencies in PLC or portection relay readings
