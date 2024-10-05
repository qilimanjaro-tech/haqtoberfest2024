## Hello quantum coders!

First of all, thank you for choosing the Quantum Finance challenge, hope you eenjoy it! At the time you are reading this document, we haven't met yet, but will hit the office in a matter of minutes. My name is Adrià, nice to meet you guys! I'm sure Ameer, Isi and the rest of mentors have given you a warm welcome :). 

As Ameer already commented during the presentation, this challenge consists of tackling a very well-known problem in the financial industry, Portfolio Optimization, leveraging Quantum Machine Learning techniques. 

## Before coding

You need to: 
1. Create a conda environament with Python 3.12
2. Install the libraries in requirements.txt
3. Clone the haqtoberfest24 repo and get into the quantum_finance challenge
4. Enjoy the ride!

All mentors are here to help, so don't hesitate to ask them in case you need some support ;) 


## Structure and recommendations on how to approach this challenge

The goal of this challenge is to build your own Variational Quantum Eigensolver (VQE) for Portfolio Optimization. As this may be quite challenging, the idea is to try to reproduce the results I obtained during my Bachelor's Thesis, which should have been already forwarded to you. My first recommendation is that before starting to type a single line of code, you read the article in diagonal up to section V (included). I wouldn't devote more than an hour to this, having a general idea is enough, take into account you can ask as many questions as needed. This way, you'll have a clear idea of what we want to achieve, which will be very helpful for the coding part. 

Note that there are two folders: challenge and solved. In the latter, you'll find a valid solution for reaching the first and main milestone of this challenge: building a VQE for Portfolio Optimization. In the former, you'll find the same notebook, but the code of the functions has been deleted. My main intention is that you learn about quantum computing and Finance, so I proposed an approach to follow in case you feel overwhelmed. You don't need to follow the established path, although we have also a non-guided part of the challenge for you. The deliverable of this hackathon is the notebook `challenge/challenge.ipynb`. Note that the functons are defined in diferent scripts depending on their meaning. This should allow you to work on different parts of the challenge in parallel, even without creating branches and so on. 

In case you manage to solve all the guidiing part, there are several things you can do, depending on your interests and knowledge: 


### Easy extensions
- Solve by brute force the problem using the Hamiltonian formulations. How good is the discretization? 
- Compare the perfomance of your portfolio to the perfomance of the assets that form it. Is Modern Portfolio Theory valid?
- Solve Portfolio Optimization following the standard approach: Monte Carlo simulation. In this case, you only need to generate sets of random weights, assess them the historical data, and calculate the portfolio metrics.

### Hard but interesting extensions
- Follow the rest of the Bachelor's Thesis to provide VQE with trainability, or even do it your own way! You'll build an Unsupervised QML model. 
- If you are familiar with VQAs and know about their limitations, we encourage you give Quantum Reservoir Computing a try. Ameer will be more than happy to guide you through the journey in case you are interested, but find below a first introduction. 

## About Quantum Reservoir Computing

Quantum reservoir computing (QRC) is an approach that has shown great promise in both classical and quantum machine learning tasks. They capitalize on the unique properties of quantum systems while utilizing simple training methods, leading to impressive performance. 

Reservoir computing is a computational framework that maps input signals into high-dimensional spaces through the dynamics of a fixed, nonlinear system known as a **reservoir**. In classical reservoir computing, the reservoir is typically a randomly initialized dynamical system whose complex internal states transform input data. The key advantage of this approach is that only the output layer, which reads the reservoir states, is trained, while the reservoir itself remains unchanged. This drastically reduces the computational cost and complexity of training compared to fully trainable models, such as traditional neural networks.

In **Quantum Reservoir Computing (QRC)**, this concept is extended by leveraging the unique properties of quantum systems to create the reservoir. Unlike classical reservoirs, quantum reservoirs can explore exponentially larger state spaces, potentially offering a significant performance boost for complex tasks like machine learning, optimization, and time-series analysis.

The process works as follows:

- **Input encoding**: Classical or quantum data is encoded into a quantum state.
- **Quantum evolution**: The input data interacts with the quantum reservoir (a network of qubits or quantum oscillators), whose internal states evolve based on the inherent quantum dynamics.
- **Measurement and output**: The quantum reservoir’s final state is measured, and these measurements are fed into a simple trainable output layer, which maps the reservoir states to the target output.

In this part of the challenge, your task is to explore the potential of QRC by applying it to solve the **portfolio optimization problem**. Additionally, you will compare the results you obtain with those produced using the **Variational Quantum Eigensolver (VQE)**, and provide your conclusions based on the comparison. You have the flexibility to simulate the quantum reservoir using any tool or framework of your choice.

To guide you in understanding how QRC can be implemented we recommend the following resources:

- https://arxiv.org/abs/2409.00998
- https://arxiv.org/pdf/2205.06809
- https://journals.aps.org/prapplied/pdf/10.1103/PhysRevApplied.8.024030
- https://dataspace.princeton.edu/handle/88435/dsp01tm70mz416