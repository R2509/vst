import dawdreamer as daw

SAMPLE_RATE = 44100
BUFFER_SIZE = 128

SYNTH_PLUGIN = './SoftSynth/S-YXG50/S-YXG50.dll'

engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)

synth = engine.make_plugin_processor("s-yxg50", SYNTH_PLUGIN)
assert synth.get_name() == "s-yxg50"