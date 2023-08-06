# pylint: disable=W0212, C0116, R0904
"""Test heartbeats.py"""
import unittest
from apphb import Heartbeat, HeartbeatFieldRecord, HeartbeatRecord

# Data classes have some strange behaviors when it comes to default values, so we test those, too.

class TestHeartbeatFieldRecord(unittest.TestCase):
    """Test class HeartbeatFieldRecord"""

    def test_default(self):
        hfr = HeartbeatFieldRecord()
        self.assertEqual(hfr.val, (0,))
        self.assertEqual(hfr.glbl, 0)
        self.assertEqual(hfr.wndw, 0)
        self.assertEqual(hfr.inst, 0)
        self.assertEqual(hfr.glbl_rate, 0)
        self.assertEqual(hfr.wndw_rate, 0)
        self.assertEqual(hfr.inst_rate, 0)

    def test_two_instances(self):
        hfr1 = HeartbeatFieldRecord()
        hfr2 = HeartbeatFieldRecord()
        self.assertEqual(hfr1, hfr2)
        hfr2.val = (1,)
        self.assertNotEqual(hfr1, hfr2)

    def test_list(self):
        hfrs = [HeartbeatFieldRecord() for _ in range(2)]
        self.assertEqual(len(hfrs), 2)
        self.assertEqual(hfrs[0], hfrs[1])
        hfrs[1].val = (1,)
        self.assertNotEqual(hfrs[0], hfrs[1])

    def test_duplicates(self):
        hfrs = [HeartbeatFieldRecord()] * 2
        self.assertEqual(len(hfrs), 2)
        self.assertEqual(hfrs[0], hfrs[1])
        hfrs[1].val = (1,)
        self.assertEqual(hfrs[0], hfrs[1])

    def test_copy(self):
        hfr = HeartbeatFieldRecord(val=(10, 20), glbl=100, wndw=50, inst=10,
                                   glbl_rate=10, wndw_rate=5, inst_rate=1)
        hfr_norm = hfr.copy(norm=10, rate_norm=0.1)
        self.assertEqual(hfr_norm.val, (100, 200))
        self.assertEqual(hfr_norm.glbl, 1000)
        self.assertEqual(hfr_norm.wndw, 500)
        self.assertEqual(hfr_norm.inst, 100)
        self.assertAlmostEqual(hfr_norm.glbl_rate, 1)
        self.assertAlmostEqual(hfr_norm.wndw_rate, 0.5)
        self.assertAlmostEqual(hfr_norm.inst_rate, 0.1)


class TestHeartbeatRecord(unittest.TestCase):
    """Test class HeartbeatRecord"""

    def test_default(self):
        hbr = HeartbeatRecord()
        self.assertEqual(hbr.ident, 0)
        self.assertEqual(hbr.tag, 0)
        self.assertEqual(hbr.time, HeartbeatFieldRecord())
        self.assertEqual(hbr.field_records, [])

    def test_two_instances(self):
        hbr1 = HeartbeatRecord()
        hbr2 = HeartbeatRecord()
        self.assertEqual(hbr1.ident, hbr2.ident)
        self.assertEqual(hbr1.tag, hbr2.tag)
        self.assertEqual(hbr1.time, hbr2.time)
        self.assertEqual(hbr1.field_records, hbr2.field_records)
        self.assertEqual(hbr1, hbr2)
        # test changing primitive
        hbr2.ident = 1
        self.assertNotEqual(hbr1.ident, hbr2.ident)
        self.assertNotEqual(hbr1, hbr2)
        # reset, test changing time
        hbr2 = HeartbeatRecord()
        self.assertEqual(hbr1, hbr2)
        hbr2.time.val = (1,)
        self.assertNotEqual(hbr1.time, hbr2.time)
        self.assertNotEqual(hbr1, hbr2)
        # reset, test changing field_records
        hbr2 = HeartbeatRecord()
        self.assertEqual(hbr1, hbr2)
        hbr2.field_records.append(HeartbeatRecord())
        self.assertNotEqual(hbr1.field_records, hbr2.field_records)
        self.assertNotEqual(hbr1, hbr2)


class TestHeartbeat(unittest.TestCase):
    """Test class Heartbeat"""

    def test_default(self):
        hbt = Heartbeat(1)
        self.assertEqual(hbt.count, 0)
        self.assertEqual(hbt.window_size, 1)
        self.assertEqual(len(hbt._window_buffer), 1)
        self.assertEqual(len(hbt._window_buffer[0].field_records), 0)

    def test_fields(self):
        hbt = Heartbeat(1, fields_shape=(1,))
        self.assertEqual(len(hbt._window_buffer[0].field_records), 1)

    def test_fields_illegal(self):
        for shape in [(0,), (-1,), (3,), (1, 3)]:
            with self.assertRaises(ValueError):
                Heartbeat(1, fields_shape=shape)

    def test_window_size_zero(self):
        with self.assertRaises(ValueError):
            Heartbeat(0)

    def test_window_size_not_int(self):
        with self.assertRaises(TypeError):
            Heartbeat(1.1)

    def _assert_first_record(self, hbt, time):
        elapsed = time[0] if len(time) == 1 else time[1] - time[0]
        self.assertEqual(hbt._window_buffer[0].ident, 0)
        self.assertEqual(hbt._window_buffer[0].tag, 0)
        self.assertEqual(hbt._window_buffer[0].time.val, time)
        self.assertEqual(hbt._window_buffer[0].time.glbl, elapsed)
        self.assertEqual(hbt._window_buffer[0].time.wndw, elapsed)
        self.assertEqual(hbt._window_buffer[0].time.inst, elapsed)
        self.assertEqual(hbt._window_buffer[0].time.glbl_rate, 1 / elapsed)
        self.assertEqual(hbt._window_buffer[0].time.wndw_rate, 1 / elapsed)
        self.assertEqual(hbt._window_buffer[0].time.inst_rate, 1 / elapsed)

    def test_heartbeat_default(self):
        for time in [(1,), [1]]:
            hbt = Heartbeat(1)
            hbt.heartbeat(0, time)
            self._assert_first_record(hbt, time)
            self.assertEqual(hbt.count, 1)

    def test_heartbeat_time_pair(self):
        for time in [(1, 2), [1, 2]]:
            hbt = Heartbeat(1, time_shape=2)
            hbt.heartbeat(0, time)
            self.assertEqual(hbt._window_buffer[0].time.val, time)
            self.assertEqual(hbt._window_buffer[0].time.glbl, 1)
            self.assertEqual(hbt._window_buffer[0].time.wndw, 1)
            self.assertEqual(hbt._window_buffer[0].time.inst, 1)
            self.assertEqual(hbt._window_buffer[0].time.glbl_rate, 1)
            self.assertEqual(hbt._window_buffer[0].time.wndw_rate, 1)
            self.assertEqual(hbt._window_buffer[0].time.inst_rate, 1)
            self.assertEqual(hbt.count, 1)

    def test_heartbeat_time_empty(self):
        for time in [(), []]:
            hbt = Heartbeat(1)
            with self.assertRaises(ValueError):
                hbt.heartbeat(0, time)

    def test_heartbeat_time_three(self):
        for time in [(0, 1, 2), [0, 1, 2]]:
            hbt = Heartbeat(1)
            with self.assertRaises(ValueError):
                hbt.heartbeat(0, time)

    def test_window_global(self):
        hbt = Heartbeat(3)
        tag = 0
        time = (1,)
        hbt.heartbeat(tag, time)
        self._assert_first_record(hbt, time)
        tag += 1
        time = (3,)
        hbt.heartbeat(tag, time)
        self.assertEqual(hbt._window_buffer[1].time.val, time)
        self.assertEqual(hbt._window_buffer[1].time.glbl, 4)
        self.assertEqual(hbt._window_buffer[1].time.wndw, 4)
        self.assertEqual(hbt._window_buffer[1].time.inst, 3)
        self.assertEqual(hbt._window_buffer[1].time.glbl_rate, 2/4)
        self.assertEqual(hbt._window_buffer[1].time.wndw_rate, 2/4)
        self.assertAlmostEqual(hbt._window_buffer[1].time.inst_rate, 1/3)
        tag += 1
        time = (4,)
        hbt.heartbeat(tag, time)
        self.assertEqual(hbt._window_buffer[2].time.val, time)
        self.assertEqual(hbt._window_buffer[2].time.glbl, 8)
        self.assertEqual(hbt._window_buffer[2].time.wndw, 8)
        self.assertEqual(hbt._window_buffer[2].time.inst, 4)
        self.assertAlmostEqual(hbt._window_buffer[2].time.glbl_rate, 3/8)
        self.assertAlmostEqual(hbt._window_buffer[2].time.wndw_rate, 3/8)
        self.assertAlmostEqual(hbt._window_buffer[2].time.inst_rate, 1/4)
        # window complete - window values start rolling over, global values continue increasing
        tag += 1
        time = (8,)
        hbt.heartbeat(tag, time)
        self.assertEqual(hbt._window_buffer[0].time.val, time)
        self.assertEqual(hbt._window_buffer[0].time.glbl, 16)
        self.assertEqual(hbt._window_buffer[0].time.wndw, 15)
        self.assertEqual(hbt._window_buffer[0].time.inst, 8)
        self.assertAlmostEqual(hbt._window_buffer[0].time.glbl_rate, 4/16)
        self.assertAlmostEqual(hbt._window_buffer[0].time.wndw_rate, 3/15)
        self.assertAlmostEqual(hbt._window_buffer[0].time.inst_rate, 1/8)

    def _assert_first_record_field(self, hbt, fld, val):
        if len(val) == 2:
            diff = val[1] - val[0]
        else:
            diff = val[0]
        self.assertEqual(hbt._window_buffer[0].field_records[fld].val, val)
        self.assertEqual(hbt._window_buffer[0].field_records[fld].glbl, diff)
        self.assertEqual(hbt._window_buffer[0].field_records[fld].wndw, diff)
        self.assertEqual(hbt._window_buffer[0].field_records[fld].inst, diff)
        self.assertAlmostEqual(hbt._window_buffer[0].field_records[fld].glbl_rate, diff)
        self.assertAlmostEqual(hbt._window_buffer[0].field_records[fld].wndw_rate, diff)
        self.assertAlmostEqual(hbt._window_buffer[0].field_records[fld].inst_rate, diff)

    def test_fields_one(self):
        hbt = Heartbeat(1, fields_shape=(1,))
        hbt.heartbeat(0, (1,), fields=((2,),))
        self._assert_first_record_field(hbt, 0, (2,))

    def test_fields_one_pair(self):
        hbt = Heartbeat(1, fields_shape=(2,))
        hbt.heartbeat(0, (1,), fields=((2, 3),))
        self._assert_first_record_field(hbt, 0, (2, 3))

    def test_fields_two(self):
        hbt = Heartbeat(1, fields_shape=(1, 2))
        hbt.heartbeat(0, (1,), fields=((2,), (4, 6)))
        self._assert_first_record_field(hbt, 0, (2,))
        self._assert_first_record_field(hbt, 1, (4, 6))

    def test_get_record(self):
        hbt = Heartbeat(1)
        hbt.heartbeat(0, (1,))
        rec = hbt.get_record()
        self.assertEqual(rec.time.glbl, 1)
        self.assertEqual(rec.time.wndw, 1)
        self.assertEqual(rec.time.inst, 1)
        self.assertEqual(rec.time.glbl_rate, 1)
        self.assertEqual(rec.time.wndw_rate, 1)
        self.assertEqual(rec.time.inst_rate, 1)

    def test_get_record_offset(self):
        hbt = Heartbeat(2)
        hbt.heartbeat(0, (1,))
        rec = hbt.get_record(off=-1)
        self.assertEqual(rec.time.glbl, 0)
        self.assertEqual(rec.time.wndw, 0)
        self.assertEqual(rec.time.inst, 0)
        self.assertEqual(rec.time.glbl_rate, 0)
        self.assertEqual(rec.time.wndw_rate, 0)
        self.assertEqual(rec.time.inst_rate, 0)

    def test_get_record_offset_illegal(self):
        hbt = Heartbeat(1)
        hbt.heartbeat(0, (1,))
        for off in [1, -2]:
            with self.assertRaises(ValueError):
                hbt.get_record(off=off)

    def test_getters(self):
        hbt = Heartbeat(2, fields_shape=(2,))
        hbt.heartbeat(0, (1,), fields=((2, 4),))
        hbt.heartbeat(0, (2,), fields=((4, 8),))
        hbt.heartbeat(0, (4,), fields=((8, 16),))
        # time
        self.assertEqual(hbt.get_value(), (4,))
        self.assertEqual(hbt.get_global_count(), 7)
        self.assertEqual(hbt.get_window_count(), 6)
        self.assertEqual(hbt.get_instant_count(), 4)
        self.assertAlmostEqual(hbt.get_global_rate(), 3/7)
        self.assertAlmostEqual(hbt.get_window_rate(), 2/6)
        self.assertAlmostEqual(hbt.get_instant_rate(), 1/4)
        # custom field
        self.assertEqual(hbt.get_value(fld=0), (8, 16))
        self.assertEqual(hbt.get_global_count(fld=0), 14)
        self.assertEqual(hbt.get_window_count(fld=0), 12)
        self.assertEqual(hbt.get_instant_count(fld=0), 8)
        self.assertAlmostEqual(hbt.get_global_rate(fld=0), 14/7)
        self.assertAlmostEqual(hbt.get_window_rate(fld=0), 12/6)
        self.assertAlmostEqual(hbt.get_instant_rate(fld=0), 8/4)
        # time with offset
        self.assertEqual(hbt.get_value(off=-1), (2,))
        self.assertEqual(hbt.get_global_count(off=-1), 3)
        self.assertEqual(hbt.get_window_count(off=-1), 3)
        self.assertEqual(hbt.get_instant_count(off=-1), 2)
        self.assertAlmostEqual(hbt.get_global_rate(off=-1), 2/3)
        self.assertAlmostEqual(hbt.get_window_rate(off=-1), 2/3)
        self.assertAlmostEqual(hbt.get_instant_rate(off=-1), 1/2)
        # custom field with offset
        self.assertEqual(hbt.get_value(off=-1, fld=0), (4, 8))
        self.assertEqual(hbt.get_global_count(off=-1, fld=0), 6)
        self.assertEqual(hbt.get_window_count(off=-1, fld=0), 6)
        self.assertEqual(hbt.get_instant_count(off=-1, fld=0), 4)
        self.assertAlmostEqual(hbt.get_global_rate(off=-1, fld=0), 6/3)
        self.assertAlmostEqual(hbt.get_window_rate(off=-1, fld=0), 6/3)
        self.assertAlmostEqual(hbt.get_instant_rate(off=-1, fld=0), 4/2)

    def test_getters_offset_illegal(self):
        hbt = Heartbeat(1)
        hbt.heartbeat(0, (1,))
        for off in [1, -2]:
            with self.assertRaises(ValueError):
                hbt.get_value(off=off)
            with self.assertRaises(ValueError):
                hbt.get_global_count(off=off)
            with self.assertRaises(ValueError):
                hbt.get_window_count(off=off)
            with self.assertRaises(ValueError):
                hbt.get_instant_count(off=off)
            with self.assertRaises(ValueError):
                hbt.get_global_rate(off=off)
            with self.assertRaises(ValueError):
                hbt.get_window_rate(off=off)
            with self.assertRaises(ValueError):
                hbt.get_instant_rate(off=off)

    def test_getters_field_illegal(self):
        hbt = Heartbeat(1, fields_shape=(2,))
        hbt.heartbeat(0, (1,), fields=((2, 4),))
        for fld in [1, -2]:
            with self.assertRaises(IndexError):
                hbt.get_value(fld=fld)
            with self.assertRaises(IndexError):
                hbt.get_global_count(fld=fld)
            with self.assertRaises(IndexError):
                hbt.get_window_count(fld=fld)
            with self.assertRaises(IndexError):
                hbt.get_instant_count(fld=fld)
            with self.assertRaises(IndexError):
                hbt.get_global_rate(fld=fld)
            with self.assertRaises(IndexError):
                hbt.get_window_rate(fld=fld)
            with self.assertRaises(IndexError):
                hbt.get_instant_rate(fld=fld)


if __name__ == '__main__':
    unittest.main()
