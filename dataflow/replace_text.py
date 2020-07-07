"""Gzip file row text replace and sava to GCS workflow."""

# pytype: skip-file

from __future__ import absolute_import

import argparse
import logging
import re

from past.builtins import unicode

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.metrics import Metrics
from apache_beam.metrics.metric import MetricsFilter
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

class UserOptions(PipelineOptions):
  @classmethod
  def _add_argparse_args(cls, parser):
    # Use add_value_provider_argument for arguments to be templatable
    # Use add_argument as usual for non-templatable arguments
    parser.add_value_provider_argument(
        '--input',
        dest='input',
        help='Path of the file to read from')
    parser.add_value_provider_argument(
        '--output',
        dest='output',
        help='Output file to write results to.')

class WordExtractingDoFn(beam.DoFn):
  """Parse each line of input text into words."""
  def __init__(self):
    beam.DoFn.__init__(self)

  def process(self, element):
    """Returns an iterator over the words of this element.

    The element is a line of text.  If the line is blank, note that, too.

    Args:
      element: the element being processed

    Returns:
      The processed element.
    """
    value = re.sub(r'\\"', '""', element)
    return [value]

def run(argv=None, save_main_session=True):
  """Main entry point; defines and runs the replace text pipeline."""
  pipeline_options = PipelineOptions()
  p = beam.Pipeline(options=pipeline_options)

  user_options = pipeline_options.view_as(UserOptions)

  # Read the text file[pattern] into a PCollection.
  (p | 'Read file from GCS' >> ReadFromText(user_options.input)
  | 'Replace Text' >> (beam.ParDo(WordExtractingDoFn()))
  | 'Mapping' >> beam.Map(lambda x: x)
  | 'Write to GCS' >> WriteToText(user_options.output))

  result = p.run()
  result.wait_until_finish()

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()

