# RV 8803 Driver

Simple driver for communicating with the the RV-8803 real time clock via I2C.

The first version of the driver has only time getting and setting functions. 

_Currently available time get functions:_
- Get miliseconds (0-99), seconds (0-59), minutes (0-59), hours (0-23), weekday (1-7, 1 is Sunday), date (1-31), month (1-12), and year (2000-2099) individually
- Get the time in format HH:MM:SS.SS
- Get the date in format DD/MM/YY
- Get the full time in DD/MM/YY - HH:MM:SS.SS

_Currently available time set functions:_
- Set seconds (0-59), minutes (0-59), hours (0-23), weekday (1-7, 1 is Sunday), date (1-31), month (1-12), and year (2000-2099) individually
- Set the time using a list of integer time values in format [{seconds}, {minutes}, {hours}]
- Set the date using a list of integer time values in format [{date}, {month}, {year}]
- Set the full time using a list of integer time values in format [{seconds}, {minutes}, {hours}, {weekday}, {date}, {month}, {year}]

_Functions to be added in the distant future:_
- Set clock output frequency
- Storing data in available RAM
- Alarm setting functions

Please contact Tran Anh Nguyen at nguyenta@umich.edu for any questions and suggestions. All communications are welcome.
