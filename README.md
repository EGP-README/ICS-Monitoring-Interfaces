# Industrial Control System (ICS) Monitoring Interfaces
- This project contains Python programs used to interface with ICS Programmable Logic Controllers
- The programs monitor the PLC sensors and corresponding outputs through an arduino enabled interface (Arduino interface code not included)
- Pygame is leveraged to create a visual interface that alerts ICS engineers when there is a discrepency in sensor readings and corresponding actuator activation
- The images used to create the interface are not included in this repository for copyright reasons
- The programs will not run unless connected and exhanging IO with the Arduino enabled interface called the YBOX
- The Ybox is a Bump-In-The-Wire device that monitors all IO from the PLC to the default Human Machine Interface (HMI) and the sensors/actuators
- With the Ybox and the custom interface scripts, an engineer should be able to detect if the PLC had been tampered with to provide false outputs to the default HMI

