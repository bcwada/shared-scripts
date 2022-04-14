python /home/bcwada/projects/shared-scripts/scripts/make_c0_molden.py c0.casscf 122 122 casscf.molden --out original

python /home/bcwada/projects/shared-scripts/scripts/swap_mos.py c0.casscf 122 122 30 31 --out c0_editted
python /home/bcwada/projects/shared-scripts/scripts/make_c0_molden.py c0_editted 122 122 casscf.molden --out swapped