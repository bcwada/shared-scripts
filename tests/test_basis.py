

def test_something():
    c0 = np.fromfile("/home/bcwada/restructuring/researchCode/testing/testing_files/IT_FC_161302_c0")
    c0 = c0.reshape((122, 122))
    molden_file = Path("/home/bcwada/restructuring/researchCode/testing/testing_files/2IT_FC_161302_nto_S0-S1.molden")
    molden_obj = tools.molden.molden.load(molden_file)
    nto_obj = nto.Nto.from_vector_file("/home/bcwada/restructuring/researchCode/testing/testing_files/2IT_FC_161302_nto_S0-S1_vector")
    basis_obj = basis.from_molden(molden_file)
    SMat = np.genfromtxt("/home/bcwada/restructuring/researchCode/testing/testing_files/IT_FC_TC_order.txt", skip_header=2)
    """
    print(c0.T@SMat@c0)
    simMat = np.isclose(c0.T@SMat@c0, np.eye(122))
    for i in range(122):
        for j in range(122):
            if not simMat[i,j]:
                pass
                print((c0.T@SMat@c0)[i,j])
                #print(i,j)
                #print(simMat[i,j])
    """
    assert np.isclose(c0.T @ SMat @ c0, np.eye(122), atol=1e-6).all()
    U = basis_obj.to_tc_order()
    alt_SMat = U.T @ SMat @ U
    # print(molden_obj.mo_coeff[:,0])
    # print(nto_obj.holes[0])
    # print(type(nto_obj.holes[0]))
    assert np.isclose(U @ molden_obj.mo_coeff[:, 0], nto_obj.holes[0], atol=1e-4).all()
    print(molden_obj.mo_coeff[:, 1])
    print(nto_obj.parts[0])
    print(np.isclose(U @ molden_obj.mo_coeff[:, 1], nto_obj.parts[0], atol=1e-4))
    assert np.isclose(U @ molden_obj.mo_coeff[:, 1], nto_obj.parts[0], atol=1e-4).all()
    ovlp1_ml = molden_obj.mo_coeff[:, 1] @ alt_SMat @ molden_obj.mo_coeff[:, 1]
    ovlp1_tc = nto_obj.holes[1] @ SMat @ nto_obj.holes[1]
    print(ovlp1_ml, ovlp1_tc)
    