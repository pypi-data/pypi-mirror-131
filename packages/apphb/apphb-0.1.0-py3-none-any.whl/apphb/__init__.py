"""An application-level heartbeats interface."""
import dataclasses
from dataclasses import dataclass
from typing import List, Tuple, Union

#: Type for heartbeat field record `val` field.
HeartbeatFieldValue = Union[Tuple[int], Tuple[float], Tuple[int, int], Tuple[float, float]]
#: Type for heartbeat field record `glbl`, `wndw`, and `inst` fields.
HeartbeatFieldCount = Union[int, float]
#: Type for heartbeat field record `glbl_rate`, `wndw_rate`, and `inst_rate` fields.
HeartbeatFieldRate = float
#: Type for heartbeat record `ident` field.
HeartbeatIdentifier = Union[int, str]

#: Union of types in a heartbeat field record.
HeartbeatFieldRecordData = Union[HeartbeatFieldValue, HeartbeatFieldCount, HeartbeatFieldRate]
#: Union of types in a heartbeat record.
HeartbeatRecordData = Union[HeartbeatFieldRecordData, HeartbeatIdentifier]

@dataclass
class HeartbeatFieldRecord:
    """
    Contains user-specified values and computed global, window, and instant counts and rates.
    """
    val: HeartbeatFieldValue = (0,)
    """The record's reported value."""
    glbl: HeartbeatFieldCount = 0
    """The record's global sum."""
    wndw: HeartbeatFieldCount = 0
    """The record's window sum."""
    inst: HeartbeatFieldCount = 0
    """The record's instant value."""
    glbl_rate: HeartbeatFieldRate = 0
    """The record's global rate."""
    wndw_rate: HeartbeatFieldRate = 0
    """The record's window rate."""
    inst_rate: HeartbeatFieldRate = 0
    """The record's instant rate."""

    # NOTE: using 'HeartbeatFieldRecord' as type hint b/c Python doesn't currently support forward
    #       references in type hints.
    def copy(self, norm: HeartbeatFieldCount=None, rate_norm: HeartbeatFieldRate=None) -> \
        'HeartbeatFieldRecord':
        """
        Create a copy, optionally by normalizing values, counts, and rates.

        Parameters
        ----------
        norm : HeartbeatFieldCount, optional
            The normalization factor for `val` tuple values, `glbl`, `wndw`, and `inst`.
        rate_norm : HeartbeatFieldRate, optional
            The normalization factor for `glbl_rate`, `wndw_rate`, and `inst_rate`.

        Returns
        -------
        HeartbeatFieldRecord
            A new normalized instance.
        """
        copy = dataclasses.replace(self)
        if norm is not None:
            copy.val = tuple(v * norm for v in copy.val)
            copy.glbl *= norm
            copy.wndw *= norm
            copy.inst *= norm
        if rate_norm is not None:
            copy.glbl_rate *= rate_norm
            copy.wndw_rate *= rate_norm
            copy.inst_rate *= rate_norm
        return copy

@dataclass
class HeartbeatRecord:
    """
    Contains identifiers and `HeartbeatFieldRecord` instances for a heartbeat's fields.
    """
    ident: HeartbeatIdentifier = 0
    """The record's (preferably) unique identifier."""
    tag: HeartbeatIdentifier = 0
    """The record's (preferably) unique alternate identifier."""
    time: HeartbeatFieldRecord = dataclasses.field(default_factory=HeartbeatFieldRecord)
    """
    The record's time field.

    The `time` field is a special case.
    Other fields depend on it for computing their rates.
    In contrast, `time` rates are computed as heartbeat rates.
    """
    field_records: List[HeartbeatFieldRecord] = dataclasses.field(default_factory=list)
    """The record's other fields."""

class Heartbeat:
    """
    An application heartbeat interface for recording time and user-specified fields.

    Heartbeats store user-provided field values and compute global, window, and instant counts and
    rates.
    A circular window buffer stores recent heartbeats in memory.
    Users are responsible for saving (e.g., logging) data older than a window period, if desired.

    Time is the only required field, which computes rates as heart rates.
    All other user-specified fields compute rates w.r.t. the time field.
    Field units (including time units) are not specified by the API.

    Notes
    -----
    It may be desirable to capture and store metrics using high-precision units.
    For example, consider using a monotonic clock with high granularity like
    :meth:`time.monotonic_ns()`.

    Because the API doesn't enforce particular units, users might need to normalize when retrieving
    heartbeat data.
    For example, if time is provided in nanoseconds, divide values and counts by 1 billion to
    compute seconds, and multiply heart rates by 1 billion to compute heartbeats per second.
    Similarly, custom fields might need to be normalized w.r.t. their units, and in the case of
    rates, w.r.t. the ratio between their units and the time units.

    Parameters
    ----------
    window_size : int
        The heartbeat window period, where ``window_size > 0``.
    time_shape : int, optional
        The shape to be used for the :meth:`heartbeat` `time` parameter.
        The only acceptable values are ``1`` and ``2``.
        ``1`` implies using elapsed time, e.g., ``time=(elapsed_time,)``.
        ``2`` implies using start and end times, e.g., ``time=(start_time, end_time)``.
    fields_shape : Tuple[int, ...], optional
        The shape that will be used if supplying additional fields with each heartbeat.
        The only acceptable values in the tuple are ``1`` and ``2``.
        For example, if the :meth:`heartbeat` `fields` param is going to be:
        ``fields=[(total_value_1,), (start_value_2, end_value_2)]``,
        then the shape would be:
        ``fields_shape=(1, 2)``.
    """

    def __init__(self, window_size: int, time_shape: int=1, fields_shape: Tuple[int, ...]=None):
        """
        Initialize a heartbeat instance.
        """
        if window_size <= 0:
            raise ValueError('window_size must be > 0')
        if time_shape not in [1, 2]:
            raise ValueError('time_shape must be 1 or 2')
        self._time_shape = time_shape
        self._fields_shape = () if fields_shape is None else fields_shape
        for shape in self._fields_shape:
            if shape not in [1, 2]:
                raise ValueError('fields_shape values must be 1 or 2')
        self._window_buffer = \
            [HeartbeatRecord(field_records=[HeartbeatFieldRecord() for _ in
                                            range(len(self._fields_shape))])
             for _ in range(window_size)]
        self._counter = 0
        self._buffer_idx = 0

    def _record_heartbeat(self, tag, time, fields):
        prev = self._window_buffer[self._buffer_idx - 1]
        curr = self._window_buffer[self._buffer_idx]

        curr.ident = self._counter
        curr.tag = tag
        for fld, prev_rec, curr_rec in zip((time,) + fields,
                                           [prev.time] + prev.field_records,
                                           [curr.time] + curr.field_records):
            old_glbl = curr_rec.glbl
            inst = fld[0] if len(fld) == 1 else fld[1] - fld[0]
            curr_rec.val = fld
            curr_rec.glbl = prev_rec.glbl + inst
            curr_rec.wndw = curr_rec.glbl - old_glbl
            curr_rec.inst = inst
            curr_rec.glbl_rate = curr_rec.glbl / curr.time.glbl
            curr_rec.wndw_rate = curr_rec.wndw / curr.time.wndw
            curr_rec.inst_rate = curr_rec.inst / curr.time.inst
        # rates for the time field are a special case (heart rate), so recompute them:
        curr.time.glbl_rate = (curr.ident + 1) / curr.time.glbl
        curr.time.wndw_rate = min(curr.ident + 1, len(self._window_buffer)) / curr.time.wndw
        curr.time.inst_rate = 1 / curr.time.inst

    def heartbeat(self, tag: HeartbeatIdentifier, time: HeartbeatFieldValue,
                  fields: Tuple[HeartbeatFieldValue, ...]=None):
        """
        Issue a heartbeat.

        Parameters
        ----------
        tag : HeartbeatIdentifier
            A user-specified identifier - most likely a unique `int` value.
        time : HeartbeatFieldValue
            The elapsed/total or the start and end times for the record, depending on `time_shape`
            specified during initialization.
            However specified, the elapsed time must be positive, i.e., the following must hold:
            ``len(time) == 1 and time[0] > 0`` or
            ``len(time) == 2 and (time[1] - time[0]) > 0``.
        fields : Tuple[HeartbeatFieldValue, ...], optional
            The elapsed/total or start and end values for each field, depending on `fields_shape`
            specified during initialization.
        """
        # check and convert all parameters before modifying internal state
        if len(time) != self._time_shape:
            raise ValueError('time must have the same shape as specified in time_shape')
        if len(time) == 1 and time[0] <= 0:
            raise ValueError('elapsed time must be > 0')
        if len(time) > 1 and (time[1] - time[0]) <= 0:
            raise ValueError('time end must be > time start')
        if fields is None:
            fields = ()
        if len(fields) != len(self._window_buffer[0].field_records):
            raise ValueError('fields must have the same shape as specified in fields_shape')
        for fld, fld_shape in zip(fields, self._fields_shape):
            if len(fld) != fld_shape:
                raise ValueError('fields must have the same shape as specified in fields_shape')

        # record the heartbeat and update state
        self._record_heartbeat(tag, time, fields)
        self._counter += 1
        self._buffer_idx = (self._buffer_idx + 1) % len(self._window_buffer)

    @property
    def count(self):
        """int: The heartbeat count."""
        return self._counter

    @property
    def window_size(self):
        """int: The window size."""
        return len(self._window_buffer)

    @property
    def time_shape(self):
        """int: The time shape."""
        return self._time_shape

    @property
    def fields_shape(self):
        """Tuple[int, ...]: The fields shape."""
        return self._fields_shape

    def _to_buffer_index(self, off):
        """
        Get the buffer index relative to current buffer pointer and offset.
        We support -window_size <= off <= 0 to be consistent with Python indexing, although
        -window_size < off <= 0 would be slightly easier to compute (no modulo operation).
        """
        if off < -len(self._window_buffer) or off > 0:
            raise ValueError('Offset must be None or in range -' + str(len(self._window_buffer)) +
                             ' <= off <= 0')
        return (self._buffer_idx - 1 + off) % len(self._window_buffer)

    def get_record(self, off: int=0) -> HeartbeatRecord:
        """
        Get a heartbeat record (the last one, by default).

        Parameters
        ----------
        off : int, optional
            A negative offset relative to the last heartbeat to get older data.
            The value must be in range: ``-window_size <= off <= 0``.

        Returns
        -------
        HeartbeatRecord
            The desired record.

        Notes
        -----
        Modifying the record is strongly discouraged.
        Changes can affect future heartbeats which compute new values based on prior heartbeats,
        e.g., for global and window values.
        """
        return self._window_buffer[self._to_buffer_index(off)]

    def _to_field_record(self, off, fld):
        hbr = self._window_buffer[self._to_buffer_index(off)]
        return hbr.time if fld is None else hbr.field_records[fld]

    def get_value(self, off: int=0, fld: int=None) -> HeartbeatFieldValue:
        """
        Get a heartbeat field value.

        Parameters
        ----------
        off : int, optional
            A negative offset relative to the last heartbeat to get older data.
            The value must be in range: ``-window_size <= off <= 0``.
        fld : int, optional
            The `HeartbeatRecord` field.
            If `None`, the `time` field is used, otherwise ``field_records[fld]`` is used.

        Returns
        -------
        HeartbeatFieldValue
            The requested value.
        """
        hbfr = self._to_field_record(off, fld)
        return hbfr.val

    def get_global_count(self, off: int=0, fld: int=None) -> HeartbeatFieldCount:
        """
        Get a heartbeat field global count.

        Parameters
        ----------
        off : int, optional
            A negative offset relative to the last heartbeat to get older data.
            The value must be in range: ``-window_size <= off <= 0``.
        fld : int, optional
            The `HeartbeatRecord` field.
            If `None`, the `time` field is used, otherwise ``field_records[fld]`` is used.

        Returns
        -------
        HeartbeatFieldCount
            The requested global count.
        """
        hbfr = self._to_field_record(off, fld)
        return hbfr.glbl

    def get_window_count(self, off: int=0, fld: int=None) -> HeartbeatFieldCount:
        """
        Get a heartbeat field window count.

        Parameters
        ----------
        off : int, optional
            A negative offset relative to the last heartbeat to get older data.
            The value must be in range: ``-window_size <= off <= 0``.
        fld : int, optional
            The `HeartbeatRecord` field.
            If `None`, the `time` field is used, otherwise ``field_records[fld]`` is used.

        Returns
        -------
        HeartbeatFieldCount
            The requested window count.
        """
        hbfr = self._to_field_record(off, fld)
        return hbfr.wndw

    def get_instant_count(self, off: int=0, fld: int=None) -> HeartbeatFieldCount:
        """
        Get a heartbeat field instant count.

        Parameters
        ----------
        off : int, optional
            A negative offset relative to the last heartbeat to get older data.
            The value must be in range: ``-window_size <= off <= 0``.
        fld : int, optional
            The `HeartbeatRecord` field.
            If `None`, the `time` field is used, otherwise ``field_records[fld]`` is used.

        Returns
        -------
        HeartbeatFieldCount
            The requested instant count.
        """
        hbfr = self._to_field_record(off, fld)
        return hbfr.inst

    def get_global_rate(self, off: int=0, fld: int=None) -> HeartbeatFieldRate:
        """
        Get a heartbeat field global rate.

        Parameters
        ----------
        off : int, optional
            A negative offset relative to the last heartbeat to get older data.
            The value must be in range: ``-window_size <= off <= 0``.
        fld : int, optional
            The `HeartbeatRecord` field.
            If `None`, the `time` field is used, otherwise ``field_records[fld]`` is used.

        Returns
        -------
        HeartbeatFieldCount
            The requested global rate.
        """
        hbfr = self._to_field_record(off, fld)
        return hbfr.glbl_rate

    def get_window_rate(self, off: int=0, fld: int=None) -> HeartbeatFieldRate:
        """
        Get a heartbeat field window rate.

        Parameters
        ----------
        off : int, optional
            A negative offset relative to the last heartbeat to get older data.
            The value must be in range: ``-window_size <= off <= 0``.
        fld : int, optional
            The `HeartbeatRecord` field.
            If `None`, the `time` field is used, otherwise ``field_records[fld]`` is used.

        Returns
        -------
        HeartbeatFieldCount
            The requested window rate.
        """
        hbfr = self._to_field_record(off, fld)
        return hbfr.wndw_rate

    def get_instant_rate(self, off: int=0, fld: int=None) -> HeartbeatFieldRate:
        """
        Get a heartbeat field instant rate.

        Parameters
        ----------
        off : int, optional
            A negative offset relative to the last heartbeat to get older data.
            The value must be in range: ``-window_size <= off <= 0``.
        fld : int, optional
            The `HeartbeatRecord` field.
            If `None`, the `time` field is used, otherwise ``field_records[fld]`` is used.

        Returns
        -------
        HeartbeatFieldCount
            The requested instant rate.
        """
        hbfr = self._to_field_record(off, fld)
        return hbfr.inst_rate
