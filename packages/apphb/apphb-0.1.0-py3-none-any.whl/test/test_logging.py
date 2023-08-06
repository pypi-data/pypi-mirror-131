# pylint: disable=C0116
"""Test logging.py"""
import unittest
from apphb import logging
from apphb import Heartbeat, HeartbeatFieldRecord, HeartbeatRecord

class TestLogging(unittest.TestCase):
    """Test logging module"""

    BASE_HDRS = ['Heartbeat', 'Tag']
    TIME_HDRS = ['Time', 'Global Time', 'Window Time', 'Instant Time']
    TIME_RATE_HDRS = ['Global Heart Rate', 'Window Heart Rate', 'Instant Heart Rate']
    FOO_NAME = 'Foo'
    FOO_HDRS = ['Foo', 'Global Foo', 'Window Foo', 'Instant Foo']
    FOO_START_STOP_HDRS = ['Start Foo', 'End Foo', 'Global Foo', 'Window Foo', 'Instant Foo']
    FOO_RATE_HDRS = ['Global Foo Rate', 'Window Foo Rate', 'Instant Foo Rate']
    BAR_RATE_NAME = 'Bar'
    BAR_RATE_HDRS = ['Global Bar', 'Window Bar', 'Instant Bar']
    FIELD2_HDRS = ['Field 2', 'Global Field 2', 'Window Field 2', 'Instant Field 2']
    FIELD2_RATE_HDRS = ['Global Field 2 Rate', 'Window Field 2 Rate', 'Instant Field 2 Rate']

    def test_get_log_header(self):
        hbt = Heartbeat(1)
        hdrs = logging.get_log_header(hbt)
        self.assertEqual(hdrs, TestLogging.BASE_HDRS +
                               TestLogging.TIME_HDRS + TestLogging.TIME_RATE_HDRS)

    def test_get_log_header_time_name(self):
        hbt = Heartbeat(1)
        hdrs = logging.get_log_header(hbt, time_name='Time (ns)')
        time_headers = [n + ' (ns)' for n in TestLogging.TIME_HDRS]
        self.assertEqual(hdrs, TestLogging.BASE_HDRS +
                               time_headers + TestLogging.TIME_RATE_HDRS)

    def test_get_log_header_heartrate_name(self):
        hbt = Heartbeat(1)
        hdrs = logging.get_log_header(hbt, heartrate_name='Heart Rate (hb/s)')
        heartrate_headers = [n + ' (hb/s)' for n in TestLogging.TIME_RATE_HDRS]
        self.assertEqual(hdrs, TestLogging.BASE_HDRS +
                               TestLogging.TIME_HDRS + heartrate_headers)

    def test_get_log_header_field_names(self):
        hbt = Heartbeat(1, fields_shape=(1,))
        hdrs = logging.get_log_header(hbt, field_names=[TestLogging.FOO_NAME])
        self.assertEqual(hdrs, TestLogging.BASE_HDRS +
                               TestLogging.TIME_HDRS + TestLogging.TIME_RATE_HDRS +
                               TestLogging.FOO_HDRS + TestLogging.FOO_RATE_HDRS)

    def test_get_log_header_field_names_shape_two(self):
        hbt = Heartbeat(1, fields_shape=(2,))
        hdrs = logging.get_log_header(hbt, field_names=[TestLogging.FOO_NAME])
        self.assertEqual(hdrs, TestLogging.BASE_HDRS +
                               TestLogging.TIME_HDRS + TestLogging.TIME_RATE_HDRS +
                               TestLogging.FOO_START_STOP_HDRS + TestLogging.FOO_RATE_HDRS)

    def test_get_log_header_field_rate_names(self):
        hbt = Heartbeat(1, fields_shape=(1,))
        hdrs = logging.get_log_header(hbt, field_names=[TestLogging.FOO_NAME],
                                      field_rate_names=[TestLogging.BAR_RATE_NAME])
        self.assertEqual(hdrs, TestLogging.BASE_HDRS +
                               TestLogging.TIME_HDRS + TestLogging.TIME_RATE_HDRS +
                               TestLogging.FOO_HDRS + TestLogging.BAR_RATE_HDRS)

    def test_get_log_header_field_names_partial(self):
        hbt = Heartbeat(1, fields_shape=(1, 1))
        # Providing name for the first field but not the second
        hdrs = logging.get_log_header(hbt, field_names=[TestLogging.FOO_NAME])
        self.assertEqual(hdrs, TestLogging.BASE_HDRS +
                               TestLogging.TIME_HDRS + TestLogging.TIME_RATE_HDRS +
                               TestLogging.FOO_HDRS + TestLogging.FOO_RATE_HDRS +
                               TestLogging.FIELD2_HDRS + TestLogging.FIELD2_RATE_HDRS)

    def test_get_log_header_tuples(self):
        hbt = Heartbeat(1, fields_shape=(1,))
        hdrs = logging.get_log_header(hbt, field_names=(TestLogging.FOO_NAME,),
                                      field_rate_names=(TestLogging.BAR_RATE_NAME,))
        self.assertEqual(hdrs, TestLogging.BASE_HDRS +
                               TestLogging.TIME_HDRS + TestLogging.TIME_RATE_HDRS +
                               TestLogging.FOO_HDRS + TestLogging.BAR_RATE_HDRS)

    def test_get_log_record(self):
        hbr = HeartbeatRecord(ident=1, tag=2,
                              time=HeartbeatFieldRecord(val=(0, 1), glbl=3, wndw=2, inst=1,
                                                        glbl_rate=1, wndw_rate=2, inst_rate=1))
        rec = logging.get_log_record(hbr)
        self.assertEqual(rec, [1, 2, 0, 1, 3, 2, 1, 1, 2, 1])

    def test_get_log_record_fields(self):
        hbr = HeartbeatRecord(ident=1, tag=2,
                              time=HeartbeatFieldRecord(val=(0, 1), glbl=3, wndw=2, inst=1,
                                                        glbl_rate=1, wndw_rate=2, inst_rate=1),
                              field_records=[HeartbeatFieldRecord(val=(1, 2), glbl=3, wndw=4,
                                                                  inst=5, glbl_rate=6, wndw_rate=7,
                                                                  inst_rate=8)])
        rec = logging.get_log_record(hbr)
        self.assertEqual(rec, [1, 2,
                               0, 1, 3, 2, 1, 1, 2, 1,
                               1, 2, 3, 4, 5, 6, 7, 8])

    def test_get_log_record_norm(self):
        hbr = HeartbeatRecord(ident=1, tag=2,
                              time=HeartbeatFieldRecord(val=(0, 1), glbl=3, wndw=2, inst=1,
                                                        glbl_rate=1, wndw_rate=2, inst_rate=1),
                              field_records=[HeartbeatFieldRecord(val=(1, 2), glbl=3, wndw=4,
                                                                  inst=5, glbl_rate=6, wndw_rate=7,
                                                                  inst_rate=8)])
        rec = logging.get_log_record(hbr, time_norm=2, heartrate_norm=0.5, field_norms=[0.5],
                                     field_rate_norms=[2])
        self.assertAlmostEqual(rec, [1, 2,
                                     0, 2, 6, 4, 2, 0.5, 1, 0.5,
                                     0.5, 1, 1.5, 2, 2.5, 12, 14, 16])

    def test_get_log_record_tuples(self):
        hbr = HeartbeatRecord(ident=1, tag=2,
                              time=HeartbeatFieldRecord(val=(0, 1), glbl=3, wndw=2, inst=1,
                                                        glbl_rate=1, wndw_rate=2, inst_rate=1),
                              field_records=[HeartbeatFieldRecord(val=(1, 2), glbl=3, wndw=4,
                                                                  inst=5, glbl_rate=6, wndw_rate=7,
                                                                  inst_rate=8)])
        rec = logging.get_log_record(hbr, time_norm=2, heartrate_norm=0.5, field_norms=(0.5,),
                                     field_rate_norms=(2,))
        self.assertAlmostEqual(rec, [1, 2,
                                     0, 2, 6, 4, 2, 0.5, 1, 0.5,
                                     0.5, 1, 1.5, 2, 2.5, 12, 14, 16])

    def test_get_log_records(self):
        hbt = Heartbeat(3)
        hbt.heartbeat(0, (1,))
        hbt.heartbeat(1, (1,))
        hbt.heartbeat(2, (1,))
        # no records
        recs = logging.get_log_records(hbt, count=0)
        self.assertEqual(recs, [])
        # most recent record
        recs = logging.get_log_records(hbt, count=1)
        self.assertEqual(recs, [[2, 2, 1, 3, 3, 1, 1, 1, 1]])
        # partial window of records
        recs = logging.get_log_records(hbt, count=2)
        self.assertEqual(recs, [[1, 1, 1, 2, 2, 1, 1, 1, 1],
                                [2, 2, 1, 3, 3, 1, 1, 1, 1]])
        # window of records
        for count in [None, 3]:
            recs = logging.get_log_records(hbt, count=count)
            self.assertEqual(recs, [[0, 0, 1, 1, 1, 1, 1, 1, 1],
                                    [1, 1, 1, 2, 2, 1, 1, 1, 1],
                                    [2, 2, 1, 3, 3, 1, 1, 1, 1]])

    def test_get_log_records_bad_count(self):
        hbt = Heartbeat(1)
        for count in [-1, 2]:
            with self.assertRaises(ValueError):
                logging.get_log_records(hbt, count=count)


if __name__ == '__main__':
    unittest.main()
