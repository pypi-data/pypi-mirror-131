from wiliot.gateway_api.gateway import *
from collections import Counter


class StatType(Enum):
    N_FILTERED_PACKETS = 'n_filtered_packets'
    GW_PACKET_TIME = 'gw_packet_time'


def estimate_diff_packet_time(packets=None, packets_time=None, gw_time=None):
    if not isinstance(packets_time, list):
        print('please add a list of packet_time')
        return None
    if gw_time is None and packets is None:
        print('please add gw_time or a packets (list)')
        return None

    if gw_time is None:
        if not isinstance(packets, list):
            print('please add a list of packets')
            return None
        # fix packets if needed:
        for i, p in enumerate(packets):
            if "process_packet" not in p:
                packets[i] = 'process_packet("{}")'.format(p)
        gw_obj = WiliotGateway()
        raw_data = [{'raw': p, 'time': t} for p, t in zip(packets, packets_time)]
        processed = gw_obj.run_process_packet(raw_data=raw_data)
        gw_time = [p['stat_param'] for p in processed]
    else:
        if not isinstance(gw_time, list):
            print('please add a list of gw_time')
            return None

    # estimated the packet time according to gw time (2 bytes of ms)
    diff_pc_time = [(y - x) * 1000 for x, y in zip(packets_time[:-1], packets_time[1:])]
    diff_gw_time = [y - x for x, y in zip(gw_time[:-1], gw_time[1:])]
    gw_time_cycle = 2 ** 16  # two bytes
    estimated_diff_time = [None]  # the diff for the first element cannot be calculated
    for dt_pc, dt_gw in zip(diff_pc_time, diff_gw_time):
        if dt_pc > gw_time_cycle:
            estimated_diff_time.append(round(dt_pc))
        else:
            if dt_gw < 0:
                estimated_diff_time.append(dt_gw + gw_time_cycle)
            else:
                estimated_diff_time.append(dt_gw)
    return estimated_diff_time


def process_encrypted_packet(packets=None, packets_time=None, stat_type=StatType.N_FILTERED_PACKETS):
    if packets is None or packets_time is None:
        return None

    gw_obj = WiliotGateway()
    raw_data = [{'raw': p, 'time': t} for p, t in zip(packets, packets_time)]
    processed = gw_obj.run_process_packet(raw_data=raw_data)
    if not processed:
        print('process packets was failed')
        return None

    # add packet rate:
    # convert list of dict to dict of list:
    processed_dict = {}
    if isinstance(processed, list):
        proc_keys = list(processed[0].keys())
        for k in list(processed[0].keys()):
            processed_dict[k] = [p[k] for p in processed]
    elif isinstance(processed, dict):
        processed_dict = processed
    else:
        print('unknown process output type: {}'.format(type(processed)))
        return None

    # handle the stat parameter:
    if stat_type == StatType.N_FILTERED_PACKETS:
        processed_dict['n_filtered_packets'] = processed_dict['stat_param']
        del processed_dict['stat_param']
    elif stat_type == StatType.GW_PACKET_TIME:
        processed_dict['gw_packet_time'] = processed_dict['stat_param']
        del processed_dict['stat_param']
        # calculate the time differences between all packets:
        processed_dict['estimate_diff_time'] = estimate_diff_packet_time(packets_time=processed_dict['time_from_start'],
                                                                         gw_time=processed_dict['gw_packet_time'])
    else:
        print('unsupported stat type')

    # calculate the time between two successive packets:
    unique_packets = Counter(processed_dict['packet'])
    processed_dict['packet_rate'] = [float('nan')] * len(processed_dict['packet'])
    for packet, n_packets in unique_packets.items():
        if n_packets >= 4:
            inds = [i for i, p in enumerate(processed_dict['packet']) if p == packet]
            if stat_type == StatType.GW_PACKET_TIME:
                packet_diff_time = [processed_dict['estimate_diff_time'][i] for i in inds]
                packet_diff_time_no_none = [p for p in packet_diff_time if p is not None]
                packet_rate = min(packet_diff_time_no_none)
            else:
                packet_time = [processed_dict['time_from_start'][i] for i in inds]
                packet_rate = min([y - x for x, y in zip(packet_time[:-1], packet_time[1:])])
            processed_dict['packet_rate'][inds[-1]] = packet_rate

    return processed_dict


if __name__ == '__main__':
    pass
