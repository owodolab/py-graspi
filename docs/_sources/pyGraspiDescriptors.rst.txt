.. _pyGraspiDescriptors:

==============================================
Descriptors
==============================================

For two-phase morphology, current **py-graspi** computes the following descriptors:

* **STAT_n** - Number of vertices, excluding meta ones
* **STAT_e** - Number of interface edges

    .. image:: imgs/stat_n_e.png
        :scale: 50%
        :align: center
* **STAT_n_D** - Number of black vertices
* **STAT_n_A** - Number of white vertices
* **STAT_CC_D** - Number of black connected components
* **STAT_CC_A** - Number of white connected components

    .. image:: imgs/c_a.png
        :scale: 50%
        :align: center
* **STAT_CC_D_An** - Number of black connected components connected to top (red)
* **STAT_CC_A_Ca** - Number of white connected components connected to bottom (blue)
* **ABS_f_D** - Fraction of black vertices
* **CT_f_conn_D_An** - Fraction of black vertices connected to the top
* **CT_f_conn_A_Ca** - Fraction of white vertices connected to bottom

    .. image:: imgs/conn_d_a.png
        :scale: 50%
        :align: center
* **CT_n_D_adj_An** - Number of black vertices in direct contact with top (An - top/anode)
* **CT_n_A_adj_Ca** - Number of white vertices in direct contact with bottom (Ca - bottom/cathode)
* **DISS_f10_D** - Fraction of black vertices in 10 distances to interface
* **DISS_wf10_D** - Fraction of black vertices in 10 distances to interface (weighted)
* **CT_f_E_conn** - Fraction of interface with complementary paths to bottom and top
* **CT_e_conn** - Number of interface edges with complementary paths
* **CT_e_D_An** - Number of black interface vertices with path to top
* **CT_e_A_Ca** - Number of white interface vertices with path to bottom
* **CT_f_D_tort1** - Fraction of black vertices with straight rising paths (t = 1)
* **CT_f_A_tort1** - Fraction of white vertices with straight rising paths (t = 1)

    .. image:: imgs/tort.png
        :scale: 50%
        :align: center

Below we provide the definition of all above descriptors and their code implementations.

   .. automodule:: py_graspi.descriptors
      :members:
      :undoc-members:
      :show-inheritance:




