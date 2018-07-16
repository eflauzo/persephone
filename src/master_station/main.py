import threading
import time
import argparse
import yaml
import can
from canstruct import pycanstruct
import urwid

from siren_station import SirenStation
from siren_sprinkler import SirenSprinkler
from schedule import Schedule
from app_context import AppContext

MY_ADDR = 0

class SprinklerWalker(urwid.ListWalker):
    def __init__(self, context):
        self.context = context
        self.pos = 0

    def build(self, ix):


        # No, Name, Name , State, Time Until Sprinkle
        items = self.context.application.list_sprinklers()
        if ix >= len(items):
            return None

        time_now = self.context.time()

        station_obj, sprinkler_obj = items[ix]
        wgt_id = urwid.Button('{}'.format(ix))
        wgt_name_station = urwid.Text('{}'.format(station_obj.name))
        wgt_name_sprinkler = urwid.Text('{}'.format(sprinkler_obj.name))
        wgt_state = urwid.Text('{}'.format(sprinkler_obj.state_str()))
        time_text = "???"
        if self.context.application.mode == Persephone.MODE_INHIBIT:
            time_text = 'inhibited'
        #elif self.context.application.mode == Persephone.MODE_MANUAL:
        #    time_text = 'manual'
        else:
            time_text = sprinkler_obj.sprinkle_time_str


        wgt_sprinkle_time = urwid.Text('{}'.format(time_text))

        return urwid.AttrMap(
            urwid.Columns([wgt_id, wgt_name_station, wgt_name_sprinkler, wgt_state, wgt_sprinkle_time] ),  'inactive_item', 'active_item'
        )

    def get_next(self, position):
        if position+1 >= len(self.context.application.list_sprinklers()):
            return None, None
        new_pos = position+1
        return self.build(new_pos), new_pos

    def get_prev(self, position):
        if position == 0:
            return None, None
        new_pos = position-1
        return self.build(new_pos), new_pos

    def set_focus(self, position):
        self.pos = position
        #pass

    def get_focus(self):
        return self.build(self.pos), self.pos

class Persephone(object):

    MODE_INHIBIT=0
    MODE_MANUAL=1
    MODE_AUTO=2

    def __init__(self, app_context):
        self.stations = []
        self.mode = Persephone.MODE_AUTO
        self.app_context=app_context
        self.app_context.application = self
        self.thread = None

    def list_sprinklers(self):
        result = []
        for station in self.stations:
            for sprinkler in station.sprinklers:
                #combined_name = '{}.{}'.format(station.name, sprinkler.name)
                record = (station, sprinkler)
                result.append(record)
        return result

    def start(self):
        self.thread = threading.Thread(target=self.loop)
        self.thread.daemon = True
        self.thread.start()

    def loop(self):
        while 1:
            time.sleep(1.0)
            self.cycle()
            self.write_out()


    def load_schedule(self, node):
        days = {
            'Monday': Schedule.MON,
            'Tuesday': Schedule.TUE,
            'Wednesday': Schedule.WED,
            'Thursday': Schedule.THU,
            'Friday': Schedule.FRI,
            'Saturday': Schedule.SAT,
            'Sunday': Schedule.SUN,
        }
        days_list = []
        for day in node['days']:
            days_list.append(days[day])
        schedule = Schedule(
            self.app_context,
            days=days_list,
            hour=node['time']['hour'],
            minute=node['time']['minute'],
            duration=node['time']['duration'],
            enabled=node['enabled']
        )
        return schedule

    def load(self):
        for station, station_def in self.app_context.config['stations'].iteritems():
            assert station_def['type'] == 'Siren'

            station_obj = SirenStation(self.app_context, station_def['name'],  station_def['addr'])
            self.stations.append(station_obj)

            print station_def['sprinklers']
            for sprinkler in station_def['sprinklers']:
                sprinkler_def = sprinkler['sprinkler']
                sprinkler_obj = SirenSprinkler(
                    self.app_context,
                    sprinkler_def['name'],
                    self.load_schedule(sprinkler_def['schedule']),
                    sprinkler_def['control']
                    )
                station_obj.sprinklers.append(sprinkler_obj)

    def command_all_off(self):
        for station in self.stations:
            for sprinkler in station.sprinklers:
                sprinkler.cmd_sprinkle = 0

    def write_out(self):
        for station in self.stations:
            #pycanstruct.
            '''
            encode_arbid(self, arbid_dict):
                result = 0x0
                for field_name, field_def in self.config['arb_id']['components'].iteritems():
                    mask = bit_mask(field_def['bit_count'])
                    result |= int(arbid_dict[field_name]) & mask << start_bit
            '''

            msg = {
                'Sprinkler1': 2,
                'Sprinkler2': 2,
                'Sprinkler3': 2,
                'Sprinkler4': 2,
            }



            for sprinkler in station.sprinklers:
                msg['Sprinkler{}'.format(sprinkler.control)] = sprinkler.cmd_sprinkle

            data = self.app_context.canstruct.encode_message('SprinkleCommand', msg)

            arbid = self.app_context.canstruct.encode_arbid({
                    'source_address': MY_ADDR,
                    'destination': station.addr,
                    'function_code':  0x10, # SprinkleCommand
                    'priority':  0x7,
                    'reserved':  0x0,
                    'data_page':  0x0,
                }
            )


            canmsg = can.Message(arbitration_id=arbid, data=data, extended_id=True)
            #print "sending ", msg, "   ", canmsg
            self.app_context.bus.send(canmsg)

            #for sprinkler in station.sprinklers:

    def count_sprinkling(self):
        time.sleep(1.0)
        how_many_sprinkle = 0
        for station in self.stations:
            for sprinkler in station.sprinklers:
                how_many_sprinkle += sprinkler.fb_sprinkle
        return how_many_sprinkle

    def safe(self):
        for station in self.stations:
            for sprinkler in station.sprinklers:
                sprinkler.cmd_sprinkle = 0

    def do_inhibit_cycle(self):
        self.safe()

    def do_auto_cycle(self):
        sprinkling_count = self.count_sprinkling()
        self.safe()
        for station in self.stations:
            for sprinkler in station.sprinklers:
                sprinkler.cycle(sprinkling_count==0)
                if sprinkler.mode == SirenSprinkler.MODE_SPRINKLING:
                     sprinkling_count+=1
                     sprinkler.cmd_sprinkle = 1



    def cycle(self):
        if self.mode == Persephone.MODE_INHIBIT:
            self.do_inhibit_cycle()
            return
        if (self.mode == Persephone.MODE_AUTO) or (self.mode == Persephone.MODE_MANUAL):
            #sprinkling_count = count_sprinkling()
            #if sprinkling_count>0:
            self.do_auto_cycle()
            return

    #def ihbit_cycle():
    #    for


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Persephone CAN Bus sprinkler System')
    parser.add_argument('config', help='config filename')
    parser.add_argument('canstruct', help='canstruct config filename')
    parser.add_argument('interface', help='SocketCAN interface')
    args = parser.parse_args()

    context = AppContext()
    context.config = yaml.load(open(args.config, 'r'))
    context.can_interface = args.interface
    context.bus = can.interface.Bus(channel=args.interface , bustype='socketcan_ctypes')

    canstruct_cfg = yaml.load(open(args.canstruct, 'r'))
    context.canstruct = pycanstruct.CANStruct(canstruct_cfg[canstruct_cfg.keys()[0]]);

    p=Persephone(context)
    p.load()
    p.start()


palette = [
    ('banner', 'white', 'dark cyan'),
    ('active_item', 'white', 'dark blue'),
    ('inactive_item', 'white', 'black'),
    ('err_active_item', 'light red', 'dark blue'),
    ('err_inactive_item', 'light red', 'black'),
    ('bg', 'dark blue', 'black'),
    ('foot','dark cyan', 'dark blue', 'bold'),
]


walker = SprinklerWalker(context)
header = urwid.AttrMap(urwid.Columns([urwid.Text('#'),urwid.Text('Station'),urwid.Text('Sprinkler'), urwid.Text('State'), urwid.Text('Time Until Sprinkle')] ), 'banner')
listbox = urwid.ListBox(walker)
mode_wgt = urwid.Text('Mode: Auto')

footer = urwid.AttrMap(urwid.Columns([mode_wgt]), 'foot')

main_window = urwid.Frame(listbox, header=header, footer=footer)


def keys(key):
    if key=='tab':
        new_mode = p.mode + 1
        if new_mode > Persephone.MODE_AUTO:
            new_mode = 0
        p.mode = new_mode

    if key=='m':
        station, sprinkler = p.list_sprinklers()[walker.pos]
        if p.mode == Persephone.MODE_MANUAL:
            sprinkler.mode = SirenSprinkler.MODE_MANUAL_REQUEST



main_loop = urwid.MainLoop(main_window, palette,unhandled_input=keys)



def update():
    while 1:
        time.sleep(0.5)
        mode = 'MODE: ???'
        if p.mode == Persephone.MODE_AUTO:
            mode = 'MODE: AUTO'
        elif p.mode == Persephone.MODE_INHIBIT:
            mode = 'MODE: INHIBIT'
        elif p.mode == Persephone.MODE_MANUAL:
            mode = 'MODE: MANUAL'

        mode_wgt.set_text(mode)
        walker._modified()
        listbox._invalidate()
        main_loop.draw_screen()

updater = threading.Thread(target=update)
updater.daemon=True
updater.start()

main_loop.run()

#footer = urwid.Columns([urwid.Text('Search'), urwid.Text('Send Mesage')])
