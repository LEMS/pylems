"""
Recording class(es).

@author: Gautham Ganapathy
@organization: Textensor (http://textensor.com)
@contact: gautham@textensor.com, gautham@lisphacker.org
"""

from lems.base.base import LEMSBase

class Recording(LEMSBase):
      """
      Stores details of a variable recording across a single simulation run.
      """

      def __init__(self, display, recorder):
            self.quantity = recorder.quantity

            self.scale = recorder.scale

            self.color = recorder.color

            self.numeric_scale = recorder.numeric_scale

            self.title = display.title if display else ''

            self.data_region = display.data_region if display else ''

            self.values = []

      def add_value(self, time, value):
            self.values.append((time, value))
