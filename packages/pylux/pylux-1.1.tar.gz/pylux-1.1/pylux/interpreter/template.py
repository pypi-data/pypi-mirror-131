from pylux.interpreter import RegularCommand, InterpreterExtension
from pylux import document
import pygdtf
from pylux.lib import data, exception
import pylux.lib.keyword as kw
import pathlib
import os.path
from decimal import Decimal


class TemplateExtension(InterpreterExtension):

    def register_commands(self):
        self.commands.append(RegularCommand((kw.FIXTURE, kw.COMPLETE_FROM), self.fixture_completefrom))
        self.commands.append(RegularCommand((kw.FIXTURE, kw.CREATE_FROM), self.fixture_createfrom, check_refs=False))

    def _get_template_file(self, template):
        template_file = data.get_data(os.path.join('fixture', template + '.gdtf'))
        if not template_file:
            self.post_feedback(['Template {0} does not exist'.format(template)])
            return None
        return pathlib.Path(template_file)

    def fixture_completefrom(self, fixtures, template):
        template_file = self._get_template_file(template)
        if not template_file:
            return
        fixture_type = pygdtf.FixtureType(template_file)
        for fix in fixtures:
            if 'fixture-type' not in fix.data:
                fix.data['fixture-type'] = fixture_type.name
            if 'manufacturer' not in fix.data:
                fix.data['manufacturer'] = fixture_type.manufacturer
            if 'power' not in fix.data:
                fix.data['power'] = sum([b.power_consumption for b in fixture_type.get_geometry_by_type(pygdtf.GeometryBeam)])
            for dmx_chan in fixture_type.dmx_modes[0].dmx_channels:
                # GDTF stores a virtual parameter as the special text string 'None',
                # document.py uses the actual None to indicate this so we need to
                # catch and convert
                if dmx_chan.offset == 'None':
                    offset = None
                else:
                    offset = dmx_chan.offset
                fix.functions.append(document.FixtureFunction(
                    parameter=str(dmx_chan.logical_channels[0].attribute), offset=offset))

    def fixture_createfrom(self, refs, template):
        template_file = self._get_template_file(template)
        if not template_file:
            return
        for r in refs:
            # If ref is zero, use automatically assigned ref
            if r == 0:
                r = self.file.next_ref(document.Fixture)
            if self.file.get_by_ref(document.Fixture, r):
                self.post_feedback(exception.ERROR_MSG_EXISTING_OBJECT.format(
                    document.Fixture.noun, str(r)))
                continue
            self.file.insert_object(document.Fixture(ref=Decimal(r)))
            self.fixture_completefrom([Decimal(r)], template)


def register_extension(interpreter):
    return TemplateExtension(interpreter).register_extension()
