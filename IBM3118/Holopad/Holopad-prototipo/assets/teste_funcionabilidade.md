# Functionality Test Report: Holopad

## Test #1: Ideal Illumination (Solar)

**Conditions:** Balcony with glass windows in the afternoon (diffused sunlight).  
**Luminosity (Lux):** `624 Lux`

| Functionality | Result | Observations |
| :--- | :---: | :--- |
| **General Detection** | Excellent | Immediate and 100% stable detection (no "jitter"). |
| **Pointing (Move)** | Excellent | Perfectly fluid and responsive movement. |
| **Visual Feedback** | OK | All status colors (Blue, Yellow, Red) corresponded. |
| **Left Click** | Excellent (10/10) | Total accuracy, no false positives. |
| **Freeze** | Excellent | Froze at the exact moment of the click intention. |
| **Drag** | Excellent | Maintained the pressed click without failure. |
| **Right Click** | Excellent (10/10) | Distinct gesture, no conflicts. |
| **Scroll (3 Fingers)** | Excellent | Immediate detection, smooth scrolling. |
| **Stop Gesture** | Immediate | Worked on the first try. |

### General Summary of Test #1  
**Analysis:** Perfect lighting condition. The model operated with maximum performance, accuracy, and responsiveness in all functionalities.   
**Conclusion:** ✅ **Usable**  

---

## Test #2: Indoor Illumination (Good)

**Conditions:** Well-lit room (central light on and windows open).  
**Luminosity (Lux):** `137 Lux`   

| Functionality | Result | Observations |
| :--- | :---: | :--- |
| **General Detection** | Excellent | Immediate and stable detection. |
| **Pointing (Move)** | Good | Perceptible slight latency ("lag"), but fully functional. |
| **Visual Feedback** | OK | All status colors worked. |
| **Left Click** | Good (>7/10) | **False positives (unintentional clicks) occurred sporadically.** |
| **Freeze** | Excellent | Worked as expected. |
| **Drag** | Good | **Noticeable delay to *start* the dragging gesture**, but maintained. |
| **Right Click** | Good (>7/10) | Good accuracy, no conflicts. |
| **Scroll (3 Fingers)** | Excellent | Immediate and smooth detection. |
| **Stop Gesture** | Immediate | Worked on the first try. |

### General Summary of Test #2  
**Analysis:** Very good indoor lighting. General performance remains excellent, but with a slight drop in responsiveness (latency) and click accuracy.  
**Conclusion:** ✅ **Usable**  

---

## Test #3: Indoor Illumination (Standard)

**Conditions:** Room with the central light on (no sunlight).  
**Luminosity (Lux):** `43 Lux`   

| Functionality | Result | Observations |
| :--- | :---: | :--- |
| **General Detection** | Excellent | Immediate and stable detection. |
| **Pointing (Move)** | Good | Slight latency, similar to Test #2. |
| **Visual Feedback** | OK | All status colors worked. |
| **Left Click** | Good (>7/10) | False positives occurred sporadically (similar to Test #2). |
| **Freeze** | Excellent | Worked as expected. |
| **Drag** | Good | Noticeable delay to start the gesture (similar to Test #2). |
| **Right Click** | Good (>7/10) | Good accuracy, no conflicts. |
| **Scroll (3 Fingers)** | Excellent | Immediate and smooth detection. |
| **Stop Gesture** | Immediate | Worked on the first try. |

### General Summary of Test #3   
**Analysis:** Performance was functionally identical to Test #2, suggesting that `~40 Lux` is still sufficient for robust operation.   
**Conclusion:** ✅ **Usable**   

---

## Test #4: Low Illumination (Lamp)

**Conditions:** Dark room with a lamp (bedside lamp) on.  
**Luminosity (Lux):** `5 Lux`  

| Functionality | Result | Observations |
| :--- | :---: | :--- |
| **General Detection** | Poor | Immediate detection, but with constant **slight "jitter" (trembling)**. |
| **Pointing (Move)** | Poor | **Significant latency**, making fine control difficult. |
| **Visual Feedback** | Poor | Status colors updated, but with visible delay. |
| **Left Click** | Poor (<7/10) | High rate of false positives. |
| **Freeze** | Poor | Perceptible delay in freezing the cursor. |
| **Drag** | Good | Worked, but **involuntarily released the click** a few times. |
| **Right Click** | Poor (<7/10) | **Gesture Conflict:** Confused the right click with the 'Scroll' gesture. |
| **Scroll (3 Fingers)** | Poor | Immediate detection, but scrolling was slow and choppy. |
| **Stop Gesture** | Immediate | Worked. (See Analysis). |

### General Summary of Test #4  
**Analysis:** Severely degraded performance. Low light caused "jitter" and high latency.   
**Critical Bug:** Gesture conflicts occurred, primarily the model interpreting clicks/scrolls as the "Stop" gesture, forcing program restart.   
**Conclusion:** ⚠️ **Usable with difficulty**   
  
---

## Test #5: Extreme Illumination (Monitor)

**Conditions:** Dark room, only monitor illumination.   
**Luminosity (Lux):** `1 Lux`   

| Functionality | Result | Observations |
| :--- | :---: | :--- |
| **Detecção Geral** | Failure | The hand was initially detected. |
| **All Gestures** | Failure | Any gesture (pointing, clicking, etc.) was erroneously interpreted as the "Stop" gesture. |

### General Summary of Test #5     
**Analysis:** Critical and total failure. The model cannot effectively distinguish landmarks, interpreting any movement as the closed fist ("Stop") gesture. The program immediately closed upon attempting any interaction.   
**Conclusion:** ❌ **Unusable**   
