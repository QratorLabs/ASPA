
IPv4, IPv6 = 4, 6
AS_SET, AS_SEQUENCE, AS_CONFED_SEQUENCE, AS_CONFED_SET = range(1, 5)
Valid, Invalid, Unknown = range(3)
NO_ATTESTATION, PROVIDER, NOT_PROVIDER = range(3)


class Segment:
    def __init__(self, value, type):
        self.value, self.type = value, type


class ASPA:
    def __init__(self, aspa_records):
        self.aspa_records = aspa_records

    def verify_pair(self, as1, as2):
        if as1 not in self.aspa_records:
            return NO_ATTESTATION

        if as2 not in self.aspa_records[as1]:
            return NOT_PROVIDER

        return PROVIDER

    def get_ramp_boundaries(self, aspath):
        min_ramp = 0

        as1 = 0
        index = 1
        for segment in aspath:
            if not as1:
                as1 = segment.value
            elif as1 != segment.value:
                pair_check = self.verify_pair(as1, segment.value)
                if pair_check == NOT_PROVIDER:
                    return index - 1, min_ramp - 1 if min_ramp else index - 1
                elif pair_check == NO_ATTESTATION and not min_ramp:
                    min_ramp = index

                as1 = segment.value

            index += 1

        return index - 1, min_ramp - 1 if min_ramp else index - 1

    def is_verifiable(self, aspath):
        for segment in aspath:
            if segment.type != AS_SEQUENCE:
                return False

        return True

    def check_upflow_path(self, aspath, neighbor_as, ix_client=False):
        if len(aspath) == 0:
            return Invalid

        if not self.is_verifiable(aspath):
            return Invalid

        if not ix_client and aspath[-1].value != neighbor_as:
            return Invalid

        max_up_ramp, min_up_ramp = self.get_ramp_boundaries(aspath)

        aspath_len = len(aspath)
        if max_up_ramp < aspath_len:
            return Invalid
        if min_up_ramp < aspath_len:
            return Unknown
        return Valid

    def check_downflow_path(self, aspath, neighbor_as):
        if len(aspath) == 0:
            return Invalid

        if not self.is_verifiable(aspath):
            return Invalid

        if aspath[-1].value != neighbor_as:
            return Invalid


        max_up_ramp, min_up_ramp = self.get_ramp_boundaries(aspath)
        max_down_ramp, min_down_ramp = self.get_ramp_boundaries(list(reversed(aspath)))

        aspath_len = len(aspath)
        if max_up_ramp + max_down_ramp < aspath_len:
            return Invalid
        if min_up_ramp + min_down_ramp < aspath_len:
            return Unknown
        return Valid
