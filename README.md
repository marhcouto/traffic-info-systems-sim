# Simmulator for Information Perculation Schemes for Traffic Management

Simulation environment on MESA simulator to evaluate information percolation systems for traffic congestion avoidance.

## Folder Structure

- docs: presentation slides and paper
- src: source code
- test: unit tests

## Requirements

- Python 3.10 installed.
- Pip3

## Setup

Install mesa library for python:
```sh
pip install --upgrade mesa
```

Install matplotlib:
```sh
pip install matplotlib
```

(Only to run tests) Install pytest:
```sh
pip install pytest
```

Alternatively you can use ```pip install -r requirements.txt``` in the root folder of this project. This will install all packages included in a base conda environment used for the development of the project.

## Usage

### Running the simulation

From the root folder:

```sh
python src/server.py
```

### Running the unit tests

```sh
python
```

### Authors 

- Marcelo Couto
- Luis Lucas
- António Oliveira

