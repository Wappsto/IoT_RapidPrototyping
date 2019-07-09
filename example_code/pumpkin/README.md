# Pumpkin example code

**NB. This example is outdated and will not work with the current version of Wappsto or the IOT creator. You can still use it for reference, but you will need to do more work by your self.**

Peripheral code for the example shown in [HacksterIO - Pumpkin Pi](https://www.hackster.io/seluxit/pumpkin-pi-5076a1)

Wappsto application for the pumpkin code: https://github.com/Wappsto/wapps/tree/master/pumpkin

Each file must be initialised in the top of the generated peripherals.py file (generated from the 'IoT Rapid Prototyping' wapp in Wappsto), and the get/set methods have to be inserted correctly.

In the folder 'finishedExamples' we've included an example file of how that might look called 'peripherals_eg.py'. Otherwise refer to the hackster.io tutorial.

Notice also that the periodical update of temperature in temperature_reader.py have to be edited with the correct names. The code is marked 'TODO' where they need to be updated. In your generated code, find the file 'uuid_defines.py' to check the names generated based on your input in the 'IoT Rapid Prototyping' tool. 

Finally, at the top of the temparature_reader.py file, enter the actual id of your thermometer. If you've followed the hackster.io tutorial, you will find that under /sys/bus/w1/devices. 

In the folder 'finishedExamples' we've also included an example file of how that might look called 'temparature_reader_eg.py. Otherwise refer again to the hackster.io tutorial.
