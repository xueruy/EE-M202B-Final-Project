/**
 *  LightingControl
 *
 *  Copyright 2017 caiboyang
 *
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License. You may obtain a copy of the License at:
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 *  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License
 *  for the specific language governing permissions and limitations under the License.
 *
 */
definition(
    name: "LightingControl",
    namespace: "caiboyang",
    author: "caiboyang",
    description: "test",
    category: "My Apps",
    iconUrl: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience.png",
    iconX2Url: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience@2x.png",
    iconX3Url: "https://s3.amazonaws.com/smartapp-icons/Convenience/Cat-Convenience@2x.png")


// preferences {
// 	section("Title") {
// 		// TODO: put inputs here
// 	}
// }

// def installed() {
// 	log.debug "Installed with settings: ${settings}"

// 	initialize()
// }

// def updated() {
// 	log.debug "Updated with settings: ${settings}"

// 	unsubscribe()
// 	initialize()
// }

// def initialize() {
// 	// TODO: subscribe to attributes, devices, locations, etc.
// }

// // TODO: implement event handlers

preferences {
	section("Light switches to turn off") {
		input "switches", "capability.switch", title: "Choose light switches", required:true
	}
	section("Select dimmers to slowly dim...") {
    	input "dimmers", "capability.switchLevel", title: "Choose light dim", required: true
    }
	section("Turn off when there is no motion") {
		input "motionSensor", "capability.motionSensor", title: "Choose motion sensor", required:true
	}
	// section("Delay before turning off") {                    
	// 	input "delayMins", "number", title: "Second of inactivity?"
	// }
	section("Schedule") {
        input "SecTime1", "time", title: "Section 1", required: true
        input "Duration1", "number", title: "Duration 1", required: true
        input "SecTime2", "time", title: "Section 2", required: true
        input "Duration2", "number", title: "Duration 2", required: true
        input "SecTime3", "time", title: "Section 3", required: true
        input "Duration3", "number", title: "Duration 3", required: true
        input "SecTime4", "time", title: "Section 4", required: true
        input "Duration4", "number", title: "Duration 4", required: true
        input "SecTime5", "time", title: "Section 5", required: false
        input "Duration5", "number", title: "Duration 5", required: false
    }
}

def delayMins

def installed() {
	subscribe(motionSensor, "motion", motionHandler)
}

def updated() {
	unsubscribe()
	subscribe(motionSensor, "motion", motionHandler)
}

def motionHandler(evt) {
	log.debug "handler $evt.name: $evt.value"
	if(timeOfDayIsBetween(SecTime1, SecTime2, new Date(), location.timeZone)){
    	log.debug "Duration1"
		delayMins = Duration1
	}
    else if(timeOfDayIsBetween(SecTime2, SecTime3, new Date(), location.timeZone)){
    	log.debug "Duration2"
    	delayMins = Duration2
    }
    else if(timeOfDayIsBetween(SecTime3, SecTime4, new Date(), location.timeZone)){
    	log.debug "Duration1"
    	delayMins = Duration3
    }
    else if(SecTime5 == null){
    	log.debug "Duration4Sec4"
    	delayMins = Duration4
    }
    else if(timeOfDayIsBetween(SecTime4, SecTime5, new Date(), location.timeZone)){
    	log.debug "Duration4Sec5"
    	delayMins = Duration4
    }
    else{
    	log.debug "Duration5"
    	delayMins = Duration5
    }

	if (evt.value == "inactive") {
		runIn(1 * 1, scheduleCheck, [overwrite: false])
        runIn(delayMins * 1, scheduleCheck, [overwrite: false])
	}
	else{
    	log.debug "switch on to 100%"
		switches.on()
		dimmers.setLevel(100)
	}
}


def scheduleCheck() {
	log.debug "scheduled check"
	def motionState = motionSensor.currentState("motion")
    if (motionState.value == "inactive") {
        def elapsed = now() - motionState.rawDateCreated.time
    	def threshold = 1000 * 1 * delayMins - 1000
    	if (elapsed >= threshold) {
        	log.debug "off"
        	switches.off()
        } else {
        	dimmers.setLevel(20)
        	log.debug "Motion has not stayed inactive long enough since last check ($elapsed ms): do nothing"
        }
    } else {
    	log.debug "Motion is active: do nothing"
    }
}