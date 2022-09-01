# Industrial Control System (ICS) Monitoring Interfaces
- This project contains Python programs used to interface with ICS Programmable Logic Controllers
- Three ICS environments were constructed and montiored: Prison Cell Block, Waste Water Facility, Power Substation
- The environments were created to enable realistic ICS cyber secrity training scenarios with defender access to physical devices
- The programs monitor the PLC sensors and corresponding outputs through an arduino enabled interface (Arduino interface code not included)
- Pygame is leveraged to create a visual interface that alerts ICS engineers when there is a discrepency in sensor readings and corresponding actuator activation
- The images used to create the interface are not included in this repository for copyright reasons
- The programs will not run unless connected and exhanging IO with the Arduino enabled interface called the YBOX
- The Ybox is a Bump-In-The-Wire device that monitors all IO from the PLC to the default Human Machine Interface (HMI) and the sensors/actuators
- With the Ybox and the custom interface scripts, an engineer should be able to detect if the PLC had been tampered with to provide false outputs to the default HMI
- See publication: [CATEGORIZATION OF CYBER TRAINING ENVIRONMENTS FOR INDUSTRIAL CONTROL SYSTEMS](https://link.springer.com/chapter/10.1007/978-3-319-70395-4_13)

## Prison Cell Block
- The Python interfaces with an OMRON CP1L PLC via the Arduino YBox
- The program enables interaction much like the offical software but is parallalized for reading and lock resources to integrate with physical button presses
- The program will not run or provide an interface without the Ybox device to act as an API to the PLC

