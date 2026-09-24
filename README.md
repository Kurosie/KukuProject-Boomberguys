# 🎮 **BomberGuys**

| 🔍 | All project files can be found here: [**Google Drive Files for this Project**](https://drive.google.com/drive/folders/1C_S7WvHjj8j-2weZabGMlgi2-YWhw3bQ?usp=sharing) |
| -- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |

| ⚡ | A demo video is available [here](https://youtu.be/pXulugr4zrg?si=tjf_972soVj1KWEB). |
| -  | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |

| 🌐 | Play the game in your browser [**here**](https://git.arts.ac.uk/pages/24009771/FinalProject-BomberGuy/). |
| --- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |

---

## 🧠 Introduction

As a game designer, I have developed a critical stance toward traditional physical controllers such as keyboards, mice, and gamepads. These conventional devices constrain players to minute finger movements, often reducing gameplay to a seated experience where the body is almost entirely disengaged. This form of interaction limits the sense of immersion, as the player's connection to the game world is compressed into a handful of button presses.

By contrast, human beings have long relied on bodily movements to convey intent and emotion—waving to greet, nodding in agreement, pointing to indicate direction. Body language inherently carries rich information. This suggests that bodily movement, when used as an input medium, offers a natural sense of intuitiveness and immersion. Studies have shown that interfaces based on physical movement allow users to interact through active bodily gestures, delivering a more organic and expressive experience than traditional mouse-and-keyboard systems.

Only by breaking free from the limitations of keyboards and mice—and by fully engaging the body in the interaction—can we achieve the kind of immersive and instinctual gameplay I envision. This is the foundation of the *BomberGuys* project: to use the body as a vessel for expressing player intent, replacing button-based inputs with full-body gestures, and allowing players to "enter" the game in a more visceral and intuitive way.

Notably, this turn toward bodily interaction aligns with recent trends in human-computer interaction. From motion-sensing game consoles to the gesture recognition features in VR/AR devices, pioneers in interactive technology have been striving for more direct and embodied forms of engagement. As scholars have pointed out, “all human action—including cognition—is fundamentally embodied.”

The conceptual framework of this project is deeply informed by embodied interaction theory and interactive art practices. During development, I drew inspiration from the work of Paul Dourish and Myron Krueger, whose theories and artistic systems helped me reconsider the meaning of “interaction” and “control” in human-computer interfaces.

### 🔸 Paul Dourish – *Embodied Interaction*

In his seminal book *Where the Action Is*, Paul Dourish introduces the concept of *embodied interaction*, arguing that human-computer interaction should be grounded in physical, bodily practices rather than abstract logical operations. Drawing on phenomenological philosophy (notably Heidegger and Wittgenstein), Dourish emphasizes that intuitive and meaningful interaction emerges from the user’s bodily skills and lived experience, rather than from detached rational thought.

This theory provided a philosophical foundation for *BomberGuys*. I came to realize that intuitive interaction must arise from the body itself, and that the player’s entire physicality should be treated as the interface—not just their fingertips. Inspired by Dourish, I approached bodily motion not just as an input method, but as a form of communication that conveys intent, allowing for more immersive and meaningful gameplay.

![s2764351](https://git.arts.ac.uk/24009771/FinalProject-BomberGuy/assets/1290/889f8a40-15b2-483d-a117-fc0111c8ff35)


### 🔸 Myron Krueger – *Videoplace* (1985)

Myron Krueger’s *Videoplace* system was one of the first interactive installations to use the body itself as the interface. Participants’ silhouettes were captured and projected in real time, allowing them to interact with virtual objects and other users without any physical controllers. Krueger famously declared that he *“hated”* the fact that humans were still interacting with computers through 100-year-old devices like the keyboard, asking: *“Why should I use just my fingers when I have an entire body?”*

In *Videoplace*, a participant steps into a space and sees their dynamic outline projected on the screen, instantly reacting with digital elements. This pioneering work demonstrated the expressive power of full-body motion as input and deeply influenced the vision behind *BomberGuys*. It validated the idea that the entire human body can serve as a controller and inspired me to explore how to break away from interface constraints and create a gesture-driven game system that feels immersive and creative.

![0ee3f434-c14b-4bce-9c1d-660e7bb37167](https://git.arts.ac.uk/24009771/FinalProject-BomberGuy/assets/1290/54ebb603-6a4d-4fd9-ae19-06b06cd993a4)


---

## 🔧 Technical Implementation Details

This project operates through a dual-system architecture composed of a **Python backend** and a **Unity frontend**. The Python side is responsible for image acquisition, gesture recognition, and keypress emulation, while the Unity side handles game logic and interaction responses. Below is a detailed breakdown of each module, as well as the communication flow between the Python and Unity components.

---

### 🧠 Python-Side Implementation

The Python backend primarily manages computer vision and machine learning tasks. It captures the player’s gestures via webcam and maps them to pre-defined control commands. This pipeline consists of several modular scripts:

---

#### 🖼️ Image Collection ([`collect_imgs.py`](collect_imgs.py))

This script is used to gather training image samples for each gesture. Upon launching the script, the user selects which gesture class to collect from a predefined set (e.g., “up”, “down”, “left”, “right”, “bomb”). The script activates the webcam (via OpenCV), captures frames at a consistent rate, and saves each frame as an image in a folder named after the gesture class.

To ensure a sufficient dataset for training, the script is set to collect up to 500 images per gesture (though it can be stopped manually at any point). During collection, a live video feed is displayed for calibration, and pressing “q” exits the process. This module lays the foundation by generating a class-labeled image dataset for downstream processing.

![8a6034f094ea76530ff284a32e0fe09](https://git.arts.ac.uk/24009771/FinalProject-BomberGuy/assets/1290/9ecb213f-e826-4ec4-9133-c66fb295e4ae)


---

#### 📐 Data Preprocessing & Keypoint Extraction ([`create_dataset.py`](create_dataset.py))

With raw image data collected, this module extracts key features for classification. It leverages Google’s **MediaPipe Hands** model to detect 21 hand landmarks (e.g., finger joints and wrist) in each image.

Each image is processed through the model to obtain landmark coordinates. If a hand is not detected in an image, that frame is skipped to ensure data quality. The coordinates are then normalized: translated into a relative coordinate system (origin at the hand’s bounding box corner), removing absolute position bias. This enables consistency across similar gestures regardless of spatial position.

Each processed image is converted into a numerical feature vector and stored with its corresponding label. All data is serialized and saved (e.g., `data.pickle`), ready for model training.

![6d07ca52584d6ebab280e04a396e296](https://git.arts.ac.uk/24009771/FinalProject-BomberGuy/assets/1290/6b16bdfd-0179-4b4b-9b3b-694849945c86)

---

#### 🏋️ Model Training ([`train_classifier.py`](train_classifier.py))

This module trains a gesture classification model using the preprocessed feature data. The dataset is split randomly into a training set (e.g., 80%) and a test set (20%).

I selected the **Random Forest Classifier**, an ensemble-based decision tree algorithm. This model was chosen for its strong performance on small to medium datasets, resistance to overfitting, and fast inference time—making it well-suited for real-time interaction.

The script trains the model, evaluates accuracy on the test set, and prints the result. In my tests, the model achieved around **95%+** accuracy (depending on the data quality and quantity), demonstrating robust gesture recognition performance.

The trained model and label mapping dictionary are then saved (e.g., `model.p`) for use in the inference pipeline.

![87a600934d95fb7a781c755ace79b35](https://git.arts.ac.uk/24009771/FinalProject-BomberGuy/assets/1290/9dc17fae-e45f-49e8-b5fd-bd924bdf55b5)


---

#### 🎮 Real-Time Inference & Keystroke Emulation ([`inference_classifier.py`](inference_classifier.py))

This is the **core runtime module** for the Python backend, responsible for live gesture recognition and control signal output during gameplay.

When launched, the script opens the webcam and begins processing each video frame in real time:

1. Each frame is converted to RGB and fed into the MediaPipe hand detector.
2. If a hand is detected, its landmark coordinates are extracted and normalized (same method as in training).
3. The trained random forest model is loaded and used to predict the gesture class based on the feature vector.

To improve stability, a **prediction smoothing mechanism** is implemented: a fixed-length queue stores the most recent predictions, and the most frequent result is used as the final gesture label. This reduces noise from single-frame misclassifications.

Each recognized gesture is mapped to a virtual keyboard input—for example:

* “up” → `W` key
* “bomb” → `Space` key

Using the **pynput** library, the script simulates key press and release events. If a new gesture is detected, the corresponding key is pressed; if no gesture is detected for several frames, the key is released. In essence, this module acts as a **“virtual player”**, translating body movements into standard keyboard inputs.

To assist with debugging, the predicted gesture label is overlayed on the live video window using OpenCV. The program can be exited by pressing “q”.

By completing this loop—**from visual input to physical gesture to keyboard output**—the Python backend enables natural gesture control for the game, eliminating the need for traditional physical controllers.

![未标题-1](https://git.arts.ac.uk/24009771/FinalProject-BomberGuy/assets/1290/1d76b1ca-80f1-48d0-8974-0139f9b893c4)


---

### 🎮 Unity-Side Implementation

The Unity side is responsible for receiving control signals from Python and executing corresponding actions within the game environment. Since the Python backend uses **keyboard input emulation** as the communication method, Unity requires **no additional networking modules**—it simply listens for standard key inputs using its built-in input system.Specifically, the player character in the Unity scene is equipped with a control script that checks for certain key presses on each frame update (e.g., using `Input.GetKey(KeyCode.W)`, etc.). When a key press is detected, the appropriate gameplay logic is triggered: When the W, A, S, or D keys are pressed, the character moves in the corresponding up, left, down, or right direction. A base movement speed and collision detection system ensure that the character can navigate freely across the grid map while avoiding obstacles.Because *BomberGuys* is inspired by the classic *Bomberman* gameplay, this grid-based four-directional movement forms a core part of the player experience.Pressing the Space key causes the character to place a bomb at their current location. A bomb object is instantiated in the scene, and a simple behavior system is initiated: after a fixed delay, the bomb explodes, producing an area-of-effect impact. This can destroy breakable walls or eliminate nearby characters.The explosion behavior in the prototype is implemented using basic triggers and timers, without involving complex physics or advanced AI.In designing the Unity system, my goal was to ensure **instantaneous input response** and **clear feedback**. Thanks to the **gesture smoothing and key-holding logic** handled on the Python side, Unity receives input events that are nearly indistinguishable from those of a real keyboard.

In *BomberGuys*, enemies are not static or randomly moving objects—they exhibit a degree of behavioral intelligence to enhance challenge and dynamism. The core logic is defined in the `BasicEnemy.cs` script. Each enemy moves through the map at a constant speed (`WalkSpeed`), periodically evaluating whether to change direction to avoid getting stuck. Two key behavior parameters govern their movement logic: `ProbabilityToFlipOnIntersection` determines how likely an enemy is to turn at intersections (with 100% ensuring a turn and 0% always going straight), while `ProbabilityToFollowPlayer` dictates how likely an enemy is to pursue the player instead of wandering aimlessly. Enemies also implement full damage and death mechanics via `IDamageTaker` and `IDamageEmitter` interfaces: when hit by bombs, they flash (`DamageBlinkDuration`), play hurt animations, and are destroyed upon reaching zero health—awarding the player with score points (`ScorePoints`). All animation states are handled through Unity’s Animator, with an optional debug mode (`DebugAnimatorCrossFades`) to visualize crossfades during development. Importantly, all parameters are exposed in the Unity Inspector, allowing quick adjustments and diverse enemy behaviors. This design strikes a balance between simplicity and configurability, providing a basic dynamic threat that complements the player’s gesture-based input system and enhances the strategic layer of gameplay.


For example:

* When the user continuously performs an “up” gesture, Python keeps simulating the W key being held down, causing the character to move upward in Unity without interruption.
* When the gesture stops or changes, the key is released, and the character immediately stops.

This **key-based architecture** makes Unity development straightforward and modular. Since Unity simply reacts to key inputs, I did not need to modify the core input system or write any custom interfaces. This clean separation allows the gesture recognition and game logic to be developed and debugged independently—each system can be optimized without interfering with the other.

![unity1](https://git.arts.ac.uk/24009771/FinalProject-BomberGuy/assets/1290/b6f3120a-5609-4b4a-8a85-0efe146fd9f6)


### 🧩 Python–Unity Communication: Keyboard Simulation vs. Network Sockets

This project deliberately chose to simulate keyboard input to transmit control signals to Unity, rather than using network socket communication (e.g., UDP/TCP). This decision was based on a balance of technical cost, stability, and development efficiency.

First, keyboard simulation offers low implementation cost and easy integration. By leveraging existing input libraries on the Python side, I can emulate keystroke events that Unity recognizes as standard input without requiring any modification to the game’s input system. This greatly simplifies development. In contrast, using UDP would have required me to write a network client in Unity to listen for messages, a server in Python to send commands, and a custom message protocol. This approach not only adds complexity but also introduces potential issues such as network latency, packet loss, and firewall restrictions. In comparison, simulated keystrokes are handled natively by the operating system with negligible latency and without network dependency, ensuring real-time responsiveness and high stability.

Second, keyboard simulation is highly portable and platform-agnostic. Any device that runs a Unity game and supports standard keyboard input can use this solution without modification. On the other hand, network communication can face compatibility issues, requiring firewall configurations or administrative permissions. During development and debugging, keyboard simulation is also more transparent: developers can directly observe the virtual input as if it came from a real user.

Of course, this method has limitations. It assumes that the Unity game window is focused and able to receive input; if the user clicks away, simulated input may be lost. However, this is manageable in a controlled demonstration setting.

Considering the prototype’s goals and development constraints, I concluded that keyboard simulation was the best approach that avoids unnecessary complexity. This design achieves a balance between modular decoupling and responsive interaction: Python focuses on interpreting human gestures, Unity handles game presentation, and the two are bridged by a simple and reliable input channel.


## 🔍 Model Performance & Gesture Strategy

During development, I repeatedly refined the gesture recognition model to ensure both high accuracy and real-time stability. The final RandomForest classifier achieved over **95% accuracy** in offline tests on my dataset, indicating that the model is highly usable. To mitigate environmental noise (e.g., lighting changes or background clutter), I implemented a sliding window voting mechanism for robust prediction smoothing. As a result, the system performs reliably during live interaction: when users perform gestures clearly, the system correctly classifies them in nearly every frame. Occasional misclassifications are quickly corrected within subsequent frames, avoiding prolonged incorrect input.

From the beginning, I strategically designed the five hand gestures to be distinct and easy to perform. For instance, open palm, closed fist, and directional pointing were chosen to ensure the model could easily differentiate them. Since my system relies on single-hand detection rather than full-body pose estimation, gesture variation is primarily expressed through finger flexion and hand shape. I also prioritized user comfort by avoiding complex or unnatural poses. For training, I collected several hundred images per gesture, incorporating different angles, positions, and user variability. This dataset diversity helped the model learn generalizable patterns and avoid overfitting to specific individuals or settings.

Technically, BomberGuys demonstrates the convergence of computer vision, machine learning, and game engines. The frontend uses deep models for hand landmark estimation (via MediaPipe), the core recognition relies on a classic RandomForest model, and a lightweight input-simulation mechanism connects the Python backend to Unity. This modular design forms a seamless pipeline from gesture to game control.

---

## ⚠️ Limitations of Embodied Interaction

Despite its innovation, gesture-based interaction has constraints. It requires reliable hardware and well-lit environments. In dim light or with occluded hands (e.g., due to sleeves, tattoos, or bracelets), accuracy drops. The system’s performance depends on visual clarity and consistency.Physical interaction favors certain users. Young, able-bodied players can easily perform gestures, but elderly users or those with mobility issues may struggle. The "gorilla arm" effect—arm fatigue from prolonged motion—is a known challenge in gesture-based UI design. Testers reported shoulder discomfort after \~10 minutes of use. Ergonomics and pacing must be considered in future designs.Intuitive gestures still require a predefined vocabulary. While familiar motions reduce the learning curve, some gestures may be culturally ambiguous or non-obvious, requiring training. Moreover, each user builds muscle memory over time, just as with keyboard controls.Body-based controls aren't a silver bullet. In high-speed or competitive games, traditional inputs remain faster and more precise. The future lies in multimodal systems—combining body gestures with voice, eye-tracking, or even brain-computer interfaces to adapt to diverse scenarios and user needs.

---

## 📚 Bibliography

1. Lugaresi, C., *et al.* (2019). **MediaPipe: A Framework for Building Perception Pipelines.** arXiv. [https://arxiv.org/abs/1906.08172](https://arxiv.org/abs/1906.08172)
2. Linardakis, M., Varlamis, I., & Papadopoulos, G. T. (2025). **Survey on Hand Gesture Recognition from Visual Input.** arXiv. [https://arxiv.org/abs/2501.11992](https://arxiv.org/abs/2501.11992)
3. Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
4. Zhou, Z.-H. (2016). *Machine Learning (in Chinese)*. Tsinghua University Press.
5. Hincapié-Ramos, J. D., Guo, X., Moghadasian, P., & Irani, P. (2014). **Consumed Endurance: A Metric to Quantify Arm Fatigue of Mid-Air Interactions.** *CHI '14: Proceedings of the SIGCHI Conference on Human Factors in Computing Systems*, ACM. [https://doi.org/10.1145/2556288.2557130](https://doi.org/10.1145/2556288.2557130)
6. Hansberger, J. T., & Bolton, M. L. (2017). **Dispelling the Gorilla Arm Syndrome: The Viability of Prolonged Gesture Interactions.** *HCI International 2017*, Lecture Notes in Computer Science (Vol. 10271), Springer. [https://doi.org/10.1007/978-3-319-58071-5\_25](https://doi.org/10.1007/978-3-319-58071-5_25)
7. Wigdor, D., & Wixon, D. (2011). *Brave NUI World: Designing Natural User Interfaces for Touch and Gesture*. Morgan Kaufmann.
8. Khan, A. R. S. (2023). **Sending Data from Python to Unity via UDP.** Medium. [https://medium.com/@almassco2007/sending-data-from-python-to-unity-udp-b818bf7698c6](https://medium.com/@almassco2007/sending-data-from-python-to-unity-udp-b818bf7698c6)
9. Sweigart, A. (2015). *Automate the Boring Stuff with Python*. No Starch Press. [https://automatetheboringstuff.com/](https://automatetheboringstuff.com/)
10. Juliani, A., *et al.* (2018). **Unity: A General Platform for Intelligent Agents.** arXiv. [https://arxiv.org/abs/1809.02627](https://arxiv.org/abs/1809.02627)
11. Halbhuber, D., Schauhuber, P., Schwind, V., & Henze, N. (2023). **The Effects of Latency and In-Game Perspective on Player Performance and Game Experience.** *Proceedings of the ACM on Human-Computer Interaction*, CHI PLAY. [https://doi.org/10.1145/3610872](https://doi.org/10.1145/3610872)
12. Swink, S. (2008). *Game Feel: A Game Designer’s Guide to Virtual Sensation*. Morgan Kaufmann.

---


