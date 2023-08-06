"""Heartbeat logging utilities."""
import dataclasses
from typing import List
from apphb import Heartbeat, HeartbeatFieldCount, HeartbeatFieldRate, HeartbeatRecord, \
                  HeartbeatRecordData

def get_log_header(hbt: Heartbeat, time_name: str='Time', heartrate_name: str='Heart Rate',
                   field_names: List[str]=None, field_rate_names: List[str]=None) -> List[str]:
    """
    Get a heartbeat header for logging.

    The first entries are always 'Heartbeat' and 'Tag'.
    'Heartbeat' is the internal identifier.
    'Tag' is the user-specified identifier.
    Then for each field, including `time`:

        The field shape determines whether one or two entries will be used for the value, where two
        columns implies Start and End values.
        Then entries for Global, Window, and Instant counts, then Global, Window, and Instant rates.

    The first field name is 'Time' with corresponding rate name 'Heart Rate'.
    User-specified fields and their corresponding rate names follow.

    Parameters
    ----------
    hbt : Heartbeat
        The heartbeat instance.
    time_name : str, optional
        Custom name for the `time` field, e.g., to specify units.
    heartrate_name : str, optional
        Custom name for the heartrate (rates for the `time` field), e.g., to specify units.
    field_names : List[str], optional
        Names for user-specified fields.
    field_rate_names : List[str], optional
        Rate names for user-specified fields.
        If not specified, the corresponding field name is used with 'Rate' appended to it.
        If ``len(field_rate_names) < len(field_names)``, 'Rate' is appended to remaining names.

    Returns
    -------
    List[str]
        The list of names for all identifiers and fields in a heartbeat record.
    """
    names = [str(time_name)]
    rate_names = [str(heartrate_name)]
    if field_names is not None:
        names.extend(field_names)
    if field_rate_names is not None:
        rate_names.extend(field_rate_names)
    field_shapes = (hbt.time_shape,) + hbt.fields_shape
    names.extend(['Field ' + str(i) for i in range(len(names), len(field_shapes))])
    rate_names.extend([n + ' Rate' for n in names[len(rate_names):]])
    hdrs = ['Heartbeat', 'Tag']
    for field_len, name, name_rate in zip(field_shapes, names, rate_names):
        if field_len == 1:
            hdrs.append(str(name))
        else:
            hdrs.extend(['Start ' + str(name), 'End ' + str(name)])
        for suffix in [str(name), str(name_rate)]:
            for prefix in ['Global', 'Window', 'Instant']:
                hdrs.append(prefix + ' ' + suffix)
    return hdrs

def get_log_record(hbr: HeartbeatRecord, time_norm: HeartbeatFieldCount=None,
                   heartrate_norm: HeartbeatFieldRate=None,
                   field_norms: List[HeartbeatFieldCount]=None,
                   field_rate_norms: List[HeartbeatFieldRate]=None) -> List[HeartbeatRecordData]:
    """
    Get a heartbeat record for logging.

    Parameters
    ----------
    hbr : HeartbeatRecord
        The heartbeat record to be logged.
    time_norm : HeartbeatFieldCount, optional
        The normalization factor for the `time` field's `val`, `glbl`, `wndw`, and `inst` values.
    heartrate_norm : HeartbeatFieldRate, optional
        The normalization factor for the `time` field's `glbl_rate`, `wndw_rate`, and `inst_rate`
        values.
    field_norms : List[HeartbeatFieldCount], optional
        The normalization factor for user-specified fields' `val`, `glbl`, `wndw`, and `inst`
        values.
        The entire parameter or individual elements may be `None`.
    field_rate_norms : List[HeartbeatFieldRate], optional
        The normalization factor for user-specified fields' `glbl_rate`, `wndw_rate`, and
        `inst_rate` values.
        The entire parameter or individual elements may be `None`.

    Returns
    -------
    List[HeartbeatRecordData]
        The heartbeat record data.
    """
    values = [hbr.ident, hbr.tag]
    norm = [time_norm]
    rate_norm = [heartrate_norm]
    if field_norms is not None:
        norm.extend(field_norms)
    if field_rate_norms is not None:
        rate_norm.extend(field_rate_norms)
    # time field + custom fields + 1 (for excluded range stop value)
    total_range = 1 + len(hbr.field_records) + 1
    norm.extend([None for _ in range(total_range - len(norm))])
    rate_norm.extend([None for _ in range(total_range - len(rate_norm))])
    for rec, field_norm, field_rate_norm in zip([hbr.time] + hbr.field_records, norm, rate_norm):
        norm_rec = rec.copy(norm=field_norm, rate_norm=field_rate_norm)
        values.extend(norm_rec.val)
        values.extend(dataclasses.astuple(norm_rec)[1:])
    return values

# pylint: disable=R0913
def get_log_records(hbt: Heartbeat, count: int=None, time_norm: HeartbeatFieldCount=None,
                    heartrate_norm: HeartbeatFieldRate=None,
                    field_norms: List[HeartbeatFieldCount]=None,
                    field_rate_norms: List[HeartbeatFieldRate]=None) -> \
    List[List[HeartbeatRecordData]]:
    """
    Get heartbeat records for logging.

    Parameters
    ----------
    hbt : Heartbeat
        The heartbeat to be logged.
    count : int, optional
        The number of historical records to get, where ``0 <= count <= window_size``.
        If `None`, returns the previous window history.
    time_norm : HeartbeatFieldCount, optional
        The normalization factor for the `time` field's `val`, `glbl`, `wndw`, and `inst` values.
    heartrate_norm : HeartbeatFieldRate, optional
        The normalization factor for the `time` field's `glbl_rate`, `wndw_rate`, and `inst_rate`
        values.
    field_norms : List[HeartbeatFieldCount], optional
        The normalization factor for user-specified fields' `val`, `glbl`, `wndw`, and `inst`
        values.
        The entire parameter or individual elements may be `None`.
    field_rate_norms : List[HeartbeatFieldRate], optional
        The normalization factor for user-specified fields' `glbl_rate`, `wndw_rate`, and
        `inst_rate` values.
        The entire parameter or individual elements may be `None`.

    Returns
    -------
    List[List[HeartbeatRecordData]]
        The heartbeat records data.
    """
    if count is None:
        count = hbt.window_size
    if count < 0 or count > hbt.window_size:
        raise ValueError('count must be in range: 0 <= count <= window_size')
    # this "range" allows count=window_size+1 (per Heartbeat.get_record) so we need the check above
    # pylint: disable=E1130 # (count will not be NoneType here)
    recs = [hbt.get_record(off=off) for off in range(-count + 1, 1)]
    return [get_log_record(r, time_norm=time_norm, heartrate_norm=heartrate_norm,
                           field_norms=field_norms, field_rate_norms=field_rate_norms)
            for r in recs]
