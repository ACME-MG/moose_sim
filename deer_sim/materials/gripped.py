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
  <{material}_cp type="SingleCrystalModel">
    <kinematics type="StandardKinematicModel">
      <emodel type="IsotropicLinearElasticModel">
        <m1_type>{youngs}</m1_type>
        <m1_type>youngs</m1_type>
        <m2_type>{poissons}</m2_type>
        <m2_type>poissons</m2_type>
      </emodel>
      <imodel type="AsaroInelasticity">
        <rule type="PowerLawSlipRule">
          <resistance type="VoceSlipHardening">
            <tau_sat>{cp_tau_s}</tau_sat>
            <b>{cp_b}</b>
            <tau_0>{cp_tau_0}</tau_0>
            <var_name>strength</var_name>
          </resistance>
          <gamma0>{cp_gamma_0}</gamma0>
          <n>{cp_n}</n>
        </rule>
      </imodel>
    </kinematics>
    <lattice type="CubicLattice">
      <a>1.0</a>
      <slip_systems>{slip_dir} ; {slip_plane}</slip_systems>
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
  </{material}_cp>
  <{material}_vp type="GeneralIntegrator">
		<elastic type="IsotropicLinearElasticModel">
      <m1_type>{youngs}</m1_type>
      <m1_type>youngs</m1_type>
      <m2_type>{poissons}</m2_type>
      <m2_type>poissons</m2_type>
		</elastic>
		<rule type="TVPFlowRule">
			<elastic type="IsotropicLinearElasticModel">
        <m1_type>{youngs}</m1_type>
        <m1_type>youngs</m1_type>
        <m2_type>{poissons}</m2_type>
        <m2_type>poissons</m2_type>
			</elastic>
			<flow type="PerzynaFlowRule">
				<surface type="IsoJ2"/>
				<hardening type="VoceIsotropicHardeningRule">
					<s0>{vp_s0}</s0>
					<R>{vp_R}</R>
					<d>{vp_d}</d>
				</hardening>
				<g type="GPowerLaw">
					<n>{vp_n}</n>
					<eta>{vp_eta}</eta>
				</g>
			</flow>
		</rule>
		<alpha type="ConstantInterpolate">
			<v>0</v>
		</alpha>
		<truesdell>false</truesdell>
		<rtol>1e-08</rtol>
		<atol>1e-08</atol>
		<miter>16</miter>
		<verbose>false</verbose>
		<linesearch>false</linesearch>
		<max_divide>2</max_divide>
		<force_divide>false</force_divide>
		<skip_first_step>false</skip_first_step>
  </{material}_vp>
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
            youngs     = 211000.0,
            poissons   = 0.30,
            cp_tau_s   = self.get_param("cp_tau_s"),
            cp_b       = self.get_param("cp_b"),
            cp_tau_0   = self.get_param("cp_tau_0"),
            cp_gamma_0 = self.get_param("cp_gamma_0"),
            cp_n       = self.get_param("cp_n"),
            vp_s0      = self.get_param("vp_s0"),
            vp_R       = self.get_param("vp_R"),
            vp_d       = self.get_param("vp_d"),
            vp_n       = self.get_param("vp_n"),
            vp_eta     = self.get_param("vp_eta"),
            slip_dir   = "1 1 0",
            slip_plane = "1 1 1"
        )
        return material_content
    