
class SirenSprinkler(object):

    MODE_WAIT_FOR_SPRINKLE = 0
    MODE_STARTING = 1
    MODE_SPRINKLING = 2
    MODE_STOPPING = 3

    MODE_MANUAL_REQUEST = 4


    def __init__(self, app_context, name, schedule, control):
        self.app_context = app_context
        self.name = name
        self.schedule = schedule
        self.control = control
        #
        self.mode = SirenSprinkler.MODE_WAIT_FOR_SPRINKLE
        self._last_time_started_sprinkle = app_context.time()
        #self._
        #
        self.sprinkle_time_str = '?'
        self.cmd_sprinkle = 0
        self.fb_sprinkle = 0


    def is_sprinkling(self):
        return self.mode == SirenSprinkler.MODE_SPRINKLING

    '''
    def cycle_manual(self, clear_to_sprinkle):
        if self.mode == SirenSprinkler.MODE_STARTING and clear_to_sprinkle:
            self._last_time_started_sprinkle = self.app_context.time()
            self.mode = SirenSprinkler.MODE_SPRINKLING
            return

        if self.mode == SirenSprinkler.MODE_SPRINKLING:
            #if #self._last_time_started_sprinkle >
            sprinkle_ends = (self._last_time_started_sprinkle + self.schedule.duration)

            dt = sprinkle_ends - self.app_context.time()
            if dt > 60.0*60.0:
                self.sprinkle_time_str = "Sprinkling for {0:.3f} hrs".format(dt/60.0/60.0)
            elif dt > 60.0:
                self.sprinkle_time_str = "Sprinkling for {0:.2f} min".format(dt/60.0)
            else:
                self.sprinkle_time_str = "Sprinkling for {0:.1f} sec".format(dt)

            if self.app_context.time() > sprinkle_ends:
                self.mode = SirenSprinkler.MODE_STOPPING
                return

        if self.mode == SirenSprinkler.MODE_STOPPING:
            self.mode = SirenSprinkler.MODE_WAIT_FOR_SPRINKLE
            return
    '''

    def cycle(self, clear_to_sprinkle):
        #if not clear_to_sprinkle:
        #    self.mode = SirenSprinkler.MODE_WAIT_FOR_SPRINKLE
        is_auto = self.app_context.application.mode == self.app_context.application.MODE_AUTO
        if self.mode == SirenSprinkler.MODE_WAIT_FOR_SPRINKLE and is_auto:

            next_sprinkle_time = self.schedule.get_next_sprinkle_time(self._last_time_started_sprinkle)
            if next_sprinkle_time is None:
                # yeah never we will exit from wait state
                self.sprinkle_time_str = 'Never'
                return

            dt = next_sprinkle_time - self.app_context.time()
            if dt > 60.0*60.0:
                self.sprinkle_time_str = "{0:.3f} hrs".format(dt/60.0/60.0)
            elif dt > 60.0:
                self.sprinkle_time_str = "{0:.2f} min".format(dt/60.0)
            else:
                self.sprinkle_time_str = "{0:.1f} sec".format(dt)

            if next_sprinkle_time <= self.app_context.time():
                self.mode = SirenSprinkler.MODE_STARTING
                # yeah lets start sprinkle on next cycle
                return

        if self.mode == SirenSprinkler.MODE_STARTING and clear_to_sprinkle:
            self._last_time_started_sprinkle = self.app_context.time()
            self.mode = SirenSprinkler.MODE_SPRINKLING
            return

        if self.mode == SirenSprinkler.MODE_MANUAL_REQUEST and clear_to_sprinkle:
            self._last_time_started_sprinkle = self.app_context.time()
            self.mode = SirenSprinkler.MODE_SPRINKLING
            return

        if self.mode == SirenSprinkler.MODE_SPRINKLING:
            #if #self._last_time_started_sprinkle >
            sprinkle_ends = (self._last_time_started_sprinkle + self.schedule.duration)

            dt = sprinkle_ends - self.app_context.time()
            if dt > 60.0*60.0:
                self.sprinkle_time_str = "Sprinkling for {0:.3f} hrs".format(dt/60.0/60.0)
            elif dt > 60.0:
                self.sprinkle_time_str = "Sprinkling for {0:.2f} min".format(dt/60.0)
            else:
                self.sprinkle_time_str = "Sprinkling for {0:.1f} sec".format(dt)

            if self.app_context.time() > sprinkle_ends:
                self.mode = SirenSprinkler.MODE_STOPPING
                return

        if self.mode == SirenSprinkler.MODE_STOPPING:
            self.mode = SirenSprinkler.MODE_WAIT_FOR_SPRINKLE
            return

    def state_str(self):
        return {
                SirenSprinkler.MODE_WAIT_FOR_SPRINKLE: 'waiting',
                SirenSprinkler.MODE_STARTING: 'starting',
                SirenSprinkler.MODE_SPRINKLING: 'sprinkling',
                SirenSprinkler.MODE_STOPPING: 'stopping',
                SirenSprinkler.MODE_MANUAL_REQUEST: 'Manual Request',
        }[self.mode]

        #if schedule.
        #if MODE_STARTING:
        #    if
