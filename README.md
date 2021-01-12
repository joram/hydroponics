# hydroponics

## Parts

### Hardware
| Item | link | cost (CAD) | quantity |
|------|------|------------|----------|
| pump                | [aliexpress](https://www.aliexpress.com/item/4001120373120.html)    | 5.41  | x1 |
| a bucket            | [home depot](https://www.uline.ca/Product/Detail/S-7914O/Pails/Plastic-Pail-5-Gallon-Orange) | 7.55 | x1 |
| specimen container  | [amazon.ca](https://www.amazon.ca/Lees-Convalescent-Home-Specimen-Container/dp/B0002APRLK/ref=sr_1_1) | 24. 31 | x1 |

### Electronics
| Item | link | cost (CAD) | quantity |
|------|------|------------|----------|
| conductivity sensor | [aliexpress](https://www.aliexpress.com/item/4001344672810.html)    | 36.65 | x1 |
| liquid PH sensor    | [aliexpress](https://www.aliexpress.com/item/1005001286188891.html) | 12.79 | x1 |
| float sensor        | [aliexpress](https://www.aliexpress.com/item/1005001733151705.html) | 1.57  | x1 |
| temperature sensor  | [aliexpress](https://www.aliexpress.com/item/4000068914916.html)    | 2.17  | x1 |
| peristaltic pumps   | [adafruit](https://www.adafruit.com/product/1150) | 24.95 | x3 |
| raspberry pi zero   | [adafruit](https://www.adafruit.com/product/3409) | 24.50 | x1 |
| relay               | [banggood](https://usa.banggood.com/1-Channel-5V-Relay-Control-Module-Low-Level-Trigger-Optocoupler-Isolation-p-1556669.html) | 2.57 | x4 |

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
