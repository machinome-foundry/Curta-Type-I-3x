"""Independent consumer expectations from Marcus Wu's 3x BOM and manual."""

import csv
import hashlib
import json
from pathlib import Path

from machinome.components import Standard
from machinome.model import ModelSnapshot, Reference
from machinome.node import AssemblyNode, StepNode
from machinome.production.process import Printed, Sourced
from machinome.simulation import Sim

from production.profile import CurtaDraft, ControlledReview
from simulation.crank_coupling_parts import SeatedMainCrank
from simulation.crank_grip_parts import SeatedCrankGrip
from simulation.mechanistic import MechanisticCurta


CRANK_PATHS = {
    "main_drive/crank/crank_handle_pin",
    "main_drive/crank/crank_handle_1/main_crank",
    "main_drive/crank/crank_handle_1/crank_handle",
    "main_drive/crank/crank_handle_1/crank_handle_pin_screw",
}
NUT_PATHS = {
    *(f"frame/fasteners/m4_nut_{i}" for i in range(1, 5)),
    *(f"frame/upper_frame/m4_nut_{i}" for i in range(1, 4)),
}
WIRE_PATHS = {
    *(f"carry_mechanism/result_carries/results_tens_lever_assembly_{i}/carry_lever_spring/wire"
      for i in range(1, 11)),
    *(f"carry_mechanism/turns_carries/turns_tens_lever_assembly_{i}/carry_lever_spring/wire"
      for i in range(1, 6)),
}
RETAINING_PATCH_PATHS = {
    f"carry_mechanism/tens_bell/tens_bell_spring/{suffix}"
    for suffix in ("mount", "right_arm/body", "left_arm/body", "right_hook", "left_hook")
}


def assigned(lines):
    return tuple(line for line in lines if line.status == "assigned")


def bom_facts(lines):
    """Compare consumer meaning without assuming profile-specific line IDs."""
    return tuple((line.status, line.process, line.quantity, line.occurrence_paths,
                  line.geometry_id, line.material, line.requirement, line.offer)
                 for line in lines)


def test_fresh_root_has_fifteen_actual_flexible_wires():
    model = MechanisticCurta()
    snapshot = ModelSnapshot(model)
    wires = {occ.path: occ for occ in snapshot.occurrences if occ.path in WIRE_PATHS}
    assert set(wires) == WIRE_PATHS
    assert all(occ.kind == "flexible-piece" for occ in wires.values())
    assert len(wires) == 15  # Manual page 30: ten result and five turns levers.
    assert snapshot.select(Reference(MechanisticCurta, ("main_drive", "crank")))[0].path == "main_drive/crank"
    crank = snapshot.select(Reference(MechanisticCurta,
                                     ("main_drive", "crank", "crank_handle_1", "main_crank")))[0]
    grip = snapshot.select(Reference(MechanisticCurta,
                                    ("main_drive", "crank", "crank_handle_1", "crank_handle")))[0]
    assert issubclass(crank.model_type, SeatedMainCrank)
    assert issubclass(grip.model_type, SeatedCrankGrip)


def test_structural_findings_and_steps_preserve_unassigned_wire_evidence(monkeypatch):
    def unexpected_geometry(*args, **kwargs):
        raise AssertionError("Structural production query requested assembly/geometry")

    # Public hooks: actual structural consumption must not need a full build.
    monkeypatch.setattr(AssemblyNode, "assemble", unexpected_geometry)
    monkeypatch.setattr(AssemblyNode, "build_stls", unexpected_geometry)
    monkeypatch.setattr(StepNode, "build_stls", unexpected_geometry)
    production = CurtaDraft(MechanisticCurta())
    missing = {path for finding in production.findings if finding.code == "unassigned"
               for path in finding.occurrences}
    assert WIRE_PATHS <= missing
    steps = production.steps
    assert any("0.6 mm" in step.instruction_text and "57 mm" in step.instruction_text
               for step in steps)
    assert any("simulation-only" in step.instruction_text for step in steps)
    assert any("five" in step.instruction_text and "retaining spring" in step.instruction_text
               for step in steps)
    assert production.crank.pin.target_paths == ("main_drive/crank/crank_handle_pin",)
    assert sum(line.quantity for line in assigned(production.frame_nuts.bom)) == 4
    assert sum(line.quantity for line in assigned(production.upper_frame_nuts.bom)) == 3


def test_child_source_files_and_instruction_scope_are_local():
    production = CurtaDraft(MechanisticCurta())
    steps = production.steps
    assembly_files = [step for step in steps if step.instruction_path.name == "assembly.md"]
    assert {step.instruction_path.parent.name for step in assembly_files} == {"crank", "frame", "upper_frame"}
    assert len({step.instruction_sha256 for step in assembly_files}) == 3
    for step in assembly_files:
        assert hashlib.sha256(step.instruction_path.read_bytes()).hexdigest() == step.instruction_sha256
    by_subject = {path: step for step in steps for path in step.subject_paths}
    assert by_subject["main_drive/crank/crank_handle_1/crank_handle_pin_screw"].instruction_path.parent.name == "crank"
    assert by_subject["frame/fasteners/m4_nut_1"].instruction_path.parent.name == "frame"


def test_root_bom_reconciles_four_printed_units_and_seven_standard_nuts():
    production = CurtaDraft(MechanisticCurta())
    lines = production.bom
    printed = [line for line in assigned(lines) if isinstance(line.process, Printed)]
    nuts = [line for line in assigned(lines) if isinstance(line.process, Sourced)]
    assert sum(line.quantity for line in printed) == 4
    assert {path for line in printed for path in line.occurrence_paths} == CRANK_PATHS
    assert all(line.material is None for line in printed)
    assert all(line.geometry_id for line in printed)
    assert len(nuts) == 1
    assert nuts[0].quantity == 7
    assert set(nuts[0].occurrence_paths) == NUT_PATHS
    assert nuts[0].requirement == Standard("DIN 934", designation="M4x0.7")
    assert nuts[0].offer is None and nuts[0].geometry_id is None
    missing = {path for line in lines if line.status == "unassigned" for path in line.occurrence_paths}
    assert WIRE_PATHS <= missing
    assert RETAINING_PATCH_PATHS <= missing
    assert len(RETAINING_PATCH_PATHS) == 5  # Five candidates, not five author springs.
    assert all(line.quantity == 1 and line.geometry_id is None
               for line in lines if line.status == "unassigned")
    assert sum(line.quantity for line in assigned(production.frame_nuts.bom)) == 4
    assert sum(line.quantity for line in assigned(production.upper_frame_nuts.bom)) == 3


def test_profiles_and_access_orders_preserve_nondefault_running_state():
    model = MechanisticCurta()
    sim = Sim(model, dt=0.02, state={"digit_1": 1})
    sim.move("marker_1_rotation", to=5)
    sim.run(0.02)
    before = sim.snapshot()
    parameters_before = {occ.path: dict(occ.parameters)
                         for occ in ModelSnapshot(model).occurrences}
    project = Path(__file__).resolve().parents[1]
    source_files = (*sorted((project / "simulation").rglob("*.py")),
                    project / "pyproject.toml", project / "CAD" / "Curta Assembly.step")
    source_hashes = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in source_files}
    source = CurtaDraft(model)
    opposite_order = CurtaDraft(model)
    review = ControlledReview(model)
    child_first = source.frame_nuts.bom
    root_first = opposite_order.bom
    assert source.frame_nuts.bom == child_first
    assert bom_facts(source.bom) == bom_facts(root_first)
    assert opposite_order.frame_nuts.bom == child_first
    assert bom_facts(source.bom) == bom_facts(review.bom)
    assert source.findings == review.findings
    assert source.mass == review.mass
    assert source.steps != review.steps
    assert sim.snapshot() == before
    assert {occ.path: dict(occ.parameters) for occ in ModelSnapshot(model).occurrences} == parameters_before
    assert {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in source_files} == source_hashes
    assert sim.state["digit_1"] == 1
    assert sim.state["marker_1_rotation"] == 5
    assert not source.mass.complete
    assert WIRE_PATHS <= set(source.mass.unknown_occurrences)
    # Reading an asset must not retire the live run or rewrite its command bindings.
    sim.move("marker_1_rotation", to=6)
    assert sim.state["marker_1_rotation"] == 6


def test_export_is_a_traceable_partial_draft(tmp_path):
    production = CurtaDraft(MechanisticCurta())
    result = production.export(tmp_path / "curta-draft")
    assert not result.coverage_complete
    assert result.executed_code_provenance == "unverified-direct-binding"
    manifest = json.loads((result.path / "production.json").read_text())
    assert manifest["format"] == "machinome-production" and manifest["version"] == 1
    instructions = (result.path / "instructions.md").read_text()
    assert "simulation-only" in instructions and "DIN 934" in instructions
    assert "57 mm" in instructions and "five" in instructions
    with (result.path / "bom.csv").open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert sum(int(row["quantity"]) for row in rows if row["status"] == "assigned") == 11
    exported_missing = {path for row in rows if row["status"] == "unassigned"
                        for path in json.loads(row["occurrence_paths"])}
    assert WIRE_PATHS <= exported_missing
    artifacts = tuple((result.path / "artifacts").iterdir())
    assert len(artifacts) == 4 and all(path.suffix == ".stl" for path in artifacts)
    assert all(path.stem == hashlib.sha256(path.read_bytes()).hexdigest() for path in artifacts)
    assert len(tuple((result.path / "files").glob("*/assembly.md"))) == 3
    # No fabricated measurement: the whole current model still has unknown mass.
    assert not production.mass.complete and production.mass.known_grams == 0
