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
        <m1 type="ConstantInterpolate">
          <v>{youngs}</v>
        </m1>
        <m1_type>youngs</m1_type>
        <m2 type="ConstantInterpolate">
          <v>{poissons}</v>
        </m2>
        <m2_type>poissons</m2_type>
      </emodel>
      <imodel type="AsaroInelasticity">
        <rule type="PowerLawSlipRule">
          <resistance type="VoceSlipHardening">
            <tau_sat type="ConstantInterpolate">
              <v>{tau_s}</v>
            </tau_sat>
            <b type="ConstantInterpolate">
              <v>{b}</v>
            </b>
            <tau_0 type="ConstantInterpolate">
              <v>{tau_0}</v>
            </tau_0>
            <k type="ConstantInterpolate">
								<v>0</v>
            </k>
            <var_name>strength</var_name>
          </resistance>
          <gamma0 type="ConstantInterpolate">
            <v>{gamma_0}</v>
          </gamma0>
          <n type="ConstantInterpolate">
            <v>{n}</v>
          </n>
        </rule>
      </imodel>
    </kinematics>
    <lattice type="CubicLattice">
      <a>1.0</a>
      <slip_systems>{slip_dir} ; {slip_plane}</slip_systems>
      <twin_systems/>
    </lattice>
    <update_rotation>true</update_rotation>
    <alpha type="ConstantInterpolate">
      <v>0</v>
    </alpha>
    <rtol>1e-08</rtol>
    <atol>1e-06</atol>
    <miter>16</miter>
    <verbose>false</verbose>
    <linesearch>false</linesearch>
    <max_divide>2</max_divide>
    <postprocessors/>
    <elastic_predictor>false</elastic_predictor>
    <fallback_elastic_predictor>true</fallback_elastic_predictor>
    <force_divide>0</force_divide>
    <elastic_predictor_first_step>false</elastic_predictor_first_step>
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
    