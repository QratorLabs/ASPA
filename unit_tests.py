import unittest
from aspa_logic import *


# just an example for the tests
aspa_records = {
    3356: {6695},
    2914: {0},
    174: {6695},
    6695: {0},
    13238: {6762, 174, 9002, 6939, 208722, 1299, 3356},
    43247: {13238},
    12389: {1273, 1299, 3257, 3356, 3491, 5511},
    8342: {12389, 8359},
    3: {4},
    4: {3},
}

aspa_manager = ASPA(aspa_records)

class ASPATests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ASPATests, self).__init__(*args, **kwargs)

    def test_upstream_path_valid(self):
        aspath = [Segment(3356, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 3356), Valid)

        aspath = [Segment(3356, AS_SEQUENCE), Segment(3356, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 3356), Valid)

        aspath = [Segment(13238, AS_SEQUENCE), Segment(3356, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 3356), Valid)

        aspath = [Segment(13238, AS_SEQUENCE), Segment(13238, AS_SEQUENCE),
                  Segment(3356, AS_SEQUENCE), Segment(3356, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 3356), Valid)

        aspath = [Segment(43247, AS_SEQUENCE), Segment(13238, AS_SEQUENCE),
                  Segment(3356, AS_SEQUENCE), Segment(3356, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 3356), Valid)

    def test_upstream_path_invalid(self):
        # aspath with zero length
        aspath = []
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 3356), Invalid)

        # invalid neighbor
        aspath = [Segment(2914, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 3356), Invalid)

        # invalid aspa
        aspath = [Segment(3356, AS_SEQUENCE), Segment(2914, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 2914), Invalid)

        # invalid aspa + set in the beginning
        aspath = [Segment(3356, AS_SET), Segment(3356, AS_SEQUENCE), Segment(2914, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 2914), Invalid)

        # invalid aspa + set at the end
        aspath = [Segment(3356, AS_SEQUENCE), Segment(2914, AS_SEQUENCE), Segment(2914, AS_SET)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 2914), Invalid)

        # invalid aspa in the middle
        aspath = [Segment(3356, AS_SEQUENCE), Segment(12389, AS_SEQUENCE), Segment(2914, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 2914), Invalid)

        # invalid aspa in the middle + prepend
        aspath = [Segment(3356, AS_SEQUENCE), Segment(12389, AS_SEQUENCE), Segment(12389, AS_SEQUENCE), Segment(2914, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 2914), Invalid)

    def test_upstream_path_unknown(self):
        # unknown pair at the origin
        aspath = [Segment(1, AS_SEQUENCE), Segment(13238, AS_SEQUENCE), Segment(3356, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 3356), Unknown)

        # unknown pair in the middle
        aspath = [Segment(13238, AS_SEQUENCE), Segment(9002, AS_SEQUENCE), Segment(3356, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 3356), Unknown)

        # two unknown pairs
        aspath = [Segment(13238, AS_SEQUENCE), Segment(9002, AS_SEQUENCE), Segment(1, AS_SEQUENCE), Segment(3356, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 3356), Unknown)

        # two unknown pairs
        aspath = [Segment(8342, AS_SEQUENCE), Segment(8359, AS_SEQUENCE), Segment(3, AS_SEQUENCE), Segment(4, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 4), Unknown)

    def test_downstream_path_valid(self):
        # single T1 in the path
        aspath = [Segment(3356, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 3356), Valid)

        # just an ISP
        aspath = [Segment(12389, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 12389), Valid)

        # ISP + T1
        aspath = [Segment(12389, AS_SEQUENCE), Segment(3356, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 3356), Valid)

        # ISP + T1 + T1
        aspath = [Segment(12389, AS_SEQUENCE), Segment(3356, AS_SEQUENCE), Segment(2914, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 2914), Valid)

        # ISP + T1 + T1 + ISP (upflow and downflow fragments)
        aspath = [Segment(12389, AS_SEQUENCE), Segment(3356, AS_SEQUENCE),
                  Segment(174, AS_SEQUENCE), Segment(13238, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 13238), Valid)

        # ISP + T1 + T1 + ISP + prepend (upflow and downflow fragments)
        aspath = [Segment(12389, AS_SEQUENCE), Segment(3356, AS_SEQUENCE), Segment(3356, AS_SEQUENCE),
                  Segment(174, AS_SEQUENCE), Segment(13238, AS_SEQUENCE), Segment(13238, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 13238), Valid)

        # ISP c2p T1 ? ISP p2c ISP
        aspath = [Segment(12389, AS_SEQUENCE), Segment(3356, AS_SEQUENCE),
                  Segment(208722, AS_SEQUENCE), Segment(13238, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 13238), Valid)

        # ISP c2p T1 ? ISP p2c ISP + prepend
        aspath = [Segment(12389, AS_SEQUENCE), Segment(3356, AS_SEQUENCE), Segment(3356, AS_SEQUENCE),
                  Segment(208722, AS_SEQUENCE), Segment(208722, AS_SEQUENCE), Segment(13238, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 13238), Valid)

    def test_downstream_path_invalid(self):
        # invalid neighbor
        aspath = [Segment(3356, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 2914), Invalid)

        # T1, T1, T1
        aspath = [Segment(3356, AS_SEQUENCE), Segment(2914, AS_SEQUENCE), Segment(174, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 174), Invalid)

        # T1, ISP, T1
        aspath = [Segment(3356, AS_SEQUENCE), Segment(12389, AS_SEQUENCE), Segment(174, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 174), Invalid)

        # Leak of the peer
        aspath = [Segment(13238, AS_SEQUENCE), Segment(20485, AS_SEQUENCE), Segment(174, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 174), Invalid)

        # Leak of the peer
        aspath = [Segment(13238, AS_SEQUENCE), Segment(20485, AS_SEQUENCE), Segment(174, AS_SEQUENCE), Segment(3356, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 174), Invalid)

    def test_downstream_path_unknown(self):
        # Unknowns + T1
        aspath = [Segment(1, AS_SEQUENCE), Segment(2, AS_SEQUENCE), Segment(174, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 174), Unknown)

        # Unknown in the beginning
        aspath = [Segment(1, AS_SEQUENCE), Segment(12389, AS_SEQUENCE), Segment(3356, AS_SEQUENCE),
                  Segment(174, AS_SEQUENCE), Segment(13238, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 13238), Unknown)

        # Unknown in the downflow segment
        aspath = [Segment(12389, AS_SEQUENCE), Segment(3356, AS_SEQUENCE),
                  Segment(174, AS_SEQUENCE), Segment(1, AS_SEQUENCE), Segment(2, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 2), Unknown)

        # Multiple unknowns in the middle without Invalids
        aspath = [Segment(8342, AS_SEQUENCE), Segment(12389, AS_SEQUENCE),
                  Segment(1, AS_SEQUENCE), Segment(2, AS_SEQUENCE), Segment(208722, AS_SEQUENCE), Segment(13238, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 13238), Unknown)

        # Unknown in the end
        aspath = [Segment(12389, AS_SEQUENCE), Segment(3356, AS_SEQUENCE),
                  Segment(174, AS_SEQUENCE), Segment(13238, AS_SEQUENCE), Segment(1, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 1), Unknown)

    def test_downstream_path_unverifiable(self):
        # Unknown in the beginning
        aspath = [Segment(1, AS_SET), Segment(12389, AS_SEQUENCE), Segment(3356, AS_SEQUENCE),
                  Segment(174, AS_SEQUENCE), Segment(13238, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 13238), Invalid)

        # Unknown in the middle
        aspath = [Segment(12389, AS_SEQUENCE), Segment(3356, AS_SEQUENCE),
                  Segment(174, AS_SEQUENCE), Segment(1, AS_SET), Segment(13238, Invalid)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 1), Invalid)

        # Unknown in the end
        aspath = [Segment(12389, AS_SEQUENCE), Segment(3356, AS_SEQUENCE),
                  Segment(174, AS_SEQUENCE), Segment(13238, AS_SEQUENCE), Segment(1, AS_SET)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 1), Invalid)

        # Leak of the peer
        aspath = [Segment(13238, AS_SEQUENCE), Segment(20485, AS_SET), Segment(174, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 174), Invalid)

    def test_ix_path_valid(self):
        # single T1 in the path through IX without 6695 in the path
        aspath = [Segment(3356, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 6695, ix_client=True), Valid)

        # ISP in the path through IX without 6695 in the path
        aspath = [Segment(1, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 6695, ix_client=True), Valid)

        # single T1 in the path with 6695 in the path
        aspath = [Segment(3356, AS_SEQUENCE), Segment(6695, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 6695, ix_client=True), Valid)

        # ISP in the path through IX without 6695 in the path
        aspath = [Segment(1, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 6695, ix_client=True), Valid)

        # non trasparent IX with ASPA record
        aspath = [Segment(12389, AS_SEQUENCE), Segment(3356, AS_SEQUENCE), Segment(6695, AS_SEQUENCE),
                  Segment(174, AS_SEQUENCE), Segment(13238, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_downflow_path(aspath, 13238), Valid)

    def test_ix_path_invalid(self):
        # T1, T1, IX without 6695 in the path
        aspath = [Segment(2914, AS_SEQUENCE), Segment(3356, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 6695, ix_client=True), Invalid)

        # T1, T1, IX with 6695 in the path
        aspath = [Segment(2914, AS_SEQUENCE), Segment(3356, AS_SEQUENCE), Segment(6695, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 6695, ix_client=True), Invalid)

        # single T1 in the path through IX with 4635 in the path, though ASPA for 4635 doesn't exist
        aspath = [Segment(3356, AS_SEQUENCE), Segment(4635, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 4635, ix_client=True), Invalid)

        # T1 + AS1 in the path through IX with 4635 in the path, though ASPA for 4635 doesn't exist
        aspath = [Segment(3356, AS_SEQUENCE), Segment(1, AS_SEQUENCE), Segment(4635, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 4635, ix_client=True), Invalid)

    def test_ix_path_unknown(self):
        # ISP unkown ISP in the path through IX without 6695 in the path
        aspath = [Segment(1, AS_SEQUENCE), Segment(2, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 6695, ix_client=True), Unknown)

        # ISP unknown ISP in the path through IX with 6695 in the path
        aspath = [Segment(1, AS_SEQUENCE), Segment(2, AS_SEQUENCE), Segment(6695, AS_SEQUENCE)]
        with self.subTest():
            self.assertEqual(aspa_manager.check_upflow_path(aspath, 6695, ix_client=True), Unknown)

if __name__ == '__main__':
    # aspa_manager = ASPA(aspa_records)
    # aspath = [Segment(3356, AS_SEQUENCE), Segment(1, AS_SEQUENCE), Segment(4635, AS_SEQUENCE)]
    # print(aspa_manager.check_ix_path(aspath, 4635) == Invalid)

    unittest.main()