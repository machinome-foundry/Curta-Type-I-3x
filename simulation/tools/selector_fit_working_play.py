"""Read-only contact/play witnesses for the ratified guide and source captures.

Sampled extrema localize the remaining proof. They are deliberately not a
continuous-stroke certificate or a ball trajectory installed in the model.
"""

import argparse
import hashlib
import json
import logging
from pathlib import Path

import numpy as np

from simulation.tools.selector_fit_alignment import native_source, measured_guide
from simulation.tools.selector_fit_contacts import closest, radial_support


def overlap(a, b):
    common = a.intersect(b)
    valid, volume = common.isValid(), common.Volume()
    if not valid or volume < 0:
        return dict(kernel_refusal=True, valid=valid, signed_volume_mm3=volume)
    return dict(kernel_refusal=False, overlap_mm3=volume)


def ball_measurements(source):
    guide, _, center = measured_guide(source['knob'], source['shaft'])
    play = guide.Radius()-2.5
    rows = []
    settings = sorted(set([i/20 for i in range(21)] + [-.05, -.025, -.0125, .0125, .025,
                                                   .975, .9875, 1.0125, 1.025, 1.05]))
    for q in settings:
        shaft = source['shaft'].rotate((58.5, 0, 0), (58.5, 0, 1), 36*q)
        offsets = [(0., 0.)]
        if q in (-.05, -.025, 0, .025, .05, .5, .95, .975, 1, 1.025, 1.05):
            offsets += [(play, 0), (-play, 0), (0, play), (0, -play)]
        samples = []
        for dy, dz in offsets:
            sample = radial_support(shaft, center[2]-6*q+dz, center[1]+dy)
            samples.append(dict(offset_yz_mm=[dy, dz], **sample))
        row = dict(setting=q, legal_stroke=(0 <= q <= 9), samples=samples)
        rows.append(row)
        print(json.dumps(dict(phase='ball_support', **row)), flush=True)
    return dict(guide_center_mm=center.tolist(), nominal_radial_play_mm=play,
                samples=rows,
                limitations=['Cardinal play samples do not exhaust the disk',
                             'Source linear shaft phase, not yet a fitted groove-following law',
                             'Below-zero setting is a local diagnostic extrapolation, not admitted travel',
                             'No full-travel or retention-basin certificate from this grid'])


def capture_measurements(source):
    screw, shaft, knob, group = (source[name] for name in ('screw', 'shaft', 'knob', 'group'))
    followers = []
    for q in (0, .125, .25, .375, .5, .625, .75, .875, 1, 4.5, 8.5, 9):
        pin = screw.translate((0, 0, -6*q))
        values = []
        for delta in (-1, -.05, 0, .05, 1):
            current = shaft.rotate((58.5, 0, 0), (58.5, 0, 1), 36*q+delta)
            values.append(dict(phase_delta_deg=delta, **overlap(current, pin),
                               closest=closest(current, pin)))
        row = dict(setting=q, phase_samples=values)
        followers.append(row)
        print(json.dumps(dict(phase='follower_capture', **row)), flush=True)
    forks = []
    for fixture, angle in (('initial', 0), ('postcarry', -648)):
        gear = group.rotate((40.5, 0, 0), (40.5, 0, 1), angle)
        values = []
        for shift in (-.5, -.2, -.1, -.05, -.025, 0, .025, .05, .1, .2, .5):
            moved = gear.translate((0, 0, shift))
            values.append(dict(axial_shift_mm=shift, **overlap(knob, moved),
                               closest=closest(knob, moved)))
        row = dict(fixture=fixture, samples=values)
        forks.append(row)
        print(json.dumps(dict(phase='fork_capture', **row)), flush=True)
    return dict(follower=followers, fork=forks,
                limitations=['Perturbation localization only; zero sampled overlap is not continuous capture proof',
                             'No follower-tip cut or between-detent phase change is installed'])


def measure(mode):
    source = native_source()
    result = dict(kind='selected-input-working-play-localization', mode=mode,
                  planning_commit='da432fbdc7fe0e7f89e308237f281e9c3d368754',
                  measurements=(ball_measurements(source) if mode == 'ball' else capture_measurements(source)))
    output = Path('_build_evidence/selector-fit-'+mode+'-play.json')
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(dict(output=str(output), sha256=hashlib.sha256(output.read_bytes()).hexdigest())), flush=True)


if __name__ == '__main__':
    logging.disable(logging.INFO)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('ball', 'capture'))
    measure(parser.parse_args().mode)
