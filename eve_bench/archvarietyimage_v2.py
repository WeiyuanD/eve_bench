# ArchVarietyImage V2 for SOFA v24.12
import math
import eve


class ArchVarietyImageV2(eve.intervention.MonoPlaneStatic):
    def __init__(
        self,
        episodes_between_arch_change: int = 1,
        stop_instrument_at_tree_end: bool = True,
        normalize_action: bool = False,
    ) -> None:
        vessel_tree = eve.intervention.vesseltree.AorticArchRandom(
            # scale_width_array = [1.0],
            # scale_heigth_array = [1.0],
            episodes_between_change=episodes_between_arch_change,
            scale_diameter_array=[0.85],
            arch_types_filter=[eve.intervention.vesseltree.ArchType.I],
        )
        instrument = eve.intervention.instrument.Angled(
            name="guidewire",
            velocity_limit=(50, 3.14),
            length=450,
            tip_radius=12.1,
            tip_angle_deg=0.4 * 180,

            diameter_outer=0.89,
            diameter_inner=0.0,
            young_modulus=80e3,
            mass_density=0.000021,
            poisson_ratio=0.49,
            collis_edges_per_mm=0.1,
            visu_edges_per_mm=0.5,

            flex_length=30.0,
            flex_diameter_outer=0.7,
            flex_diameter_inner=0.0,
            flex_young_modulus=17e3,
            flex_mass_density=0.000021,
            flex_poisson_ratio=0.49,
            flex_collis_edges_per_mm=2,
            flex_visu_edges_per_mm=0.5,

            color=(0.0, 0.0, 0.0),

            arc_mesh_resolution=0.1,
        )

        simulation = eve.intervention.simulation.SofaBeamAdapter(friction=0.1)


        # fluoroscopy = eve.intervention.fluoroscopy.Pillow(
        #     simulation=simulation,
        #     vessel_tree=vessel_tree,
        #     image_frequency=7.5,
        #     image_rot_zx=[25, 0],
        #     image_center=[0, 0, 0],
        #     field_of_view=None,
        # )

        fluoroscopy = eve.intervention.fluoroscopy.Pillow(
            simulation=simulation,
            vessel_tree=vessel_tree,
            # image_size=[128, 128],
            image_frequency=7.5,
            image_rot_zx=[0, 0],
        )


        target = eve.intervention.target.CenterlineRandom(
            vessel_tree=vessel_tree,
            fluoroscopy=fluoroscopy,
            threshold=5,
            branches=["lcca", "rcca", "lsa", "rsa", "bct", "co"],
        )


        super().__init__(
            vessel_tree,
            [instrument],
            simulation,
            fluoroscopy,
            target,
            stop_instrument_at_tree_end,
            normalize_action,
        )

    @property
    def episodes_between_arch_change(self) -> int:
        return self.vessel_tree.episodes_between_change



