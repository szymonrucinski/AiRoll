import os
import sys
import tkinter
import gobject
import gst


def on_sync_message(bus, message, window_id):
    if message.structure is not None:
        if message.structure.get_name() == 'prepare-xwindow-id':
            image_sink = message.src
            image_sink.set_property('force-aspect-ratio', True)
            image_sink.set_xwindow_id(window_id)


gobject.threads_init()

window = tkinter.Tk()
window.geometry('500x400')

video = tkinter.Frame(window, bg='#000000')
video.pack(
    side=tkinter.BOTTOM,
    anchor=tkinter.S,
    expand=tkinter.YES,
    fill=tkinter.BOTH)

window_id = video.winfo_id()

player = gst.element_factory_make('playbin2', 'player')
player.set_property('video-sink', None)
player.set_property('uri', 'file://%s' % (os.path.abspath(sys.argv[1])))
player.set_state(gst.STATE_PLAYING)

bus = player.get_bus()
bus.add_signal_watch()
bus.enable_sync_message_emission()
bus.connect('sync-message::element', on_sync_message, window_id)

window.mainloop()
