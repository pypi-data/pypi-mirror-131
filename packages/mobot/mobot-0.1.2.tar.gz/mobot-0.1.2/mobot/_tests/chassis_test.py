# MIT License
#
# Copyright (c) 2021 Mobotx
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import select
import termios
import tty
import threading

from mobot.brain.agent import Agent
from mobot.utils.rate import Rate

CTRL_PLUS_C = '\x03'


def get_key(key_timeout):
    """Returns charecter pressed"""
    settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


class ChassisTestAgent(Agent):

    def __init__(self):
        super().__init__()
        self.chassis.enable()
        self.control_thread = threading.Thread(target=self.control_thread)

        self.bindings = {'w':( 0.07,  0.0),\
                         'a':( 0.0,  0.5),\
                         's':(-0.07,  0.0),\
                         'd':( 0.0, -0.5),\
                         ' ':( 0.0,  0.0)}
        self.help_msg = """Moving around:
                w
           a    s    d

        Spacebar to Stop!
        CTRL-C to quit
        """

    def on_start(self):
        self.control_thread.start()

    def control_thread(self):
        self.logger.info(self.help_msg)
        rate = Rate(10)
        while self.ok():
            key = get_key(0.1)
            if key == CTRL_PLUS_C:
                self.terminate()
                break
            if key in self.bindings:
                self.chassis.set_cmdvel(v=self.bindings[key][0], w=self.bindings[key][1])
            rate.sleep()


def main():
    chassis_test_agent = ChassisTestAgent()
    chassis_test_agent.start()


if __name__ == "__main__":
    main()
