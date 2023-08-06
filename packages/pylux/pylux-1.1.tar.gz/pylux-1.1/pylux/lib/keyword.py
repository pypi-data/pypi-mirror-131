CUE = 'Cue'
FILE = 'File'
FILTER = 'Filter'
FIXTURE = 'Fixture'
GROUP = 'Group'
META = 'Metadata'
ALL_PALETTE = 'AllPalette'
INTENSITY_PALETTE = 'IntensityPalette'
FOCUS_PALETTE = 'FocusPalette'
COLOUR_PALETTE = 'ColourPalette'
BEAM_PALETTE = 'BeamPalette'
PLOT = 'Plot'
PROGRAM = 'Program'
REGISTRY = 'Registry'
REPORT = 'Report'
STRUCTURE = 'Structure'
ABOUT = 'About'
APPEND = 'Append'
CLONE = 'CopyTo'
CREATE = 'Create'
CREATE_FROM = 'CreateFrom'
COMPLETE_FROM = 'CompleteFrom'
DISPLAY = 'Display'
HELP = 'Help'
IMPORT = 'Import'
LABEL = 'Label'
FAN = 'Fan'
OUTPUT = 'Output'
OUTPUT_STOP = 'StopOutput'
PATCH = 'Patch'
QUERY = 'Query'
REMOVE = 'Remove'
SET = 'Set'
UNPATCH = 'Unpatch'
WRITE = 'Write'
WRITE_TO = 'WriteTo'
WRITE_EXIT = 'WriteAndQuit'
EXIT = 'Quit'
RELOAD_CONFIG = 'ReloadConfig'

NOUNS = [CUE, FILE, FILTER, FIXTURE, GROUP, META, ALL_PALETTE,
         INTENSITY_PALETTE, FOCUS_PALETTE, COLOUR_PALETTE, BEAM_PALETTE,
         PLOT, PROGRAM, REGISTRY, REPORT, STRUCTURE]
VERBS = [ABOUT, APPEND, CLONE, CREATE, CREATE_FROM, COMPLETE_FROM, DISPLAY,
         HELP, IMPORT, LABEL, FAN, OUTPUT, OUTPUT_STOP, PATCH, QUERY,
         REMOVE, SET, UNPATCH, WRITE, WRITE_TO, WRITE_EXIT, EXIT, RELOAD_CONFIG]

KWS = NOUNS + VERBS
