from IntSimulator.hamiltonians import hamiltonian_site_i, total_hamiltonian_site, total_hamiltonian_int
from qutip import Qobj
import pytest
import numpy as np

def test_single_site_evalues():
    hamiltonian = hamiltonian_site_i(1)

    assert (hamiltonian.eigenenergies()[0] == pytest.approx(0.5))
    assert (hamiltonian.eigenenergies()[1] == pytest.approx(1.5))
    assert (hamiltonian.eigenenergies()[2] == pytest.approx(2.5))

def test_single_site_evectors():
    hamiltonian = hamiltonian_site_i(1)

    evector_0 = hamiltonian.eigenstates()[1][0]
    evector_1 = hamiltonian.eigenstates()[1][1]
    evector_2 = hamiltonian.eigenstates()[1][2]

    assert (evector_0[0] == pytest.approx(0.5))
    assert (evector_0[1] == pytest.approx(np.sqrt(2)/2))
    assert (evector_0[2] == pytest.approx(0.5))

    assert (evector_1[0] == pytest.approx(-1/np.sqrt(2)))
    assert (evector_1[1] == pytest.approx(0))
    assert (evector_1[2] == pytest.approx(1/np.sqrt(2)))

    assert (evector_2[0] == pytest.approx(-0.5))
    assert (evector_2[1] == pytest.approx(np.sqrt(2)/2))
    assert (evector_2[2] == pytest.approx(-0.5))
