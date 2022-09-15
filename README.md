# Reinforcement Learning for Snake Game Project in Python

<p align="center">
  <img src="https://user-images.githubusercontent.com/113403062/189812492-6b03500b-57ed-4111-9453-ec6abd43befe.gif" alt="animated" width=700 heigt=700/>
</p>

*Above is a video of a reinforcement learning model that was trained with the proximal policy optimization (PPO) algorithm for 1M iterations. It averages around a score of 20.*

This project was made in July 2022. In this project, I programmed the Snake Game with **pygame**. The goal is to obtain as many apples/foods/points as possible by controlling the snake with the arrow keys on your keyboard. The snake dies when it either runs into a wall or runs into itself. After programming the game itself, I programmed a custom environment to train a snake agent to play the game successfully through policy gradient reinforcement learning. Packages used include Stable Baselines3, Gym, NumPy, and others.   

**Game-File.py** is a Python file that will allow you to play the Snake Game on your own with the arrow keys on your keyboard. All necessary dependencies are listed at the top of the file. I found that it was easier to simply code the game itself before implementing the reinforcement learning methods, which is why this file exists. 

**Array-Snake-Environment.pt** is a Python file that allows you to either train new RL models or evaluate the performance of existing models. **PPO-Model-Snake-1m.zip, PPO-Model-Snake-500k.zip, and PPO-Model-Snake200k.zip** are all examples of previously saved models. Each of this models was trained on the PPO algorithm. Alternative algorithms can be found on the documentation page for Stable Baselines3 [here](https://stable-baselines3.readthedocs.io/en/master/).
