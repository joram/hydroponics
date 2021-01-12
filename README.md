# hydroponics

## Parts
[here](./docs/parts.md)

## Construction
- sensors in the specimen container
- specimen container in the bucket
- nutrients/ph-adjustments pumps aimed into the bucket
- circulating pump pumping under the plants
- plants draining into the specimen container

### Electronics
- wire each sensor to the pi
- wire peristaltic pumps to the pi (via relays)
- plug circulating plug into wall
- plug lights into timer into wall

### Software
- balance PH with two inputs (`PH up` and `PH down`)
  - a min-max acceptable range can be set (peppers = 6.0-6.5)
  - if the ph is above the acceptable range, `PH down` is added every 5min
  - if the ph is below the acceptable range, `PH up` is added every 5min
    

- balance nutrients with one input (nutrients)
  - a single threshold for conductivity can be set
  - the value will be calibrated based off the nutrients instructions
  - if the conductivity is below the threshold, nutrients is added every 5min
    
    
- alert for reservoir being low
  - if the float sensor doesn't float, an alert will be sent
