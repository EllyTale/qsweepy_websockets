def create_openqasm_file(filename: str, qasm_code: str) -> None:
  """
  Creates OpenQASM file

  Args:
    filename:
    qasm_code:
  """
  with open(filename, "w") as f:
    f.write(qasm_code)

my_qasm_code: str = """
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];
"""
create_openqasm_file("quantum_circuit.qasm", my_qasm_code)