"""
 Title:         Voce Slip Hardening Asaro Inelasticity Model
 Description:   For creating the VSHAI material file
 Author:        Janzen Choi

"""

# Libraries
from deer_sim.materials.__material__ import __Material__

# Format for defining materials
MATERIAL_FORMAT = """
<materials>
  <{material} type="SingleCrystalModel">
    <kinematics type="StandardKinematicModel">
      <emodel type="IsotropicLinearElasticModel">
        <m1_type>youngs</m1_type>
        <m1>{youngs}</m1>
        <m2_type>poissons</m2_type>
        <m2>{poissons}</m2>
      </emodel>
      <imodel type="AsaroInelasticity">
        <rule type="PowerLawSlipRule">
          <resistance type="VoceSlipHardening">
            <tau_sat>{tau_s}</tau_sat>
            <b>{b}</b>
            <tau_0>{tau_0}</tau_0>
          </resistance>
          <gamma0>{gamma_0}</gamma0>
          <n>{n}</n>
        </rule>
      </imodel>
    </kinematics>
    <lattice type="CubicLattice">
      <a>1.0</a>
      <slip_systems>
        {slip_dir} ; {slip_plane}
      </slip_systems>
    </lattice>
  </{material}>
</materials>
"""

# VSHAI Class
class Material(__Material__):
    
    def get_material(self) -> str:
        """
        Gets the content for the material file;
        must be overridden
        """
        material_content = MATERIAL_FORMAT.format(
            material   = self.get_name(),
            youngs     = 157000.0,
            poissons   = 0.30,
            tau_s      = self.get_param("tau_s"),
            b          = self.get_param("b"),
            tau_0      = self.get_param("tau_0"),
            gamma_0    = self.get_param("gamma_0"),
            n          = self.get_param("n"),
            slip_dir   = "1 1 0",
            slip_plane = "1 1 1"
        )
        return material_content
    