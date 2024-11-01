.. _pyGraspiDescriptors:

==============================================
Descriptors
==============================================

For two-phase morphology, current **py-graspi** computes the following descriptors:

* **STAT_n** - Number of vertices
* **STAT_e** - Number of interface edges
* **STAT_n_D** - Number of black vertices
* **STAT_n_A** - Number of white vertices
* **STAT_CC_D** - Number of black connected components
* **STAT_CC_A** - Number of white connected components
* **STAT_CC_D_An** - Number of black connected components connected to top (red)
* **STAT_CC_A_Ca** - Number of white connected components connected to bottom (blue)
* **ABS_f_D** - Fraction of black vertices
* **CT_f_conn_D_An** - Fraction of black vertices connected to the top
* **CT_f_conn_A_Ca** - Fraction of white vertices connected to bottom
* **CT_n_D_adj_An** - Number of black vertices in direct contact with top (An - top/anode)
* **CT_n_A_adj_Ca** - Number of white vertices in direct contact with bottom (Ca - bottom/cathode)

Below we provide the definition of all above descriptors and their code implementations.

   .. automodule:: graspi_igraph.descriptors
      :members:
      :undoc-members:
      :show-inheritance:




