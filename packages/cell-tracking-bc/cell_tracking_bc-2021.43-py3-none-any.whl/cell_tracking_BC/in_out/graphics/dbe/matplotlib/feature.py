# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# TODO: this implementation is a temporary solution to plotting division and death events. It should be replaced with
#     two_d_feature.py in generic. This will also be the occasion to extract the axes_track of two_d_tracking, make it
#     something similar to the future two_d_feature, and trun them both into embeddable axes as is two_d_sequence.

from typing import Dict, Sequence, Tuple

import matplotlib.lines as lins
import matplotlib.pyplot as pypl
import numpy as nmpy
from matplotlib.legend_handler import HandlerTuple as tuple_handler_t
from matplotlib.patches import Rectangle as rectangle_t


DIVISION_MARKER = "3"
DEATH_MARKER = "x"
DIVISION_MARKER_SIZE = 60
DEATH_MARKER_SIZE = 30
N_SCORE_LEGEND_SHADES = 8


def ShowDivisionAndDeathEventResponses(
    cell_division_response: Dict[int, Sequence[float]],
    cell_death_response: Dict[int, Sequence[float]],
    cell_division_frame_idc: Dict[int, Sequence[int]],
    cell_death_frame_idc: Dict[int, int],
    sequence_length: int,
    /,
    *,
    zero_is_black: bool = True,
) -> None:
    """"""
    max_label, div_values, dea_values, rectangles = _ValuesAndRectangles(
        cell_division_response,
        cell_death_response,
        cell_division_frame_idc,
        cell_death_frame_idc,
    )
    if rectangles.__len__() == 0:
        return

    events = _DivisionAndDeathEvents(
        div_values, dea_values, rectangles, zero_is_black=zero_is_black
    )

    figure, axes = pypl.subplots()

    for rectangle, _ in rectangles:
        axes.add_artist(rectangle)
    if zero_is_black:
        color = "w"
    else:
        color = "k"
    for what, size, where in events:
        axes.scatter(*where, c=color, marker=what, s=size)
    _SetAxesProperties(axes, sequence_length, max_label)
    _AddLegend(axes, zero_is_black=zero_is_black)

    figure.tight_layout()
    pypl.show()


def _ValuesAndRectangles(
    cell_division_response: Dict[int, Sequence[float]],
    cell_death_response: Dict[int, Sequence[float]],
    cell_division_frame_idc: Dict[int, Sequence[int]],
    cell_death_frame_idc: Dict[int, int],
    /,
) -> Tuple[
    int,
    Sequence[float],
    Sequence[float],
    Sequence[Tuple[rectangle_t, Tuple[float, float, bool, bool]]],
]:
    """"""
    max_label = max(max(cell_division_response.keys()), max(cell_death_response.keys()))
    div_values = []
    dea_values = []
    rectangles = []

    for (
        (label, division_response),
        death_response,
        division_time_points,
        death_frame_idx,
    ) in zip(
        cell_division_response.items(),
        cell_death_response.values(),
        cell_division_frame_idc.values(),
        cell_death_frame_idc.values(),
    ):
        if division_response is None:
            continue

        div_values.extend(division_response)
        dea_values.extend(death_response)

        death_occurred = (death_frame_idx is not None) and (death_frame_idx >= 0)
        for t_idx, (div_value, dea_value) in enumerate(
            zip(division_response, death_response)
        ):
            if division_response is None:
                continue
            if death_occurred and (t_idx > death_frame_idx):
                break

            # Note: division_time_points is (-1,) if no divisions
            dividing = t_idx in division_time_points
            dying = t_idx == death_frame_idx
            rectangle = (
                rectangle_t((t_idx, label - 0.5), 1.0, 1.0, edgecolor="none"),
                (div_value, dea_value, dividing, dying),
            )
            rectangles.append(rectangle)

    return max_label, div_values, dea_values, rectangles


def _DivisionAndDeathEvents(
    div_values: Sequence[float],
    dea_values: Sequence[float],
    rectangles: Sequence[Tuple[rectangle_t, Tuple[float, float, bool, bool]]],
    /,
    *,
    zero_is_black: bool = True,
) -> Sequence[Tuple[str, int, Sequence[float]]]:
    """"""
    output = []

    min_div_value = min(div_values)
    max_div_value = max(div_values)
    div_scaling = 1.0 / (max_div_value - min_div_value)

    min_dea_value = min(dea_values)
    max_dea_value = max(dea_values)
    dea_scaling = 1.0 / (max_dea_value - min_dea_value)

    for rectangle, (div_value, dea_value, dividing, dying) in rectangles:
        div = div_scaling * (div_value - min_div_value)
        dea = dea_scaling * (dea_value - min_dea_value)
        if zero_is_black:
            color = (dea, 0.0, div)
        else:
            div_color = (1.0 - div, 1.0 - div, 1.0)
            dea_color = (1.0, 1.0 - dea, 1.0 - dea)
            color = nmpy.minimum(div_color, dea_color)
        rectangle.set_facecolor(color)

        if dividing or dying:
            where = tuple(_crd + 0.5 for _crd in rectangle.get_xy())
            if dividing:
                output.append((DIVISION_MARKER, DIVISION_MARKER_SIZE, where))
            if dying:
                output.append((DEATH_MARKER, DEATH_MARKER_SIZE, where))

    return output


def _SetAxesProperties(
    axes: pypl.Axes, sequence_length: int, max_label: int, /
) -> None:
    """"""
    axes.set_xlim(left=0, right=sequence_length)
    axes.set_ylim(bottom=0, top=max_label + 1)

    positions = range(1, max_label + 1, max(1, int(round(max_label / 10))))
    axes.yaxis.set_ticks(positions)
    axes.yaxis.set_ticklabels(positions)


def _AddLegend(axes: pypl.Axes, /, *, zero_is_black: bool = True) -> None:
    """"""
    shades = nmpy.linspace(0.0, 1.0, num=N_SCORE_LEGEND_SHADES)

    if zero_is_black:
        DivisionColor = lambda _shd: (0.0, 0.0, _shd)
        DeathColor = lambda _shd: (_shd, 0.0, 0.0)
    else:
        DivisionColor = lambda _shd: (1.0 - _shd, 1.0 - _shd, 1.0)
        DeathColor = lambda _shd: (1.0, 1.0 - _shd, 1.0 - _shd)
    score_legends = [
        [
            rectangle_t(
                (0, 0),
                3.0,
                5.0,
                edgecolor="none",
                facecolor=_Clr(_shd),
            )
            for _shd in shades
        ]
        for _Clr in (DivisionColor, DeathColor)
    ]

    event_legends = [
        lins.Line2D(
            (),
            (),
            color="k",
            marker=_mrk,
            markersize=_sze,
            linestyle="none",
        )
        for _mrk, _sze in (
            (DIVISION_MARKER, DIVISION_MARKER_SIZE // 5),
            (DEATH_MARKER, DEATH_MARKER_SIZE // 5),
        )
    ]

    axes.legend(
        handles=(*score_legends, *event_legends),
        labels=("Division Score", "Death Score", "Division", "Death"),
        loc="right",
        bbox_to_anchor=(1.3, 0.5),
        handler_map={list: tuple_handler_t(ndivide=None, pad=0)},
    )
