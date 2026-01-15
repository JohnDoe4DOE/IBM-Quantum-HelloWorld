# Bell-State Quantum Circuit (Qiskit)

This repository contains a **Bell-state example** using Qiskit's EstimatorV2 API.

## Overview

- Creates a 2-qubit Bell state.
- Measures single-qubit observables (IZ, IX, ZI, XI) — appear random.
- Measures two-qubit correlations (ZZ, XX) — show entanglement.
- Visualizes the circuit and plots expectation values.

## Requirements

- Python 3.11+
- Qiskit and IBM Quantum Runtime:
```bash
pip install qiskit qiskit-ibm-runtime matplotlib
