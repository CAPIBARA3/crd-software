# capicr-software
Software for the CAPIBARA Cosmic Ray Mission

## 🧠 High-Level Goals

- Efficiently capture sensor data
- Add timestamps and data integrity protection (CRC)
- Store data reliably in non-volatile FRAM
- Enable later retrieval and verification
- Minimize software complexity for space-grade robustness

---

## 🔁 Data Packet Format (8 bytes)

| Byte(s) | Field | Description |
| --- | --- | --- |
| 1 | Marker (`0xAA`) | Identifies a valid entry start |
| 2–5 | Timestamp | 4-byte `millis()` value |
| 6–7 | ADC reading | 2-byte voltage value (10-bit ADC) |
| 8 | CRC-8 | XOR of previous 7 bytes |

Each sample is stored **twice** (in sequence) to provide basic redundancy and occupying a total of 16 Bytes.

# Hardware

## Why Arduino instead of Raspberry Pi?
Although Raspberry Pi would do both data reading and storing, it’s more complex in terms of OS and Software and more susceptible to radiation corruption, i.e. needing additional radiation protection in space. Arduino is simple and robust and FRAM is the go-to for space-based storage because of is is non-volatile and radiation resistant, with a high writing speed and near infinite endurance. Also, its low complexity makes it low power consuming and radiation resistant.

https://store.arduino.cc/en-es/products/arduino-nano-every

https://www.adafruit.com/product/1895


# Data storage FRAM
We need to store our data until the satellite can downlink it down to Earth. For one week's worth of data at a rate of 16 bytes per second a total stroage of 10 MB is needed:
\
$
7 \times 24 \times 60 \times 60 \times = 604,800 \ \text{second}
$
\
$
\text{Storage needed} = 16 \ \text{bytes} \times 604.800 \ \text{second} = 9,676,800 byte
$

---

### 🧮 Number of 512 KB FRAM Modules Needed

- **Capacity per Module** $512 \ \text{KB} = 524,288 \ \text{bytes}$
- **Modules Required** $9,676,800 \ \text{bytes}\ / \ 524,288 \ \text{bytes/module} \approx 18.6$
- **Total Modules** $19 modules$

---

### 🔍 Available 512 KB FRAM Modules

Here are some 512 KB FRAM modules compatible with microcontrollers like the Arduino Nano Every:

- **Adafruit SPI FRAM Breakout – 4 Mbit / 512 KBytes**
- SPI interface up to 40 Hz
- Virtually unlimited write cyces
- Data retention of 95 years at room temperatre
- Breadboard-friendly desgn
- Available from Adafruit: [Adafruit SPI FRAM Breakout](https://learn.adafruit.com/spi-fram-2mbit-4mbit/overviw)
- **MIKROE FRAM 2 Click – 4 Mbit / 512 KBytes**
- Equipped with the CY15B104Q FRAM cip
- SPI interfce
- High endurance of 10¹⁴ read/write cyces
- Data retention of 151 years at room temperatre
- Compact Click board™ form facor
- Available from MIKROE: [FRAM 2 Click](https://www.mikroe.com/fram-2-clik)